#!/usr/bin/env python3
import boto3
import time

def check_vpce_status():
    ec2 = boto3.client('ec2', region_name='us-west-2')
    
    # Check the new endpoint status
    vpce_id = 'vpce-040a072980491a0c8'
    
    try:
        response = ec2.describe_vpc_endpoints(VpcEndpointIds=[vpce_id])
        endpoint = response['VpcEndpoints'][0]
        
        print(f"VPC Endpoint: {vpce_id}")
        print(f"Status: {endpoint['State']}")
        print(f"Service: {endpoint['ServiceName']}")
        
        if endpoint['State'] == 'available':
            print("✅ SageMaker API VPC Endpoint is ready!")
            print("\nNext steps:")
            print("1. Restart JupyterLab apps in f1, f2, test spaces")
            print("2. The timeout errors should be resolved")
        else:
            print("⏳ Still provisioning... (typically takes 2-5 minutes)")
            
    except Exception as e:
        print(f"Error checking status: {e}")

def verify_all_endpoints():
    print("=== Updated VPC Endpoint Status ===")
    check_vpce_status()
    
    print("\n" + "="*40)
    print("Running full connectivity check...")
    
    # Re-run the original check
    import subprocess
    subprocess.run(['python', 'check_vpce.py'])

if __name__ == "__main__":
    verify_all_endpoints()