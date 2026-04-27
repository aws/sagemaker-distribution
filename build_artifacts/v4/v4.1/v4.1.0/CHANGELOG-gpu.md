# Change log: 4.1.0 (gpu)

This page lists all package changes since the previous release (4.0.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyter-ai|2.31.7|3.0.0|major
altair|6.0.0|6.1.0|minor
sagemaker-jupyterlab-extension-common|0.3.3|0.4.2|minor
uvicorn|0.44.0|0.46.0|minor
fastapi|0.135.3|0.136.1|minor
sagemaker-mlflow|0.2.0|0.3.0|minor
boto3|1.42.70|1.42.91|patch
amazon_sagemaker_sql_editor|0.2.1|0.2.4|patch
amzn-sagemaker-aiops-jupyterlab-extension|1.0.5|1.0.6|patch
matplotlib-base|3.10.8|3.10.9|patch
conda|26.3.1|26.3.2|patch
docker-cli|29.4.0|29.4.1|patch
sagemaker-code-editor|1.9.4|1.9.5|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.15|1.0.16|patch
sagemaker-jupyterlab-extension|0.5.4|0.5.7|patch
sagemaker-studio|1.1.8|1.1.14|patch
sagemaker-studio-dataengineering-extensions|1.3.8|1.3.9|patch
sagemaker-studio-dataengineering-sessions|1.3.18|1.3.19|patch
uv|0.11.4|0.11.7|patch

### Removed

Package | Last Version
---|---
amazon-sagemaker-jupyter-ai-q-developer|1.2.9

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
importlib_resources|6.5.2|7.1.0|major
cryptography|44.0.3|46.0.7|major
pyopenssl|24.3.0|25.3.0|major
gdown|5.2.1|6.0.0|major
libsqlite|3.52.0|3.53.0|minor
ca-certificates|2026.2.25|2026.4.22|minor
filelock|3.25.2|3.29.0|minor
certifi|2026.2.25|2026.4.22|minor
idna|3.11|3.13|minor
nccl|2.29.3.1|2.30.3.1|minor
python-tzdata|2026.1|2026.2|minor
pydantic-core|2.41.5|2.46.3|minor
pydantic|2.12.5|2.13.3|minor
aiobotocore|3.3.0|3.5.0|minor
greenlet|3.3.2|3.4.0|minor
narwhals|2.19.0|2.20.0|minor
prometheus_client|0.24.1|0.25.0|minor
snowflake-connector-python|3.13.2|3.17.4|minor
apsw|3.52.0.0|3.53.0.0|minor
lcms2|2.18|2.19|minor
opentelemetry-api|1.40.0|1.41.0|minor
opentelemetry-sdk|1.40.0|1.41.0|minor
opentelemetry-proto|1.40.0|1.41.1|minor
smart_open|7.5.1|7.6.0|minor
wheel|0.46.3|0.47.0|minor
typer|0.24.1|0.25.0|minor
smart-open|7.5.1|7.6.0|minor
awswrangler|3.15.1|3.16.0|minor
pathspec|1.0.4|1.1.1|minor
conda-libmamba-solver|26.3.0|26.4.0|minor
databricks-sdk|0.102.0|0.105.0|minor
deltalake|1.3.2|1.5.0|minor
dnspython|2.7.0|2.8.0|minor
uvicorn-standard|0.44.0|0.46.0|minor
fastapi-core|0.135.3|0.136.1|minor
pydantic-settings|2.13.1|2.14.0|minor
sse-starlette|3.3.4|3.4.1|minor
skops|0.13.0|0.14|minor
sagemaker-core|2.7.1|2.9.0|minor
sagemaker-train|1.7.1|1.9.0|minor
sagemaker-serve|1.7.1|1.9.0|minor
llvm-openmp|22.1.2|22.1.4|patch
liblzma|5.8.2|5.8.3|patch
libpng|1.6.56|1.6.58|patch
libjpeg-turbo|3.1.2|3.1.4.1|patch
botocore|1.42.70|1.42.91|patch
zipp|3.23.0|3.23.1|patch
mako|1.3.10|1.3.11|patch
s3transfer|0.16.0|0.16.1|patch
platformdirs|4.9.4|4.9.6|patch
jupyter_events|0.12.0|0.12.1|patch
fastcore|1.12.34|1.12.43|patch
fonttools|4.62.0|4.62.1|patch
matplotlib|3.10.8|3.10.9|patch
google-auth|2.49.1|2.49.2|patch
virtualenv|21.2.0|21.2.4|patch
rich|14.3.3|14.3.4|patch
python-multipart|0.0.24|0.0.26|patch
python-fasthtml|0.13.3|0.13.4|patch
numba|0.65.0|0.65.1|patch
libsolv|0.7.36|0.7.37|patch
reproc|14.2.5.post0|14.2.7.post0|patch
reproc-cpp|14.2.5.post0|14.2.7.post0|patch
python-duckdb|1.5.1|1.5.2|patch
duckdb|1.5.1|1.5.2|patch
gitpython|3.1.46|3.1.47|patch
jupyter_ydoc|3.4.0|3.4.1|patch
langsmith|0.7.26|0.7.37|patch
param|2.3.2|2.3.3|patch
opentelemetry-semantic-conventions|0.61b0|0.62b0|
opentelemetry-exporter-prometheus|0.61b0|0.62b0|
opentelemetry-instrumentation|0.61b0|0.62b0|
opentelemetry-instrumentation-threading|0.61b0|0.62b0|

### New

Package | Version
---|---
onemkl-license|2025.3.1
agent-client-protocol|0.9.0
caio|0.9.25
aiofile|3.9.0
authlib|1.7.0
backports|1.0
backports.tarfile|1.2.0
docutils|0.22.4
rich-rst|1.3.2
cyclopts|4.11.0
fastar|0.11.0
griffelib|2.0.2
joserfc|1.6.4
jsonref|1.1.0
pathable|0.5.0
jsonschema-path|0.4.5
more-itertools|11.0.2
jaraco.classes|3.4.0
jaraco.context|6.1.2
jaraco.functools|4.4.0
jeepney|0.9.0
secretstorage|3.4.1
keyring|25.7.0
openapi-pydantic|0.5.1
py-key-value-aio|0.4.4
xorg-libxt|1.3.1
xorg-libxmu|1.3.1
xclip|0.13
xsel|1.2.1
pyperclip|1.11.0
uncalled-for|0.3.1
fastmcp|3.2.4
jupyter_server_documents|0.2.0
jupyterlab-chat|0.21.1
jupyter-ai-router|0.0.4
jupyter-ai-persona-manager|0.0.11
jupyter-ai-acp-client|0.1.3
jupyter-ai-chat-commands|0.0.4
jupyter-ai-tools|0.5.1
jupyter-server-mcp|0.1.2
jupyterlab-eventlistener|0.4.0
jupyterlab-commands-toolkit|0.1.5
jupyterlab-notebook-awareness|0.2.0
opensearch-py|2.5.0
sqlglot|28.10.1

### Removed

Package | Last Version
---|---
libfaiss|1.10.0
faiss|1.10.0
faiss-cpu|1.10.0
locket|1.0.0
partd|1.4.2
dask-core|2026.3.0
deepmerge|2.0
cytoolz|1.1.0
zict|3.0.0
distributed|2026.3.0
ply|3.11
jsonpath-ng|1.8.0
marshmallow|3.26.1
typing_inspect|0.9.0
dataclasses-json|0.6.7
langchain-community|0.3.31
jupyter-ai-magics|2.31.7
