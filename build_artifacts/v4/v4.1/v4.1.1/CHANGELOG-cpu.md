# Change log: 4.1.1 (cpu)

This page lists all package changes since the previous release (4.1.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
boto3|1.42.91|1.42.97|patch
jupyterlab|4.5.6|4.5.7|patch
notebook|7.5.5|7.5.6|patch
docker-cli|29.4.1|29.4.2|patch
sagemaker-code-editor|1.9.5|1.9.6|patch
uv|0.11.8|0.11.9|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libexpat|2.7.5|2.8.0|minor
libdeflate|1.24|1.25|minor
aiobotocore|3.5.0|3.6.0|minor
wcwidth|0.6.0|0.7.0|minor
jupyter_server|2.17.0|2.18.1|minor
google-auth|2.49.2|2.50.0|minor
fastprogress|1.1.3|1.0.3|minor
cloudpathlib|0.23.0|0.24.0|minor
databricks-sdk|0.105.0|0.106.0|minor
jupyter-server-mcp|0.1.2|0.2.1|minor
langsmith|0.7.37|0.8.0|minor
sagemaker-core|2.9.0|2.10.0|minor
sagemaker-train|1.9.0|1.10.0|minor
sagemaker-serve|1.9.0|1.10.0|minor
sagemaker-mlops|1.7.1|1.10.0|minor
libsqlite|3.53.0|3.53.1|patch
botocore|1.42.91|1.42.97|patch
parso|0.8.6|0.8.7|patch
mistune|3.2.0|3.2.1|patch
authlib|1.7.0|1.7.1|patch
virtualenv|21.3.0|21.3.1|patch
fastcore|1.12.43|1.12.44|patch
typer|0.25.0|0.25.1|patch
conda-libmamba-solver|26.4.0|26.4.1|patch
cyclopts|4.11.0|4.11.2|patch
gitpython|3.1.48|3.1.49|patch
jupyter-ai-router|0.0.4|0.0.5|patch
jupyter_server_documents|0.2.0|0.2.1|patch
jupyterlab-commands-toolkit|0.1.5|0.1.6|patch
pymysql|1.1.2|1.1.3|patch

### Removed

Package | Last Version
---|---
apsw|3.53.0.0
apswutils|0.1.2
fastlite|0.2.3
oauthlib|3.3.1
python-fasthtml|0.13.4
