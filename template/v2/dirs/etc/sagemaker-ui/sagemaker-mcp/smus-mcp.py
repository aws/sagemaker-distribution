"""
SageMaker Unified Studio Project Context MCP Server in stdio transport.

This is a self-contained MCP Server, ready to be used directly.
Dependencies:
pip install mcp[cli]
pip install sagemaker_studio
"""

import json
import os
import logging
from typing import Any, Dict, Optional

import boto3
from mcp.server.fastmcp import FastMCP
from sagemaker_studio import ClientConfig, Project

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProjectContext:
    """
    A class that encapsulates AWS session, project object, and region.
    This class simplifies the common pattern of setting up an AWS session,
    extracting credentials, and getting a project.
    """

    def __init__(self):
        try:
            datazone_domain_id = os.getenv("AmazonDataZoneDomain")
            datazone_project_id = os.getenv("AmazonDataZoneProject")
            aws_region = os.getenv("AWS_REGION")
            if datazone_domain_id and datazone_project_id and aws_region:
                self.domain_id = datazone_domain_id
                self.project_id = datazone_project_id
                self.region = aws_region
            else:
                with open("/opt/ml/metadata/resource-metadata.json", "r") as metadata_file:
                    metadata = json.load(metadata_file)
                    self.domain_id = metadata["AdditionalMetadata"]["DataZoneDomainId"]
                    self.project_id = metadata["AdditionalMetadata"]["DataZoneProjectId"]
                    self.region = metadata["AdditionalMetadata"]["DataZoneDomainRegion"]

            logger.info(f"Read self.domain: {self.domain_id}")

            self.session = boto3.Session(profile_name="DomainExecutionRoleCreds", region_name=self.region)
            client_conf = ClientConfig(session=self.session, region=self.region)
            self.project = Project(id=self.project_id, domain_id=self.domain_id, config=client_conf)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize project: {e}")


def safe_get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    """Safely get an attribute from an object."""
    if obj is None:
        return default

    try:
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            # Handle case where attribute access might throw RuntimeError
            if callable(value):
                try:
                    return value()
                except (RuntimeError, Exception) as e:
                    logger.debug(f"Error calling attribute {attr}: {e}")
                    return default
            return value
        return default
    except Exception as e:
        logger.debug(f"Error getting attribute {attr}: {e}")
        return default


def create_smus_context_identifiers_response(domain_id: str, project_id: str, region: str) -> str:

    return f"""Selectively use the below parameters only when the parameter is required.
<parameter>
domain identifier: "{domain_id}"
project identifier: "{project_id}"
region: "{region}"
aws profiles: "DomainExecutionRoleCreds, default"
</parameter>
Again, include only required parameters. Any extra parameters may cause the API to fail. Stick strictly to the schema."""


async def aws_context_provider() -> Dict[str, Any]:
    """
    AWS Context Provider - MUST BE CALLED BEFORE ANY use_aws OPERATIONS

    This tool provides essential AWS context parameters that are required by subsequent AWS operations.
    It returns configuration details including domain identifiers, project information, and region
    settings that would otherwise need to be manually specified with each use_aws call.

    The returned parameters include:
    - domain identifier: Unique identifier for the AWS DataZone domain
    - project identifier: Identifier for the specific project being worked on
    - profile name: Name of the AWS profile to use for credentials
    - project profile connection name: Connection name for project integration
    - region: AWS region where operations should be performed
    - aws profiles: use the aws profile named DomainExecutionRoleCreds for calling datazone APIs; otherwise use default AWS profile

    Returns:
        dict: Parameter context to be used with subsequent use_aws operations
    """
    identifiers_response = ""
    try:
        ctx = ProjectContext()
        domain_id = safe_get_attr(ctx, "domain_id", "")
        project_id = safe_get_attr(ctx, "project_id", "")
        region = safe_get_attr(ctx, "region", "")
        identifiers_response = create_smus_context_identifiers_response(domain_id, project_id, region)
        return {"response": identifiers_response}
    except Exception as e:
        logger.error(f"Error providing SMUS context identifiers: {e}")
        return {"response": identifiers_response, "error": str(e)}


if __name__ == "__main__":
    mcp: FastMCP = FastMCP("SageMakerUnififedStudio Project Context MCP Server")

    # Register the tools from tools.py
    mcp.tool()(aws_context_provider)  # use the doc string of the function as description, do not overwrite here.

    mcp.run(transport="stdio")
