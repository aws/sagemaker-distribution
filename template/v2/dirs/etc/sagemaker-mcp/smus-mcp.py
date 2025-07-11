"""
SageMaker Unified Studio Project Context MCP Server in stdio transport.

This is a self-contained MCP Server, ready to be used directly.
Dependencies:
pip install mcp[cli]
pip install sagemaker_studio
"""

import json
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
            with open("/opt/ml/metadata/resource-metadata.json", "r") as metadata_file:
                metadata = json.load(metadata_file)
                self.domain_id = metadata["AdditionalMetadata"]["DataZoneDomainId"]
                self.project_id = metadata["AdditionalMetadata"]["DataZoneProjectId"]
                self.region = metadata["AdditionalMetadata"]["DataZoneDomainRegion"]

            logger.info(f"Read self.domain: {self.domain_id}")

            self.session = boto3.Session(region_name=self.region)
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

    Returns:
        dict: Parameter context to be used with subsequent use_aws operations
    """
    identifiers_response = ""
    try:
        ctx = ProjectContext()
        domain_id = safe_get_attr(ctx, "domain_id", "")
        project_id = safe_get_attr(ctx, "project_id", "")
        region = safe_get_attr(ctx, "region", "")
        identifiers_response = create_smus_context_identifiers_response(
            domain_id, project_id, region
        )
        return {"response": identifiers_response}
    except Exception as e:
        logger.error(f"Error providing SMUS context identifiers: {e}")
        return {"response": identifiers_response, "error": str(e)}


async def list_tables(
    catalog_id: Optional[str] = None, database_name: Optional[str] = None
) -> dict:
    """List all available tables, optionally filtered by catalog ID and database name."""
    try:
        ctx = ProjectContext()
        connections = safe_get_attr(ctx.project, "connections", [])
        tables_list = []

        for conn in connections:
            conn_type = safe_get_attr(conn, "type", "")
            if conn_type != 'IAM' and conn_type != 'LAKEHOUSE':
                continue
            # collect lakehouse catalogs
            catalogs = safe_get_attr(conn, "catalogs", [])

            # collect glue catalogs
            catalogs.append(conn.catalog())
            for catalog in catalogs:
                current_catalog_id = safe_get_attr(catalog, "id")

                # Skip if catalog_id is provided and doesn't match
                if catalog_id and current_catalog_id != catalog_id:
                    continue

                databases = safe_get_attr(catalog, "databases", [])
                for db in databases:
                    current_db_name = safe_get_attr(db, "name")

                    # Skip if database_name is provided and doesn't match
                    if database_name and current_db_name != database_name:
                        continue

                    tables = safe_get_attr(db, "tables", [])

                    for table in tables:
                        table_name = safe_get_attr(table, "name")

                        if table_name:
                            table_info = {
                                "name": table_name,
                                "database_name": current_db_name,
                                "catalog_id": current_catalog_id,
                            }

                            # Add location if available
                            location = safe_get_attr(table, "location")
                            if location:
                                table_info["location"] = location

                            # Get columns if available
                            columns = safe_get_attr(table, "columns", [])
                            columns_info = []

                            for column in columns:
                                col_name = safe_get_attr(column, "name")
                                col_type = safe_get_attr(column, "type")

                                if col_name and col_type:
                                    columns_info.append({"name": col_name, "type": col_type})

                            if columns_info:
                                table_info["columns"] = columns_info

                            tables_list.append(table_info)

        return {"tables": tables_list}
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        return {"tables": [], "error": str(e)}


async def get_table_schema(catalog_id: str, database_name: str, table_name: str) -> dict:
    """Get schema information for a specific table."""
    try:
        ctx = ProjectContext()
        connections = safe_get_attr(ctx.project, "connections", [])

        for conn in connections:
            conn_type = safe_get_attr(conn, "type", "")
            if conn_type != 'IAM' and conn_type != 'LAKEHOUSE':
                continue
            # collect lakehouse catalogs
            catalogs = safe_get_attr(conn, "catalogs", [])

            # collect glue catalogs
            catalogs.append(conn.catalog())
            for catalog in catalogs:
                current_catalog_id = safe_get_attr(catalog, "id")
                if current_catalog_id != catalog_id:
                    continue

                databases = safe_get_attr(catalog, "databases", [])
                for db in databases:
                    current_db_name = safe_get_attr(db, "name")
                    if current_db_name != database_name:
                        continue

                    tables = safe_get_attr(db, "tables", [])
                    for table in tables:
                        current_table_name = safe_get_attr(table, "name")
                        if current_table_name != table_name:
                            continue

                        # Get columns
                        columns = safe_get_attr(table, "columns", [])
                        columns_info = []
                        for column in columns:
                            col_name = safe_get_attr(column, "name")
                            col_type = safe_get_attr(column, "type")
                            if col_name and col_type:
                                column_info = {"name": col_name, "type": col_type}
                                comment = safe_get_attr(column, "comment")
                                if comment:
                                    column_info["comment"] = comment
                                columns_info.append(column_info)
                        table_info = {
                            "name": table_name,
                            "database_name": database_name,
                            "catalog_id": catalog_id,
                            "columns": columns_info,
                        }
                        location = safe_get_attr(table, "location")
                        if location:
                            table_info["location"] = location

                        return table_info

        return {"error": f"Table not found: {catalog_id}.{database_name}.{table_name}"}
    except Exception as e:
        logger.error(f"Error listing table schema: {e}")
        return {"error": str(e)}


def create_mcp_server():
    """
    Create and return a new FastMCP server instance.
    This ensures a fresh instance is created for each Lambda invocation.
    """
    mcp: FastMCP = FastMCP(
        stateless_http=True,
    )

    # Register the tools from tools.py
    mcp.tool()(
        aws_context_provider
    )  # use the doc string of the function as description, do not overwrite here.

    mcp.tool(
        description="List all available tables, optionally filtered by catalog ID and database name"
    )(list_tables)
    mcp.tool(description="Get schema information for a specific table")(get_table_schema)

    return mcp


# For local development only
if __name__ == "__main__":
    # Create the initial FastMCP server for local development
    mcp = create_mcp_server()
    mcp.run(transport="stdio")
