#!/usr/bin/env python3
import boto3
import json

def detailed_space_analysis(domain_id, space_names):
    sagemaker = boto3.client('sagemaker', region_name='us-west-2')
    
    print("=== Detailed Network Connectivity Analysis ===\n")
    
    for space_name in space_names:
        print(f"Space: {space_name}")
        print("-" * 40)
        
        try:
            response = sagemaker.describe_space(
                DomainId=domain_id,
                SpaceName=space_name
            )
            
            # Print full space configuration
            space_settings = response.get('SpaceSettings', {})
            
            print(f"Space Settings Keys: {list(space_settings.keys())}")
            
            # Check each app type for network-related settings
            app_types = ['JupyterServerAppSettings', 'KernelGatewayAppSettings', 'CodeEditorAppSettings']
            
            for app_type in app_types:
                if app_type in space_settings:
                    settings = space_settings[app_type]
                    print(f"\n{app_type}:")
                    if settings:
                        for key, value in settings.items():
                            print(f"  {key}: {value}")
                    else:
                        print("  (Empty)")
                else:
                    print(f"\n{app_type}: Not configured")
            
            # Check for any other network-related configurations
            other_keys = [k for k in space_settings.keys() if k not in app_types]
            if other_keys:
                print(f"\nOther Settings:")
                for key in other_keys:
                    print(f"  {key}: {space_settings[key]}")
            
            print("\n" + "="*50 + "\n")
            
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    domain_id = "d-pxmbksrhiqnc"
    spaces = ["f2", "test"]
    
    detailed_space_analysis(domain_id, spaces)