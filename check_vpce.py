#!/usr/bin/env python3
import boto3

def check_vpc_endpoints(domain_id):
    sagemaker = boto3.client('sagemaker', region_name='us-west-2')
    ec2 = boto3.client('ec2', region_name='us-west-2')
    
    # Get domain VPC info
    domain = sagemaker.describe_domain(DomainId=domain_id)
    vpc_id = domain['VpcId']
    
    print(f"Domain VPC: {vpc_id}")
    print("=" * 50)
    
    # List VPC endpoints in the VPC
    vpce_response = ec2.describe_vpc_endpoints(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
    )
    
    print("VPC Endpoints:")
    sagemaker_vpce = False
    ecr_vpce = False
    
    for vpce in vpce_response['VpcEndpoints']:
        service_name = vpce['ServiceName']
        state = vpce['State']
        print(f"  • {service_name} - {state}")
        
        if 'sagemaker.api' in service_name:
            sagemaker_vpce = True
        if 'ecr.dkr' in service_name or 'ecr.api' in service_name:
            ecr_vpce = True
    
    print("\n" + "=" * 50)
    print("CONNECTIVITY ANALYSIS:")
    print(f"✓ SageMaker API VPCE: {'Present' if sagemaker_vpce else 'MISSING'}")
    print(f"✓ ECR VPCE: {'Present' if ecr_vpce else 'MISSING'}")
    
    if not sagemaker_vpce:
        print("\n⚠️  ISSUE FOUND:")
        print("   Missing SageMaker API VPC Endpoint")
        print("   This explains the timeout error in f1's JupyterLab logs")
        print("   Spaces cannot reach api.sagemaker.us-west-2.amazonaws.com")

if __name__ == "__main__":
    check_vpc_endpoints("d-pxmbksrhiqnc")