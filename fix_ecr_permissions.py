#!/usr/bin/env python3
import boto3
import json

def add_ecr_permissions_to_domain_role():
    iam = boto3.client('iam')
    role_name = "AmazonSageMakerDomainExecution"
    
    # ECR policy for SageMaker domain execution
    ecr_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ecr:GetAuthorizationToken",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage",
                    "ecr:DescribeRepositories",
                    "ecr:DescribeImages"
                ],
                "Resource": "*"
            }
        ]
    }
    
    try:
        # Add inline policy to the role
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName="ECRAccessForSageMakerDomain",
            PolicyDocument=json.dumps(ecr_policy)
        )
        
        print(f"✅ Added ECR permissions to {role_name}")
        print("Policy: ECRAccessForSageMakerDomain")
        print("Permissions added:")
        for action in ecr_policy["Statement"][0]["Action"]:
            print(f"  • {action}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error adding ECR permissions: {e}")
        return False

def verify_fix():
    print("\n" + "="*50)
    print("VERIFICATION:")
    
    # Re-run the permission check
    import subprocess
    result = subprocess.run(['python', 'check_ecr_permissions.py'], 
                          capture_output=True, text=True)
    
    if "Domain Execution Role ECR Access: ✓" in result.stdout:
        print("✅ ECR permissions successfully added!")
        print("The 'no such image' error should now be resolved.")
    else:
        print("❌ Issue persists, manual intervention may be needed")

if __name__ == "__main__":
    print("=== Fixing ECR Permissions for Domain Execution Role ===")
    
    success = add_ecr_permissions_to_domain_role()
    
    if success:
        verify_fix()