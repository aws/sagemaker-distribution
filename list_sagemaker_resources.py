#!/usr/bin/env python3
import boto3

def list_sagemaker_resources():
    sagemaker = boto3.client('sagemaker', region_name='us-west-2')
    
    print("=== Available SageMaker Domains ===")
    try:
        domains = sagemaker.list_domains()
        for domain in domains['Domains']:
            print(f"Domain ID: {domain['DomainId']}")
            print(f"Domain Name: {domain['DomainName']}")
            print(f"Status: {domain['Status']}")
            print()
            
            # List spaces in this domain
            try:
                spaces = sagemaker.list_spaces(DomainIdEquals=domain['DomainId'])
                print(f"  Spaces in {domain['DomainId']}:")
                for space in spaces['Spaces']:
                    print(f"    - {space['SpaceName']} (Status: {space['Status']})")
                print()
            except Exception as e:
                print(f"  Error listing spaces: {e}\n")
                
    except Exception as e:
        print(f"Error listing domains: {e}")

if __name__ == "__main__":
    list_sagemaker_resources()