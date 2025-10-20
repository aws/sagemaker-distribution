#!/usr/bin/env python3
import boto3

def check_unified_studio_services():
    ec2 = boto3.client('ec2', region_name='us-west-2')
    
    # Check available VPC endpoint services
    services = ec2.describe_vpc_endpoint_services()
    
    print("=== SageMaker Unified Studio Related Services ===")
    
    unified_services = []
    for service in services['ServiceNames']:
        if any(keyword in service.lower() for keyword in ['sagemaker', 'datazone', 'unified']):
            unified_services.append(service)
    
    print("Available services:")
    for service in sorted(unified_services):
        print(f"  • {service}")
    
    print("\n=== Current VPC Endpoints Analysis ===")
    
    # Get current endpoints
    domain_vpc = 'vpc-0b61bc945309d6036'
    vpce_response = ec2.describe_vpc_endpoints(
        Filters=[{'Name': 'vpc-id', 'Values': [domain_vpc]}]
    )
    
    current_services = []
    for vpce in vpce_response['VpcEndpoints']:
        current_services.append(vpce['ServiceName'])
    
    print("Currently configured:")
    print(f"  ✓ SageMaker API: {'Present' if any('sagemaker.api' in s for s in current_services) else 'Missing'}")
    print(f"  ✓ DataZone: {'Present' if any('datazone' in s for s in current_services) else 'Missing'}")
    
    print("\n=== Unified Studio Requirements ===")
    print("For SageMaker Unified Studio domains:")
    print("  • DataZone VPCE: Required for project/domain management")
    print("  • SageMaker API VPCE: Required for ML workloads")
    print("  • No separate 'Unified Studio' VPCE exists")
    print("  • DZ + SM VPCEs should suffice for full functionality")

if __name__ == "__main__":
    check_unified_studio_services()