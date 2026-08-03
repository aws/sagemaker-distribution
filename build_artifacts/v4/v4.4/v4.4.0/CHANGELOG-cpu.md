# Change log: 4.4.0 (cpu)

This page lists all package changes since the previous release (4.3.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
pip|26.1.2|26.2|minor
uvicorn|0.51.0|0.52.1|minor
docker-cli|29.6.2|29.7.1|minor
fastapi|0.139.2|0.141.1|minor
jupyter-ai|3.0.1|3.1.2|minor
mlflow|3.13.0|3.14.0|minor
python-lsp-server|1.14.0|1.15.0|minor
uv|0.11.30|0.12.1|minor
jupyter-collaboration|4.4.0|4.4.1|patch
keras|3.15.0|3.15.1|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.18|1.0.19|patch
sagemaker-studio|1.1.26|1.1.28|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libgcc|15.2.0|16.1.0|major
libgcc-ng|15.2.0|16.1.0|major
libstdcxx|15.2.0|16.1.0|major
libstdcxx-ng|15.2.0|16.1.0|major
harfbuzz|12.2.0|11.0.0|major
libgfortran5|15.2.0|16.1.0|major
libgfortran|15.2.0|16.1.0|major
datasets|2.2.1|5.0.1|major
graphviz|13.1.2|12.2.1|major
starlette|0.52.1|1.3.1|major
websockets|16.1.1|17.0.1|major
gunicorn|23.0.0|26.0.0|major
huey|2.6.0|3.3.2|major
sqlglot|28.10.1|30.14.0|major
ca-certificates|2026.6.17|2026.7.22|minor
certifi|2026.6.17|2026.7.22|minor
tqdm|4.69.0|4.70.0|minor
pcre2|10.46|10.44|minor
libglib|2.86.2|2.84.0|minor
lerc|4.1.0|4.2.0|minor
gdk-pixbuf|2.44.4|2.42.12|minor
annotated-types|0.7.0|0.8.0|minor
agent-client-protocol|0.9.0|0.11.1|minor
traitlets|5.15.1|5.16.0|minor
python-fastjsonschema|2.21.2|2.22.1|minor
prometheus_client|0.25.0|0.26.0|minor
h2|4.3.0|4.4.0|minor
jedi|0.19.2|0.20.0|minor
dbus|1.16.2|1.13.6|minor
qt6-main|6.9.2|6.8.3|minor
pyside6|6.9.2|6.8.3|minor
glib-tools|2.86.2|2.84.0|minor
python-fasthtml|0.12.50|0.14.11|minor
boltons|26.0.0|26.1.0|minor
databricks-sdk|0.122.0|0.123.0|minor
uvicorn-standard|0.51.0|0.52.1|minor
fastapi-core|0.139.2|0.141.1|minor
pycrdt|0.12.50|0.13.1|minor
jupyter_ydoc|3.4.1|3.5.0|minor
jupyterlab-chat|0.22.1|0.23.1|minor
jupyter-ai-persona-manager|0.0.12|0.1.2|minor
jupyter-ai-acp-client|0.1.5|0.2.1|minor
jupyter-ai-tools|0.5.2|0.6.1|minor
jupyter_server_documents|0.2.5|0.3.2|minor
mlflow-skinny|3.13.0|3.14.0|minor
mlflow-ui|3.13.0|3.14.0|minor
python-lsp-server-base|1.14.0|1.15.0|minor
sagemaker-core|2.16.0|2.18.0|minor
libsqlite|3.53.3|3.53.4|patch
filelock|3.32.0|3.32.2|patch
gflags|2.3.0|2.3.1|patch
fontconfig|2.18.1|2.18.2|patch
pango|1.56.4|1.56.3|patch
aiohttp|3.14.2|3.14.3|patch
greenlet|3.5.3|3.5.4|patch
mistune|3.3.3|3.3.4|patch
pandoc|3.10|3.10.1|patch
prompt-toolkit|3.0.52|3.0.53|patch
s3transfer|0.19.1|0.19.2|patch
pyathena|3.35.2|3.35.4|patch
scramp|1.4.12|1.4.15|patch
annotated-doc|0.0.4|0.0.5|patch
google-auth|2.56.0|2.56.2|patch
proto-plus|1.28.1|1.28.2|patch
python-discovery|1.5.0|1.5.1|patch
virtualenv|21.7.0|21.7.1|patch
markdown|3.10.2|3.10.3|patch
fastcore|2.1.4|2.1.17|patch
prompt_toolkit|3.0.52|3.0.53|patch
bokeh|3.9.1|3.9.2|patch
conda-self|0.2.0|0.2.1|patch
coverage|7.15.2|7.15.3|patch
cyclopts|4.22.0|4.22.2|patch
fastmcp-slim|3.4.4|3.4.5|patch
fastmcp|3.4.4|3.4.5|patch
gitpython|3.1.53|3.1.57|patch
google-cloud-bigquery-core|3.42.2|3.42.3|patch
pycrdt-store|0.1.3|0.1.4|patch
pycrdt-websocket|0.16.0|0.16.2|patch
jupyter_server_ydoc|2.4.0|2.4.1|patch
jupyter-ai-router|0.0.5|0.0.6|patch
langsmith|0.10.9|0.10.15|patch
panel-material-ui|0.14.0|0.14.1|patch
sqlalchemy-bigquery|1.17.0|1.17.1|patch
poppler|25.12.0|25.02.0|

### New

Package | Version
---|---
expat|2.8.1
libllvm20|20.1.8
libclang-cpp20.1|20.1.8
mysql-common|9.0.1
mysql-libs|9.0.1
httpcore2|2.5.0
httpx2|2.5.0

### Removed

Package | Last Version
---|---
apsw|3.53.3.1
apswutils|0.1.2
libclang-cpp21.1|21.1.0
dataclasses|0.8
fastlite|0.2.3
querystring_parser|1.2.4
