# Change log: 4.3.5 (cpu)

This page lists all package changes since the previous release (4.3.4).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyter-ai|3.0.1|3.2.0|minor
sagemaker-jupyterlab-extension-common|0.4.8|0.4.7|patch
aws-smus-cicd-cli|1.0.6|1.0.7|patch
jupyter-collaboration|4.4.0|4.4.2|patch
sagemaker-studio-dataengineering-sessions|1.3.24|1.3.25|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
llvm-openmp|22.1.8|23.1.0|major
wrapt|1.17.3|2.4.0|major
isort|8.0.1|9.0.1|major
agent-client-protocol|0.9.0|0.11.1|minor
anyio|4.14.2|4.15.0|minor
jupyter_client|8.9.1|8.10.0|minor
jupyter_server|2.20.0|2.21.0|minor
pandoc|3.10.2|3.11|minor
pyathena|3.35.4|3.36.0|minor
authlib|1.7.2|1.8.0|minor
joblib|1.5.3|1.6.0|minor
google-auth|2.56.3|2.57.0|minor
opentelemetry-api|1.43.0|1.44.0|minor
opentelemetry-sdk|1.43.0|1.44.0|minor
python-discovery|1.5.3|1.6.0|minor
regex|2026.7.19|2026.9.3|minor
plum-dispatch|2.9.0|2.10.0|minor
statsmodels|0.14.6|0.15.0|minor
conda-package-handling|2.5.0|2.6.0|minor
python-build|1.5.0|1.6.0|minor
coverage|7.15.4|7.16.0|minor
websockets|17.0.1|17.1|minor
google-resumable-media|2.8.0|2.10.2|minor
google-cloud-bigquery-core|3.43.0|3.44.0|minor
jiter|0.15.0|0.16.0|minor
pycrdt|0.12.50|0.13.1|minor
jupyter_ydoc|3.4.1|3.5.0|minor
jupyterlab-chat|0.22.1|0.25.0|minor
jupyter-ai-router|0.0.7|0.1.1|minor
jupyter-ai-persona-manager|0.0.12|0.2.0|minor
jupyter-ai-acp-client|0.1.5|0.3.0|minor
jupyterlab-commands-toolkit|0.1.6|0.2.0|minor
jupyter-ai-tools|0.5.2|0.7.0|minor
jupyter-server-mcp|0.2.1|0.3.0|minor
langsmith|0.11.1|0.12.1|minor
linkify-it-py|2.1.1|2.2.0|minor
mmh3|5.2.1|5.3.0|minor
sagemaker-core|2.20.0|2.21.0|minor
slack-sdk|3.43.0|3.44.1|minor
libuuid|2.42.2|2.42.3|patch
filelock|3.32.4|3.32.5|patch
pydantic-core|2.46.4|2.46.5|patch
pydantic|2.13.4|2.13.5|patch
platformdirs|4.11.4|4.11.6|patch
websocket-client|1.9.0|1.9.2|patch
wcwidth|0.8.2|0.8.3|patch
fastcore|2.2.15|2.2.21|patch
arro3-core|0.8.1|0.8.2|patch
joserfc|1.7.4|1.7.5|patch
kiwisolver|1.5.0|1.5.1|patch
msgpack-python|1.2.1|1.2.2|patch
virtualenv|21.7.4|21.7.8|patch
typer|0.27.1|0.27.2|patch
patsy|1.0.2|1.0.3|patch
reproc|14.2.7.post0|14.2.8.post0|patch
reproc-cpp|14.2.7.post0|14.2.8.post0|patch
sse-starlette|3.4.8|3.4.10|patch
gitpython|3.1.59|3.1.61|patch
graphql-core|3.2.11|3.2.12|patch
pycrdt-store|0.1.3|0.1.4|patch
pycrdt-websocket|0.16.0|0.16.2|patch
jupyter_server_ydoc|2.4.0|2.4.2|patch
pylint|4.0.7|4.0.8|patch
pyspnego|0.12.1|0.12.2|patch
opentelemetry-semantic-conventions|0.64b0|0.65b0|
opentelemetry-exporter-prometheus|0.64b0|0.65b0|
opentelemetry-instrumentation|0.64b0|0.65b0|
opentelemetry-instrumentation-threading|0.64b0|0.65b0|

### New

Package | Version
---|---
libpython|3.12.14
interface_meta|1.3.0
formulaic|1.2.2
httpcore2|2.5.0
httpx2|2.5.0
jupyterlab-cell-input-footer|0.3.2
jupyterlab-diff|0.7.1
jupyterlab-ai-commands|0.4.0
jupyter-live-content|0.1.1

### Removed

Package | Last Version
---|---
jupyter_server_documents|0.2.6
jupyterlab-notebook-awareness|0.2.0
