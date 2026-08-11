# Change log: 4.4.0 (gpu)

This page lists all package changes since the previous release (4.3.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension-common|0.4.7|0.5.1|minor
pip|26.1.2|26.2.1|minor
uvicorn|0.51.0|0.52.1|minor
conda|26.5.3|26.7.0|minor
docker-cli|29.6.2|29.7.1|minor
fastapi|0.139.2|0.141.1|minor
jupyter-ai|3.0.1|3.1.2|minor
mlflow|3.13.0|3.15.1|minor
python-lsp-server|1.14.0|1.15.0|minor
sagemaker-jupyterlab-emr-extension|0.4.3|0.5.0|minor
sagemaker-jupyterlab-extension|0.5.10|0.6.1|minor
uv|0.11.30|0.12.3|minor
jupyter-scheduler|2.12.0|2.12.1|patch
jupyter-collaboration|4.4.0|4.4.2|patch
jupyterlab-git|0.54.0|0.54.1|patch
keras|3.15.0|3.15.1|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.18|1.0.19|patch
sagemaker-studio|1.1.26|1.1.29|patch
sagemaker-studio-dataengineering-extensions|1.3.12|1.3.13|patch
sagemaker-studio-dataengineering-sessions|1.3.21|1.3.23|patch

### New

Package | Version
---|---
extension-ray-jupyterlab-sagemaker-ai|0.1.1
toolkit-for-ray-on-sagemaker-ai|1.0.3

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libgcc|15.2.0|16.1.0|major
libstdcxx|15.2.0|16.1.0|major
libgcc-ng|15.2.0|16.1.0|major
libstdcxx-ng|15.2.0|16.1.0|major
psutil|5.9.8|7.1.3|major
setuptools|83.0.0|84.0.0|major
libgfortran5|15.2.0|16.1.0|major
libgfortran|15.2.0|16.1.0|major
datasets|2.2.1|5.0.1|major
starlette|0.52.1|1.6.0|major
websockets|16.1.1|17.0.1|major
gunicorn|23.0.0|26.0.0|major
huey|2.6.0|3.3.4|major
sqlglot|28.10.1|30.15.0|major
ca-certificates|2026.6.17|2026.7.22|minor
certifi|2026.6.17|2026.7.22|minor
tqdm|4.69.0|4.70.0|minor
lerc|4.1.0|4.2.0|minor
annotated-types|0.7.0|0.8.0|minor
agent-client-protocol|0.9.0|0.11.1|minor
caio|0.9.25|0.12.2|minor
aiofile|3.11.1|3.12.3|minor
mako|1.3.12|1.4.1|minor
alembic|1.18.5|1.19.1|minor
traitlets|5.15.1|5.16.1|minor
python-fastjsonschema|2.21.2|2.22.1|minor
nbformat|5.10.4|5.11.0|minor
prometheus_client|0.25.0|0.26.0|minor
h2|4.3.0|4.4.1|minor
jedi|0.19.2|0.20.0|minor
nspr|4.38|4.40|minor
fastcore|2.1.4|2.2.10|minor
python-fasthtml|0.12.50|0.14.11|minor
boltons|26.0.0|26.1.0|minor
databricks-sdk|0.122.0|0.125.0|minor
uvicorn-standard|0.51.0|0.52.1|minor
fastapi-core|0.139.2|0.141.1|minor
pydantic-settings|2.14.2|2.15.0|minor
uncalled-for|0.3.2|0.4.0|minor
google-cloud-bigquery-core|3.42.2|3.43.0|minor
pycrdt|0.12.50|0.13.1|minor
jupyter_ydoc|3.4.1|3.5.0|minor
jupyterlab-chat|0.22.1|0.23.1|minor
jupyter-ai-persona-manager|0.0.12|0.1.2|minor
jupyter-ai-acp-client|0.1.5|0.2.1|minor
jupyter-ai-tools|0.5.2|0.6.1|minor
jupyter_server_documents|0.2.5|0.3.3|minor
mlflow-skinny|3.13.0|3.15.1|minor
mlflow-ui|3.13.0|3.15.1|minor
onnxruntime|1.26.0|1.28.0|minor
python-lsp-server-base|1.14.0|1.15.0|minor
sagemaker-core|2.16.0|2.18.0|minor
libsqlite|3.53.3|3.53.4|patch
libxcrypt|4.4.36|4.4.38|patch
filelock|3.32.0|3.32.2|patch
gflags|2.3.0|2.3.1|patch
fontconfig|2.18.1|2.18.3|patch
typing-inspection|0.4.2|0.4.3|patch
aiohttp|3.14.2|3.14.3|patch
greenlet|3.5.3|3.5.5|patch
platformdirs|4.11.0|4.11.2|patch
tornado|6.5.7|6.5.8|patch
soupsieve|2.9.1|2.9.2|patch
mistune|3.3.3|3.3.4|patch
pandoc|3.10|3.10.1|patch
jupyter_scheduler|2.12.0|2.12.1|patch
prompt-toolkit|3.0.52|3.0.53|patch
s3transfer|0.19.1|0.19.2|patch
pyathena|3.35.2|3.35.4|patch
scramp|1.4.12|1.4.17|patch
annotated-doc|0.0.4|0.0.5|patch
google-auth|2.56.0|2.56.3|patch
proto-plus|1.28.1|1.28.2|patch
python-discovery|1.5.0|1.5.1|patch
virtualenv|21.7.0|21.7.3|patch
omegaconf|2.3.0|2.3.1|patch
markdown|3.10.2|3.10.3|patch
typer|0.27.0|0.27.1|patch
prompt_toolkit|3.0.52|3.0.53|patch
awswrangler|3.17.0|3.17.1|patch
bokeh|3.9.1|3.9.2|patch
conda-self|0.2.0|0.2.1|patch
coverage|7.15.2|7.15.4|patch
cyclopts|4.22.0|4.22.5|patch
fastmcp-slim|3.4.4|3.4.6|patch
sse-starlette|3.4.6|3.4.8|patch
fastmcp|3.4.4|3.4.6|patch
gitpython|3.1.53|3.1.58|patch
jupyter-collaboration-ui|2.4.1|2.4.2|patch
jupyter-docprovider|2.4.1|2.4.2|patch
pycrdt-store|0.1.3|0.1.4|patch
pycrdt-websocket|0.16.0|0.16.2|patch
jupyter_server_ydoc|2.4.0|2.4.2|patch
jupyter-ai-router|0.0.5|0.0.7|patch
jupyterlab-git-core|0.54.0|0.54.1|patch
langsmith|0.10.9|0.10.17|patch
panel-material-ui|0.14.0|0.14.1|patch
pylint|4.0.6|4.0.7|patch
sqlalchemy-bigquery|1.17.0|1.17.2|patch

### New

Package | Version
---|---
httpcore2|2.5.0
httpx2|2.5.0

### Removed

Package | Last Version
---|---
apsw|3.53.3.1
apswutils|0.1.2
dataclasses|0.8
fastlite|0.2.3
querystring_parser|1.2.4
