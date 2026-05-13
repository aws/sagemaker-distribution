# Change log: 4.2.0 (gpu)

This page lists all package changes since the previous release (4.1.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
boto3|1.42.97|1.43.0|minor
pip|26.0.1|26.1.1|minor
jupyter-collaboration|4.3.0|4.4.0|minor
mlflow|3.11.1|3.12.0|minor
s3fs|2026.3.0|2026.4.0|minor
sagemaker-mlflow|0.3.0|0.4.0|minor
sagemaker-python-sdk|3.7.1|3.10.1|minor
docker-cli|29.4.2|29.4.3|patch
keras|3.14.0|3.14.1|patch
sagemaker-studio|1.1.14|1.1.15|patch
uv|0.11.10|0.11.14|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
rdma-core|62.0|63.0|major
starlette|1.0.0|0.52.1|major
paramiko|4.0.0|5.0.0|major
fsspec|2026.3.0|2026.4.0|minor
requests|2.33.1|2.34.0|minor
botocore|1.42.97|1.43.0|minor
aiobotocore|3.6.0|3.7.0|minor
narwhals|2.20.0|2.21.0|minor
s3transfer|0.16.1|0.17.0|minor
tomlkit|0.14.0|0.15.0|minor
google-auth|2.50.0|2.52.0|minor
googleapis-common-protos|1.74.0|1.75.0|minor
proto-plus|1.27.2|1.28.0|minor
markdown-it-py|4.0.0|4.2.0|minor
regex|2026.4.4|2026.5.9|minor
python-fasthtml|0.13.4|0.12.50|minor
coverage|7.13.5|7.14.0|minor
docstring_parser|0.17.0|0.18.0|minor
databricks-sdk|0.106.0|0.108.0|minor
jupyter-collaboration-ui|2.3.0|2.4.0|minor
jupyter-docprovider|2.3.0|2.4.0|minor
jupyter_server_ydoc|2.3.0|2.4.0|minor
uuid-utils|0.14.1|0.15.0|minor
mdit-py-plugins|0.5.0|0.6.0|minor
mlflow-skinny|3.11.1|3.12.0|minor
mlflow-ui|3.11.1|3.12.0|minor
onnxruntime|1.24.4|1.25.1|minor
sqlalchemy-bigquery|1.16.0|1.17.0|minor
llvm-openmp|22.1.4|22.1.5|patch
pydantic-core|2.46.3|2.46.4|patch
pydantic|2.13.3|2.13.4|patch
matplotlib-inline|0.2.1|0.2.2|patch
fastcore|1.12.44|1.12.47|patch
smart_open|7.6.0|7.6.1|patch
virtualenv|21.3.1|21.3.2|patch
python-multipart|0.0.27|0.0.28|patch
fastprogress|1.1.3|1.1.6|patch
smart-open|7.6.0|7.6.1|patch
rich-toolkit|0.19.7|0.19.8|patch
pydantic-settings|2.14.0|2.14.1|patch
sse-starlette|3.4.1|3.4.4|patch
uncalled-for|0.3.1|0.3.2|patch
langsmith|0.8.1|0.8.3|patch
sagemaker-core|2.10.0|2.10.1|patch
sagemaker-train|1.10.0|1.10.1|patch
sagemaker-serve|1.10.0|1.10.1|patch
sagemaker-mlops|1.10.0|1.10.1|patch
