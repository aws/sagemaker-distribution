#!/usr/bin/env python3
import boto3
import json

def check_role_ecr_permissions(role_arn):
    iam = boto3.client('iam')
    role_name = role_arn.split('/')[-1]
    
    print(f"\n=== Checking Role: {role_name} ===")
    
    try:
        # Get role policies
        role = iam.get_role(RoleName=role_name)
        
        # Check inline policies
        inline_policies = iam.list_role_policies(RoleName=role_name)
        
        # Check attached managed policies
        attached_policies = iam.list_attached_role_policies(RoleName=role_name)
        
        ecr_permissions = []
        
        # Check inline policies
        for policy_name in inline_policies['PolicyNames']:
            policy = iam.get_role_policy(RoleName=role_name, PolicyName=policy_name)
            policy_doc = policy['PolicyDocument']
            
            for statement in policy_doc.get('Statement', []):
                actions = statement.get('Action', [])
                if isinstance(actions, str):
                    actions = [actions]
                
                ecr_actions = [action for action in actions if 'ecr:' in action.lower() or action == '*']
                if ecr_actions:
                    ecr_permissions.extend(ecr_actions)
        
        # Check managed policies
        for policy in attached_policies['AttachedPolicies']:
            policy_arn = policy['PolicyArn']
            policy_name = policy['PolicyName']
            
            if 'ecr' in policy_name.lower() or 'sagemaker' in policy_name.lower():
                print(f"  Relevant managed policy: {policy_name}")
                
                try:
                    policy_version = iam.get_policy(PolicyArn=policy_arn)
                    policy_doc = iam.get_policy_version(
                        PolicyArn=policy_arn,
                        VersionId=policy_version['Policy']['DefaultVersionId']
                    )
                    
                    for statement in policy_doc['PolicyVersion']['Document'].get('Statement', []):
                        actions = statement.get('Action', [])
                        if isinstance(actions, str):
                            actions = [actions]
                        
                        ecr_actions = [action for action in actions if 'ecr:' in action.lower() or action == '*']
                        if ecr_actions:
                            ecr_permissions.extend(ecr_actions)
                except:
                    pass
        
        # Check for required ECR permissions
        required_ecr_perms = [
            'ecr:GetAuthorizationToken',
            'ecr:BatchCheckLayerAvailability', 
            'ecr:GetDownloadUrlForLayer',
            'ecr:BatchGetImage'
        ]
        
        print(f"  ECR permissions found: {list(set(ecr_permissions))}")
        
        has_all_required = all(
            any(perm in found or found == '*' for found in ecr_permissions) 
            for perm in required_ecr_perms
        )
        
        print(f"  Has required ECR permissions: {'✓' if has_all_required else '❌'}")
        
        return has_all_required
        
    except Exception as e:
        print(f"  Error checking role: {e}")
        return False

def check_datazone_domain_execution_role(domain_id):
    datazone = boto3.client('datazone', region_name='us-west-2')
    
    try:
        domain = datazone.get_domain(identifier=domain_id)
        execution_role = domain.get('domainExecutionRole')
        
        if execution_role:
            print(f"\nDataZone Domain Execution Role: {execution_role}")
            return check_role_ecr_permissions(execution_role)
        else:
            print("\nNo domain execution role found")
            return False
            
    except Exception as e:
        print(f"Error getting DataZone domain: {e}")
        return False

def main():
    print("=== ECR Permissions Analysis ===")
    
    # Check DataZone user role
    user_role = "arn:aws:iam::558210242385:role/datazone_usr_role_4camhtkdokngr4_c59ctxrefg0vf4"
    user_role_ok = check_role_ecr_permissions(user_role)
    
    # Check DataZone domain execution role
    domain_id = "dzd_bwj5l674y6akb4"
    domain_role_ok = check_datazone_domain_execution_role(domain_id)
    
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"DataZone User Role ECR Access: {'✓' if user_role_ok else '❌'}")
    print(f"Domain Execution Role ECR Access: {'✓' if domain_role_ok else '❌'}")
    
    if not (user_role_ok or domain_role_ok):
        print("\n⚠️  ISSUE: Neither role has sufficient ECR permissions")
        print("Required ECR permissions:")
        print("  • ecr:GetAuthorizationToken")
        print("  • ecr:BatchCheckLayerAvailability")
        print("  • ecr:GetDownloadUrlForLayer") 
        print("  • ecr:BatchGetImage")

if __name__ == "__main__":
    main()