#!/usr/bin/env python3
import boto3
import json

def check_space_connectivity(domain_id, space_names):
    sagemaker = boto3.client('sagemaker', region_name='us-west-2')
    
    results = {}
    
    for space_name in space_names:
        try:
            response = sagemaker.describe_space(
                DomainId=domain_id,
                SpaceName=space_name
            )
            
            space_settings = response.get('SpaceSettings', {})
            
            # Extract network-related configurations
            network_config = {
                'space_name': space_name,
                'jupyter_server_app_settings': space_settings.get('JupyterServerAppSettings', {}),
                'kernel_gateway_app_settings': space_settings.get('KernelGatewayAppSettings', {}),
                'code_editor_app_settings': space_settings.get('CodeEditorAppSettings', {}),
                'space_sharing_settings': space_settings.get('SpaceSharingSettings', {}),
                'custom_file_systems': space_settings.get('CustomFileSystems', [])
            }
            
            # Check for VPC/subnet configurations in app settings
            for app_type in ['jupyter_server_app_settings', 'kernel_gateway_app_settings', 'code_editor_app_settings']:
                app_settings = network_config[app_type]
                if 'DefaultResourceSpec' in app_settings:
                    resource_spec = app_settings['DefaultResourceSpec']
                    if 'SageMakerImageArn' in resource_spec:
                        network_config[f'{app_type}_image'] = resource_spec['SageMakerImageArn']
            
            results[space_name] = network_config
            
        except Exception as e:
            results[space_name] = {'error': str(e)}
    
    return results

def compare_connectivity(results):
    print("=== SageMaker Space Network Connectivity Comparison ===\n")
    
    space_names = list(results.keys())
    
    for space_name, config in results.items():
        print(f"Space: {space_name}")
        if 'error' in config:
            print(f"  Error: {config['error']}\n")
            continue
            
        print(f"  Jupyter Server App Settings: {bool(config['jupyter_server_app_settings'])}")
        print(f"  Kernel Gateway App Settings: {bool(config['kernel_gateway_app_settings'])}")
        print(f"  Code Editor App Settings: {bool(config['code_editor_app_settings'])}")
        print(f"  Custom File Systems: {len(config['custom_file_systems'])}")
        print()
    
    # Compare differences
    if len(space_names) >= 2:
        print("=== Key Differences ===")
        space1, space2 = space_names[0], space_names[1]
        
        if 'error' not in results[space1] and 'error' not in results[space2]:
            config1, config2 = results[space1], results[space2]
            
            for key in config1:
                if key != 'space_name' and config1[key] != config2[key]:
                    print(f"  {key}:")
                    print(f"    {space1}: {config1[key]}")
                    print(f"    {space2}: {config2[key]}")

if __name__ == "__main__":
    domain_id = "d-pxmbksrhiqnc"
    spaces = ["f2", "test"]
    
    results = check_space_connectivity(domain_id, spaces)
    compare_connectivity(results)
    
    # Also get domain-level network settings for context
    sagemaker = boto3.client('sagemaker', region_name='us-west-2')
    try:
        domain_response = sagemaker.describe_domain(DomainId=domain_id)
        print("\n=== Domain Network Settings ===")
        print(f"VPC ID: {domain_response.get('VpcId', 'N/A')}")
        print(f"Subnet IDs: {domain_response.get('SubnetIds', [])}")
        print(f"App Network Access Type: {domain_response.get('AppNetworkAccessType', 'N/A')}")
    except Exception as e:
        print(f"\nError getting domain info: {e}")