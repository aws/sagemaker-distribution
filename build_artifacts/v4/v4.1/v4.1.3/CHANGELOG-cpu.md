# Change log: 4.1.3 (cpu)

This page lists all package changes since the previous release (4.1.2).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension-common|0.4.2|0.4.3|patch
amazon-sagemaker-jupyter-scheduler|3.2.0|3.2.2|patch
mcp|1.27.0|1.27.1|patch
uv|0.11.13|0.11.14|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
harfbuzz|11.5.1|12.2.0|major
decorator|5.2.1|5.3.1|minor
fastcore|1.12.47|1.13.2|minor
fonttools|4.62.1|4.63.0|minor
libpciaccess|0.18|0.19|minor
google-auth|2.52.0|2.53.0|minor
docstring_parser|0.17.0|0.18.0|minor
cyclopts|4.11.2|4.14.0|minor
databricks-sdk|0.108.0|0.109.0|minor
deepdiff|9.0.0|9.1.0|minor
watchfiles|1.1.1|1.2.0|minor
jaraco.functools|4.4.0|4.5.0|minor
fastmcp|3.2.4|3.3.1|minor
jupyter-collaboration-ui|2.4.0|2.3.0|minor
jupyterlab-chat|0.21.1|0.22.0|minor
onnxruntime|1.25.1|1.26.0|minor
sagemaker-core|2.10.1|2.11.0|minor
sagemaker-train|1.10.1|1.11.0|minor
sagemaker-serve|1.10.1|1.11.0|minor
sagemaker-mlops|1.10.1|1.11.0|minor
libuuid|2.42|2.42.1|patch
requests|2.34.0|2.34.2|patch
narwhals|2.21.0|2.21.2|patch
xorg-libxi|1.8.2|1.8.3|patch
libdrm|2.4.125|2.4.127|patch
python-discovery|1.3.0|1.3.1|patch
virtualenv|21.3.1|21.3.3|patch
python-multipart|0.0.28|0.0.29|patch
orjson|3.11.8|3.11.9|patch
conda-libmamba-solver|26.4.1|26.4.2|patch
rich-toolkit|0.19.8|0.19.9|patch
sse-starlette|3.4.3|3.4.4|patch
jupyter_server_documents|0.2.1|0.2.2|patch
langsmith|0.8.3|0.8.5|patch
mdit-py-plugins|0.6.0|0.6.1|patch

### New

Package | Version
---|---
cachebox|5.2.3
fastmcp-slim|3.3.1
