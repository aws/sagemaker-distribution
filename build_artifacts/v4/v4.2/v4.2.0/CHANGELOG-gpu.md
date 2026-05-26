# Change log: 4.2.0 (gpu)

This page lists all package changes since the previous release (4.1.2).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
boto3|1.42.97|1.43.0|minor
pip|26.0.1|26.1.1|minor
uvicorn|0.46.0|0.48.0|minor
conda|26.3.2|26.5.0|minor
docker-cli|29.4.3|29.5.2|minor
jupyter-collaboration|4.3.0|4.4.0|minor
jupyterlab-git|0.52.0|0.53.0|minor
mlflow|3.11.1|3.12.0|minor
s3fs|2026.3.0|2026.4.0|minor
sagemaker-mlflow|0.3.0|0.4.0|minor
sagemaker-python-sdk|3.7.1|3.12.0|minor
sagemaker-jupyterlab-extension-common|0.4.2|0.4.5|patch
amazon-sagemaker-jupyter-scheduler|3.2.0|3.2.2|patch
fastapi|0.136.1|0.136.3|patch
mcp|1.27.0|1.27.1|patch
sagemaker-jupyterlab-extension|0.5.7|0.5.9|patch
sagemaker-studio|1.1.15|1.1.19|patch
sagemaker-studio-dataengineering-sessions|1.3.20|1.3.21|patch
uv|0.11.13|0.11.16|patch

### Removed

Package | Last Version
---|---
amazon-q-developer-jupyterlab-ext|3.4.8

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
zipp|3.23.1|4.1.0|major
pycparser|2.22|3.0|major
starlette|1.0.0|0.52.1|major
rich-rst|1.3.2|2.0.1|major
ca-certificates|2026.4.22|2026.5.20|minor
fsspec|2026.3.0|2026.4.0|minor
certifi|2026.4.22|2026.5.20|minor
idna|3.13|3.15|minor
libuv|1.51.0|1.52.1|minor
fontconfig|2.17.1|2.18.0|minor
yarl|1.23.0|1.24.2|minor
botocore|1.42.97|1.43.0|minor
decorator|5.2.1|5.3.1|minor
s3transfer|0.16.1|0.17.0|minor
pyjwt|2.12.1|2.13.0|minor
pyathena|3.30.1|3.31.0|minor
fastcore|1.12.47|1.13.2|minor
fonttools|4.62.1|4.63.0|minor
libpciaccess|0.18|0.19|minor
google-auth|2.52.0|2.53.0|minor
opentelemetry-api|1.41.0|1.42.1|minor
opentelemetry-sdk|1.41.0|1.42.1|minor
opentelemetry-proto|1.41.1|1.42.1|minor
python-fasthtml|0.14.1|0.12.50|minor
libboost|1.88.0|1.90.0|minor
black|26.3.1|26.5.1|minor
docstring_parser|0.17.0|0.18.0|minor
cyclopts|4.11.2|4.15.0|minor
databricks-sdk|0.108.0|0.111.0|minor
deepdiff|9.0.0|9.1.0|minor
httptools|0.7.1|0.8.0|minor
watchfiles|1.1.1|1.2.0|minor
uvicorn-standard|0.46.0|0.48.0|minor
pathable|0.5.0|0.6.0|minor
jsonschema-path|0.4.6|0.5.0|minor
more-itertools|11.0.2|11.1.0|minor
jaraco.functools|4.4.0|4.5.0|minor
fastmcp|3.2.4|3.3.1|minor
jupyterlab-chat|0.21.1|0.22.0|minor
uuid-utils|0.15.0|0.16.0|minor
mlflow-skinny|3.11.1|3.12.0|minor
mlflow-ui|3.11.1|3.12.0|minor
onnxruntime|1.25.1|1.26.0|minor
param|2.3.3|2.4.0|minor
panel|1.8.10|1.9.1|minor
snowballstemmer|3.0.1|3.1.0|minor
pymysql|1.1.3|1.2.0|minor
sagemaker-core|2.10.1|2.12.0|minor
sagemaker-train|1.10.1|1.12.0|minor
sagemaker-serve|1.10.1|1.12.0|minor
sagemaker-mlops|1.10.1|1.12.0|minor
snowflake-sqlalchemy|1.9.0|1.10.0|minor
slack-sdk|3.41.0|3.42.0|minor
llvm-openmp|22.1.5|22.1.6|patch
libexpat|2.8.0|2.8.1|patch
libuuid|2.42|2.42.1|patch
requests|2.34.0|2.34.2|patch
libcublas|12.9.1.4|12.9.2.10|patch
aiohappyeyeballs|2.6.1|2.6.2|patch
greenlet|3.5.0|3.5.1|patch
sqlalchemy|2.0.49|2.0.50|patch
narwhals|2.21.0|2.21.2|patch
soupsieve|2.8.3|2.8.4|patch
xorg-libxi|1.8.2|1.8.3|patch
joserfc|1.6.5|1.6.7|patch
libdrm|2.4.125|2.4.127|patch
python-discovery|1.3.0|1.3.1|patch
virtualenv|21.3.1|21.3.3|patch
python-multipart|0.0.28|0.0.29|patch
ujson|5.12.0|5.12.1|patch
orjson|3.11.8|3.11.9|patch
awswrangler|3.16.0|3.16.1|patch
conda-libmamba-solver|26.4.1|26.4.2|patch
python-duckdb|1.5.2|1.5.3|patch
duckdb|1.5.2|1.5.3|patch
rich-toolkit|0.19.8|0.19.10|patch
fastapi-core|0.136.1|0.136.3|patch
sse-starlette|3.4.3|3.4.4|patch
jupyter-ai-acp-client|0.1.3|0.1.5|patch
langsmith|0.8.3|0.8.5|patch
mdit-py-plugins|0.6.0|0.6.1|patch
opentelemetry-semantic-conventions|0.62b0|0.63b1|
opentelemetry-exporter-prometheus|0.62b0|0.63b1|
opentelemetry-instrumentation|0.62b0|0.63b1|
opentelemetry-instrumentation-threading|0.62b0|0.63b1|

### New

Package | Version
---|---
cachebox|5.2.3
conda-lockfiles|0.2.0
conda-index|0.11.0
pyproject_hooks|1.2.0
python-build|1.5.0
python-installer|1.0.1
unearth|0.18.2
conda-pypi|0.9.0
py-rattler|0.23.2
conda-rattler-solver|0.1.0
conda-self|0.2.0
fastmcp-slim|3.3.1
jupyterlab-git-core|0.53.0
nh3|0.3.5
panel-material-ui|0.11.0
vertica-python|1.4.0

### Removed

Package | Last Version
---|---
docutils|0.22.4
