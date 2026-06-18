# Change log: 4.0.5 (cpu)

This page lists all package changes since the previous release (4.0.4).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.7|4.5.8|patch
amazon_sagemaker_sql_editor|0.2.4|0.2.5|patch
notebook|7.5.6|7.5.7|patch
mcp|1.27.1|1.27.2|patch
sagemaker-jupyterlab-extension|0.5.7|0.5.9|patch
sagemaker-studio|1.1.19|1.1.22|patch
uv|0.11.15|0.11.21|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python-json-logger|3.2.1|4.1.0|major
datasets|2.2.1|5.0.0|major
idna|3.15|3.17|minor
tqdm|4.67.3|4.68.2|minor
libuv|1.51.0|1.52.1|minor
safetensors|0.7.0|0.8.0|minor
fontconfig|2.17.1|2.18.1|minor
frozenlist|1.7.0|1.8.0|minor
propcache|0.3.1|0.5.2|minor
aiohttp|3.13.5|3.14.1|minor
narwhals|2.21.2|2.22.1|minor
wcwidth|0.7.0|0.8.1|minor
python-xxhash|3.6.0|3.7.0|minor
platformdirs|4.9.6|4.10.0|minor
jupyter_client|8.8.0|8.9.1|minor
beautifulsoup4|4.14.3|4.15.0|minor
bleach|6.3.0|6.4.0|minor
bleach-with-css|6.3.0|6.4.0|minor
nbclient|0.10.4|0.11.0|minor
jupyter_server|2.18.2|2.19.0|minor
ipykernel|7.2.0|7.3.0|minor
pyjwt|2.12.1|2.13.0|minor
pandoc|3.9.0.2|3.10|minor
pyathena|3.30.1|3.32.0|minor
google-api-core|2.30.3|2.29.0|minor
opentelemetry-api|1.41.0|1.42.1|minor
opentelemetry-sdk|1.41.0|1.42.1|minor
python-discovery|1.3.1|1.4.0|minor
virtualenv|21.3.3|21.4.2|minor
gdown|6.0.0|6.1.0|minor
starlette|1.0.0|1.3.0|minor
typer|0.25.1|0.26.7|minor
libboost|1.88.0|1.90.0|minor
optuna|4.8.0|4.9.0|minor
black|26.3.1|26.5.1|minor
conda-package-handling|2.4.0|2.5.0|minor
menuinst|2.4.2|2.5.0|minor
databricks-sdk|0.110.0|0.116.0|minor
rich-toolkit|0.19.10|0.20.1|minor
httptools|0.7.1|0.8.0|minor
google-cloud-bigquery-core|3.18.0|3.41.0|minor
jiter|0.13.0|0.15.0|minor
pycrdt|0.12.50|0.13.1|minor
jupyter_ydoc|3.4.1|3.5.0|minor
tiktoken|0.12.0|0.13.0|minor
snowballstemmer|3.0.1|3.1.1|minor
sagemaker-core|2.12.0|2.13.1|minor
sagemaker-train|1.12.0|1.13.1|minor
sqlalchemy-bigquery|1.16.0|1.17.0|minor
llvm-openmp|22.1.6|22.1.7|patch
libsqlite|3.53.1|3.53.2|patch
openssl|3.6.2|3.6.3|patch
filelock|3.29.0|3.29.3|patch
graphite2|1.3.14|1.3.15|patch
sqlalchemy|2.0.49|2.0.50|patch
alsa-lib|1.2.15.3|1.2.16|patch
traitlets|5.15.0|5.15.1|patch
tornado|6.5.5|6.5.7|patch
langsmith|0.8.5|0.8.14|patch
soupsieve|2.8.3|2.8.4|patch
debugpy|1.8.20|1.8.21|patch
apsw|3.53.1.0|3.53.2.0|patch
fastcore|1.13.2|1.13.3|patch
distlib|0.4.0|0.4.2|patch
pytorch-lightning|2.6.1|2.6.5|patch
charls|2.4.3|2.4.4|patch
libavif16|1.4.1|1.4.2|patch
python-multipart|0.0.29|0.0.32|patch
python-fasthtml|0.14.1|0.14.2|patch
ujson|5.12.0|5.12.1|patch
ocl-icd|2.3.3|2.3.4|patch
bokeh|3.9.0|3.9.1|patch
libsolv|0.7.37|0.7.39|patch
coverage|7.14.0|7.14.1|patch
fastapi-cli|0.0.23|0.0.24|patch
pydantic-extra-types|2.11.2|2.11.1|patch
flask-cors|6.0.2|6.0.5|patch
graphql-core|3.2.8|3.2.11|patch
jupyter-collaboration-ui|2.4.0|2.4.1|patch
jupyter-docprovider|2.4.0|2.4.1|patch
pycrdt-store|0.1.3|0.1.4|patch
pycrdt-websocket|0.16.0|0.16.2|patch
jupyter_server_ydoc|2.4.0|2.4.1|patch
panel-material-ui|0.11.0|0.11.2|patch
panel|1.9.0|1.9.3|patch
opentelemetry-semantic-conventions|0.62b0|0.63b1|
opentelemetry-exporter-prometheus|0.62b0|0.63b1|
opentelemetry-instrumentation|0.62b0|0.63b1|
opentelemetry-instrumentation-threading|0.62b0|0.63b1|

### New

Package | Version
---|---
nest-asyncio2|1.7.2
tomli-w|1.2.0
google-api-core-grpc|2.29.0
lz4|4.4.5
oracledb|3.4.2
panel-core|1.9.3
tzlocal|5.3.1
trino-python-client|0.337.0

### Removed

Package | Last Version
---|---
dataclasses|0.8
