import json
import os
import re

import yaml


def generate_intelligent_default_config(metadata: str) -> dict:
    has_vpc = metadata["SecurityGroupIds"] and metadata["Subnets"] and metadata["SecurityGroupIds"] != [''] and metadata["Subnets"] != ['']
    vpc_config = {"SecurityGroupIds": metadata["SecurityGroupIds"], "Subnets": metadata["Subnets"]} if has_vpc else None
    
    config = {
        "SchemaVersion": "1.0",
        "SageMaker": {
            "PythonSDK": {
                "Modules": {
                    "Session": {
                        "DefaultS3Bucket": metadata["S3Bucket"],
                        "DefaultS3ObjectKeyPrefix": metadata["S3ObjectKeyPrefix"],
                    },
                    "RemoteFunction": {
                        "IncludeLocalWorkDir": True,
                    },
                    "NotebookJob": {
                        "RoleArn": metadata["UserRoleArn"],
                        "S3RootUri": f"s3://{metadata['S3Bucket']}/{metadata['S3ObjectKeyPrefix']}",
                    },
                    "Serve": {"S3ModelDataUri": f"s3://{metadata['S3Bucket']}/{metadata['S3ObjectKeyPrefix']}"},
                }
            },
            "Pipeline": {"RoleArn": metadata["UserRoleArn"]},
            "Model": {"ExecutionRoleArn": metadata["UserRoleArn"]},
            "ModelPackage": {"ValidationSpecification": {"ValidationRole": metadata["UserRoleArn"]}},
            "ProcessingJob": {"RoleArn": metadata["UserRoleArn"]},
            "TrainingJob": {"RoleArn": metadata["UserRoleArn"]},
        },
    }
    
    if has_vpc:
        config["SageMaker"]["PythonSDK"]["Modules"]["RemoteFunction"]["VpcConfig"] = vpc_config
        config["SageMaker"]["PythonSDK"]["Modules"]["NotebookJob"]["VpcConfig"] = vpc_config
        config["SageMaker"]["MonitoringSchedule"] = {
            "MonitoringScheduleConfig": {
                "MonitoringJobDefinition": {
                    "NetworkConfig": {"VpcConfig": vpc_config}
                }
            }
        }
        config["SageMaker"]["AutoMLJob"] = {
            "AutoMLJobConfig": {
                "SecurityConfig": {"VpcConfig": vpc_config}
            }
        }
        config["SageMaker"]["AutoMLJobV2"] = {
            "SecurityConfig": {"VpcConfig": vpc_config}
        }
        config["SageMaker"]["CompilationJob"] = {"VpcConfig": vpc_config}
        config["SageMaker"]["Model"]["VpcConfig"] = vpc_config
        config["SageMaker"]["ProcessingJob"]["NetworkConfig"] = {"VpcConfig": vpc_config}
        config["SageMaker"]["TrainingJob"]["VpcConfig"] = vpc_config
    
    return config


if __name__ == "__main__":
    try:
        config = {}
        resource_metadata = "/opt/ml/metadata/resource-metadata.json"

        PROJECT_S3_PATH = "ProjectS3Path"
        SECURITY_GROUP = "SecurityGroup"
        PRIVATE_SUBNETS = "PrivateSubnets"
        META_DATA = "AdditionalMetadata"
        EXECUTION_ROLE_ARN = "ExecutionRoleArn"
        CONFIG_FILE_NAME = "config.yaml"
        CONFIG_DIR = "/etc/xdg/sagemaker/"

        if os.path.exists(resource_metadata):
            with open(resource_metadata, "r") as file:
                data = json.load(file)

            s3_path = data[META_DATA].get(PROJECT_S3_PATH, "")
            metadata = {
                # user provided bucket
                "S3Bucket": re.search(r"s3://([^/]+)/", s3_path).group(1),
                # ${datazoneEnvironmentDomainId}/${datazoneEnvironmentProjectId}/${datazoneScopeName}/
                "S3ObjectKeyPrefix": s3_path.split("//")[1].split("/", 1)[1],
                # TODO: Is this a billing concern if set default
                # 'InstanceType': 'ml.m5.xlarge',
                "SecurityGroupIds": data[META_DATA].get(SECURITY_GROUP, "").split(","),
                "Subnets": data[META_DATA].get(PRIVATE_SUBNETS, "").split(","),
                "UserRoleArn": data[EXECUTION_ROLE_ARN],
            }

            # Not create config file when invalid value exists in metadata
            empty_values = [key for key, value in metadata.items() if key not in ["SecurityGroupIds", "Subnets"] and (value == "" or value == [""])]
            if empty_values:
                raise AttributeError(f"There are empty values in the metadata: {empty_values}")

            config = generate_intelligent_default_config(metadata)
        else:
            raise FileNotFoundError("No resource-metadata.json exists on host!")

        # Write the config YAML file to default location of the admin config file
        with open(os.path.join(CONFIG_DIR, CONFIG_FILE_NAME), "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    except Exception as e:
        print(f"Error: {e}, SageMaker PySDK intelligent config file is not valid!")
