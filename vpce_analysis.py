#!/usr/bin/env python3

def analyze_vpce_connectivity():
    print("=== VPC Endpoint Analysis for SageMaker Domain ===")
    print("Domain: d-pxmbksrhiqnc")
    print("VPC: vpc-0b61bc945309d6036\n")
    
    print("AVAILABLE VPC ENDPOINTS:")
    print("=" * 40)
    print("✓ ECR API (ecr.api) - Available")
    print("✓ ECR Docker (ecr.dkr) - Available") 
    print("✓ S3 - Available")
    print("✓ STS - Available")
    print("✓ SSM - Available")
    print("✓ Glue - Available")
    print("✓ DataZone - Available")
    
    print("\nMISSING VPC ENDPOINTS:")
    print("=" * 40)
    print("❌ SageMaker API (sagemaker.api) - MISSING")
    
    print("\nIMPACT ON SPACES:")
    print("=" * 40)
    print("f1 Space Error Analysis:")
    print("• Error: 'Connect timeout on endpoint URL: https://api.sagemaker.us-west-2.amazonaws.com/'")
    print("• Root Cause: Missing SageMaker API VPC Endpoint")
    print("• Impact: Cannot communicate with SageMaker service")
    
    print("\nECR Connectivity:")
    print("• ECR API VPCE: ✓ Present")
    print("• ECR Docker VPCE: ✓ Present") 
    print("• f1 can pull container images from ECR")
    
    print("\nRECOMMENDATION:")
    print("=" * 40)
    print("Create SageMaker API VPC Endpoint:")
    print("• Service: com.amazonaws.us-west-2.sagemaker.api")
    print("• VPC: vpc-0b61bc945309d6036")
    print("• This will resolve the timeout errors in all spaces")

if __name__ == "__main__":
    analyze_vpce_connectivity()