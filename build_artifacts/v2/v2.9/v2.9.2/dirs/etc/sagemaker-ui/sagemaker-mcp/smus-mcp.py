"""
SageMaker Unified Studio Project Context MCP Server in stdio transport.

"""

import json
import logging
import os
import re
import time
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

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
        except Exception as e:
            raise RuntimeError(f"Failed to initialize project: {e}")

        if not re.match("^dzd[-_][a-zA-Z0-9_-]{1,36}$", self.domain_id):
            raise RuntimeError(f"Invalid domain id")
        if not re.match("^[a-zA-Z0-9_-]{1,36}$", self.project_id):
            raise RuntimeError(f"Invalid project id")
        if not re.match("^[a-z]{2}-[a-z]{4,10}-\\d$", self.region):
            raise RuntimeError(f"Invalid region")


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
                    logger.error(f"Error calling attribute {attr}: {e}")
                    return default
            return value
        return default
    except Exception as e:
        logger.error(f"Error getting attribute {attr}: {e}")
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


def write_log_entry(
    operation: str, tool_name: str, error_count: int = 0, domain_id: str = "", latency: float = 0
) -> None:
    """
    Write a log entry to the SageMaker GenAI Jupyter Lab extension log file.

    Args:
        operation: The operation being performed
        tool_name: The name of the tool being used
        error_count: Number of errors (0 for success, 1 for failure)
        domain_id: The domain identifier (optional)
        latency: Execution latency in milliseconds
    """
    try:
        log_entry = {
            "Operation": operation,
            "ToolName": tool_name,
            "ErrorCount": error_count,
            "DomainId": domain_id,
            "Latency": latency,
            "_aws": {
                "Timestamp": int(time.time() * 1000),
                "CloudWatchMetrics": [
                    {
                        "Dimensions": [["Operation"], ["ToolName"]],
                        "Metrics": [
                            {"Name": "ErrorCount", "Unit": "Count"},
                            {"Name": "Latency", "Unit": "Milliseconds"},
                        ],
                        "Namespace": "SagemakerGenAIJupyterLab",
                    }
                ],
            },
        }

        # Write to log file
        log_file_path = "/var/log/studio/sagemaker_genai_jl_ext/sagemaker_genai_jl_extension.log"
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

    except Exception:
        # Fail quietly - logging failures shouldn't affect main functionality
        pass


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
    - region: AWS region where operations should be performed
    - aws profiles: use the aws profile named DomainExecutionRoleCreds for calling datazone APIs; otherwise use default AWS profile

    Returns:
        dict: Parameter context to be used with subsequent use_aws operations
    """
    start_time = time.time()
    identifiers_response = ""
    domain_id = ""
    try:
        ctx = ProjectContext()
        domain_id = safe_get_attr(ctx, "domain_id", "")
        project_id = safe_get_attr(ctx, "project_id", "")
        region = safe_get_attr(ctx, "region", "")
        identifiers_response = create_smus_context_identifiers_response(domain_id, project_id, region)

        latency = (time.time() - start_time) * 1000
        write_log_entry("SMUS-Local-MCP", "aws_context_provider", 0, domain_id, latency)

        return {"response": identifiers_response}
    except Exception as e:
        logger.error(f"Error providing SMUS context identifiers: {e}")
        # Calculate latency and log error
        latency = (time.time() - start_time) * 1000
        error_domain_id = domain_id if domain_id else "unable to retrieve domain id"
        write_log_entry("SMUS-Local-MCP", "aws_context_provider", 1, error_domain_id, latency)
        return {"response": identifiers_response, "error": "Error providing SMUS context identifiers"}


if __name__ == "__main__":
    mcp: FastMCP = FastMCP("SageMakerUnififedStudio Project Context MCP Server")

    # Register the tools from tools.py
    mcp.tool()(aws_context_provider)  # use the doc string of the function as description, do not overwrite here.

    mcp.run(transport="stdio")
