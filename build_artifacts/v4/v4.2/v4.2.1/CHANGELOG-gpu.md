# Change log: 4.2.1 (gpu)

This page lists all package changes since the previous release (4.2.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
pip|26.1.1|26.1.2|patch
conda|26.5.0|26.5.2|patch
docker-cli|29.5.2|29.5.3|patch
mcp|1.27.1|1.27.2|patch
uv|0.11.16|0.11.18|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libcap|2.77|2.78|minor
propcache|0.3.1|0.5.2|minor
narwhals|2.21.2|2.22.0|minor
jupyter_server|2.18.2|2.19.0|minor
joserfc|1.6.8|1.7.0|minor
gdown|6.0.0|6.1.0|minor
optuna|4.8.0|4.9.0|minor
databricks-sdk|0.112.0|0.114.0|minor
fastmcp-slim|3.3.1|3.4.0|minor
fastmcp|3.3.1|3.4.0|minor
sagemaker-core|2.12.0|2.13.0|minor
llvm-openmp|22.1.6|22.1.7|patch
filelock|3.29.0|3.29.1|patch
fontconfig|2.18.0|2.18.1|patch
graphite2|1.3.14|1.3.15|patch
alsa-lib|1.2.15.3|1.2.16|patch
traitlets|5.15.0|5.15.1|patch
debugpy|1.8.20|1.8.21|patch
distlib|0.4.0|0.4.1|patch
virtualenv|21.4.1|21.4.2|patch
pytorch-lightning|2.6.1|2.6.5|patch
python-multipart|0.0.29|0.0.30|patch
typer|0.26.2|0.26.7|patch
ocl-icd|2.3.3|2.3.4|patch
libsolv|0.7.38|0.7.39|patch
fastapi-cli|0.0.23|0.0.24|patch
langsmith|0.8.6|0.8.9|patch
panel-material-ui|0.11.0|0.11.2|patch
panel|1.9.1|1.9.3|patch
snowballstemmer|3.1.0|3.1.1|patch

### New

Package | Version
---|---
panel-core|1.9.3
