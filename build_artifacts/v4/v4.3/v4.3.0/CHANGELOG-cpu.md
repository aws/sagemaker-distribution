# Change log: 4.3.0 (cpu)

This page lists all package changes since the previous release (4.2.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
altair|6.1.0|6.2.1|minor
uvicorn|0.48.0|0.49.0|minor
fastapi|0.136.3|0.137.1|minor
mlflow|3.12.0|3.13.0|minor
jupyterlab|4.5.7|4.5.8|patch
amazon_sagemaker_sql_editor|0.2.4|0.2.5|patch
pip|26.1.1|26.1.2|patch
notebook|7.5.6|7.5.7|patch
conda|26.5.0|26.5.2|patch
docker-cli|29.5.2|29.5.3|patch
mcp|1.27.1|1.27.2|patch
sagemaker-studio|1.1.20|1.1.22|patch
uv|0.11.16|0.11.21|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python-json-logger|3.2.1|4.1.0|major
datasets|2.2.1|5.0.0|major
tqdm|4.67.3|4.68.2|minor
safetensors|0.7.0|0.8.0|minor
accelerate|1.13.0|1.14.0|minor
propcache|0.3.1|0.5.2|minor
aiohttp|3.13.5|3.14.1|minor
aiofile|3.9.0|3.11.1|minor
narwhals|2.21.2|2.22.1|minor
jupyter_client|8.8.0|8.9.1|minor
beautifulsoup4|4.14.3|4.15.0|minor
bleach|6.3.0|6.4.0|minor
bleach-with-css|6.3.0|6.4.0|minor
nbclient|0.10.4|0.11.0|minor
jupyter_server|2.18.2|2.19.0|minor
pandoc|3.9.0.2|3.10|minor
wcwidth|0.7.0|0.8.1|minor
ipykernel|7.2.0|7.3.0|minor
pyathena|3.31.0|3.32.0|minor
joserfc|1.6.8|1.7.1|minor
google-auth|2.53.0|2.54.0|minor
virtualenv|21.4.1|21.5.0|minor
gdown|6.0.0|6.1.0|minor
ujson|5.12.1|5.13.0|minor
optuna|4.8.0|4.9.0|minor
conda-package-streaming|0.12.0|0.13.0|minor
conda-package-handling|2.4.0|2.5.0|minor
conda-pypi|0.9.0|0.10.1|minor
py-rattler|0.23.2|0.25.0|minor
menuinst|2.4.2|2.5.0|minor
cyclopts|4.16.1|4.18.0|minor
databricks-sdk|0.112.0|0.117.0|minor
rich-toolkit|0.19.10|0.20.1|minor
uvicorn-standard|0.48.0|0.49.0|minor
fastapi-core|0.136.3|0.137.1|minor
fastmcp-slim|3.3.1|3.4.2|minor
secretstorage|3.4.1|3.5.0|minor
fastmcp|3.3.1|3.4.2|minor
tiktoken|0.12.0|0.13.0|minor
mlflow-skinny|3.12.0|3.13.0|minor
mlflow-ui|3.12.0|3.13.0|minor
sagemaker-core|2.12.0|2.13.1|minor
sagemaker-train|1.12.0|1.13.1|minor
llvm-openmp|22.1.6|22.1.7|patch
libsqlite|3.53.1|3.53.2|patch
openssl|3.6.2|3.6.3|patch
filelock|3.29.0|3.29.4|patch
fontconfig|2.18.0|2.18.1|patch
graphite2|1.3.14|1.3.15|patch
sqlalchemy|2.0.50|2.0.51|patch
alsa-lib|1.2.15.3|1.2.16.1|patch
traitlets|5.15.0|5.15.1|patch
tornado|6.5.6|6.5.7|patch
debugpy|1.8.20|1.8.21|patch
apsw|3.53.1.0|3.53.2.0|patch
fastcore|1.13.2|1.13.3|patch
arro3-core|0.8.0|0.8.1|patch
distlib|0.4.0|0.4.3|patch
python-discovery|1.4.0|1.4.2|patch
pytorch-lightning|2.6.1|2.6.5|patch
charls|2.4.3|2.4.4|patch
python-multipart|0.0.29|0.0.32|patch
typer|0.26.2|0.26.7|patch
ocl-icd|2.3.3|2.3.4|patch
bokeh|3.9.0|3.9.1|patch
libsolv|0.7.38|0.7.39|patch
conda-rattler-solver|0.1.0|0.1.1|patch
fastapi-cli|0.0.23|0.0.24|patch
pydantic-extra-types|2.11.2|2.11.1|patch
flask-cors|6.0.2|6.0.5|patch
graphql-core|3.2.8|3.2.11|patch
jupyter-collaboration-ui|2.4.0|2.4.1|patch
jupyter-docprovider|2.4.0|2.4.1|patch
jupyterlab-chat|0.22.0|0.22.1|patch
jupyter-ai-tools|0.5.1|0.5.2|patch
jupyter_server_documents|0.2.1|0.2.4|patch
langsmith|0.8.6|0.8.15|patch
panel-material-ui|0.11.0|0.11.2|patch
panel|1.9.1|1.9.3|patch
snowballstemmer|3.1.0|3.1.1|patch
pylint|4.0.5|4.0.6|patch
snowflake-sqlalchemy|1.10.0|1.10.1|patch

### New

Package | Version
---|---
nest-asyncio2|1.7.2
backports.zstd|1.6.0
tomli-w|1.2.0
oracledb|3.4.2
panel-core|1.9.3

### Removed

Package | Last Version
---|---
dataclasses|0.8
