# Change log: 4.2.0 (cpu)

This page lists all package changes since the previous release (4.1.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
boto3|1.42.91|1.43.0|minor
pip|26.0.1|26.1.1|minor
s3fs|2026.3.0|2026.4.0|minor
sagemaker-mlflow|0.3.0|0.4.0|minor
jupyterlab|4.5.6|4.5.7|patch
notebook|7.5.5|7.5.6|patch
docker-cli|29.4.1|29.4.3|patch
sagemaker-code-editor|1.9.5|1.9.6|patch
sagemaker-studio|1.1.14|1.1.15|patch
sagemaker-studio-dataengineering-extensions|1.3.9|1.3.10|patch
sagemaker-studio-dataengineering-sessions|1.3.19|1.3.20|patch
uv|0.11.8|0.11.11|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libexpat|2.7.5|2.8.0|minor
fsspec|2026.3.0|2026.4.0|minor
hf-xet|1.4.3|1.5.0|minor
libdeflate|1.24|1.25|minor
botocore|1.42.91|1.43.0|minor
aiobotocore|3.5.0|3.6.0|minor
s3transfer|0.16.1|0.17.0|minor
traitlets|5.14.3|5.15.0|minor
wcwidth|0.6.0|0.7.0|minor
jupyter_server|2.17.0|2.18.2|minor
google-auth|2.49.2|2.50.0|minor
python-discovery|1.2.2|1.3.0|minor
markdown-it-py|4.0.0|4.1.0|minor
cloudpathlib|0.23.0|0.24.0|minor
databricks-sdk|0.105.0|0.106.0|minor
jupyter-server-mcp|0.1.2|0.2.1|minor
langsmith|0.7.37|0.8.1|minor
sagemaker-core|2.9.0|2.10.0|minor
sagemaker-train|1.9.0|1.10.0|minor
sagemaker-serve|1.9.0|1.10.0|minor
sagemaker-mlops|1.7.1|1.10.0|minor
libsqlite|3.53.0|3.53.1|patch
optree|0.19.0|0.19.1|patch
pydantic-core|2.46.3|2.46.4|patch
pydantic|2.13.3|2.13.4|patch
parso|0.8.6|0.8.7|patch
mistune|3.2.0|3.2.1|patch
apsw|3.53.0.0|3.53.1.0|patch
fastcore|1.12.43|1.12.44|patch
authlib|1.7.0|1.7.2|patch
lcms2|2.19|2.19.1|patch
virtualenv|21.3.0|21.3.1|patch
typer|0.25.0|0.25.1|patch
conda-libmamba-solver|26.4.0|26.4.1|patch
cyclopts|4.11.0|4.11.2|patch
joserfc|1.6.4|1.6.5|patch
sse-starlette|3.4.1|3.4.2|patch
uncalled-for|0.3.1|0.3.2|patch
gitpython|3.1.48|3.1.50|patch
jupyter-ai-router|0.0.4|0.0.5|patch
jupyter_server_documents|0.2.0|0.2.1|patch
jupyterlab-commands-toolkit|0.1.5|0.1.6|patch
onnxruntime|1.24.2|1.24.4|patch
pymysql|1.1.2|1.1.3|patch

### Removed

Package | Last Version
---|---
humanfriendly|10.0
coloredlogs|15.0.1
