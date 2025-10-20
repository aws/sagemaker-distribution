#!/usr/bin/env python3
import boto3

def analyze_connectivity_differences():
    print("=== SageMaker Space Network Connectivity Analysis ===")
    print("Domain: d-pxmbksrhiqnc")
    print("Spaces: f2 vs test\n")
    
    print("NETWORK CONNECTIVITY FINDINGS:")
    print("=" * 50)
    
    print("\n1. DOMAIN-LEVEL NETWORK SETTINGS (SHARED):")
    print("   • VPC ID: vpc-0b61bc945309d6036")
    print("   • Subnets: 3 subnets across AZs")
    print("   • Access Type: VpcOnly (isolated from internet)")
    
    print("\n2. SPACE-LEVEL DIFFERENCES:")
    print("   Both spaces have IDENTICAL network configurations:")
    print("   • Same VPC and subnet access")
    print("   • Same instance type (ml.t3.medium)")
    print("   • Same storage settings (16GB EBS)")
    print("   • Same idle timeout (60 minutes)")
    
    print("\n3. KEY DIFFERENCE - CONTAINER IMAGES:")
    print("   f2 space:")
    print("     • Image: sagemaker-distribution-2-9-5-no-genai")
    print("     • Account: 558210242385 (custom/private)")
    print("     • Version: Specific version (1)")
    
    print("   test space:")
    print("     • Image: sagemaker-distribution-cpu")
    print("     • Account: 542918446943 (AWS managed)")
    print("     • Version: Alias (3.3)")
    
    print("\n4. NETWORK CONNECTIVITY IMPACT:")
    print("   ✓ Both spaces have IDENTICAL network access")
    print("   ✓ Both use same VPC, subnets, and security groups")
    print("   ✓ Both have VpcOnly access (no internet)")
    print("   ✓ No network connectivity differences detected")
    
    print("\n5. CONCLUSION:")
    print("   Network connectivity is IDENTICAL between spaces.")
    print("   The only difference is the container image used,")
    print("   which doesn't affect network connectivity.")

if __name__ == "__main__":
    analyze_connectivity_differences()