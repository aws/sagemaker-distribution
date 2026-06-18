# Change log: 2.13.9 (gpu)

This page lists all package changes since the previous release (2.13.8).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.8|4.5.9|patch
sagemaker-code-editor|1.8.9|1.8.10|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
ca-certificates|2026.5.20|2026.6.17|minor
certifi|2026.5.20|2026.6.17|minor
idna|3.17|3.18|minor
accelerate|1.13.0|1.14.0|minor
anyio|4.13.0|4.14.0|minor
jupyter_server|2.19.0|2.20.0|minor
dask-core|2026.3.0|2026.6.0|minor
distributed|2026.3.0|2026.6.0|minor
google-auth|2.53.0|2.55.0|minor
virtualenv|21.4.2|21.5.1|minor
ujson|5.12.1|5.13.0|minor
conda-package-streaming|0.12.0|0.13.0|minor
google-cloud-bigquery-core|3.41.0|3.42.0|minor
pytest|9.0.3|9.1.0|minor
llvm-openmp|22.1.7|22.1.8|patch
libuuid|2.42.1|2.42.2|patch
filelock|3.29.3|3.29.4|patch
sqlalchemy|2.0.50|2.0.51|patch
alsa-lib|1.2.16|1.2.16.1|patch
langsmith|0.8.14|0.8.16|patch
fastcore|1.13.3|1.13.5|patch
arro3-core|0.8.0|0.8.1|patch
distlib|0.4.2|0.4.3|patch
python-discovery|1.4.0|1.4.2|patch
python-duckdb|1.5.3|1.5.4|patch
duckdb|1.5.3|1.5.4|patch
param|2.4.0|2.4.1|patch
pylint|4.0.5|4.0.6|patch
snowflake-sqlalchemy|1.10.0|1.10.1|patch

### New

Package | Version
---|---
backports.zstd|1.6.0
