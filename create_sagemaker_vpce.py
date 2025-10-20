#!/usr/bin/env python3
import boto3

def create_sagemaker_vpce():
    ec2 = boto3.client('ec2', region_name='us-west-2')
    sagemaker = boto3.client('sagemaker', region_name='us-west-2')
    
    # Get VPC and subnet info from domain
    domain = sagemaker.describe_domain(DomainId='d-pxmbksrhiqnc')
    vpc_id = domain['VpcId']
    subnet_ids = domain['SubnetIds']
    
    print(f"Creating SageMaker API VPC Endpoint...")
    print(f"VPC: {vpc_id}")
    print(f"Subnets: {subnet_ids}")
    
    try:
        response = ec2.create_vpc_endpoint(
            VpcId=vpc_id,
            ServiceName='com.amazonaws.us-west-2.sagemaker.api',
            VpcEndpointType='Interface',
            SubnetIds=subnet_ids,
            PolicyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":"*","Action":"*","Resource":"*"}]}'
        )
        
        vpce_id = response['VpcEndpoint']['VpcEndpointId']
        print(f"✅ Created VPC Endpoint: {vpce_id}")
        print("⏳ Endpoint is being provisioned...")
        
        return vpce_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    create_sagemaker_vpce()