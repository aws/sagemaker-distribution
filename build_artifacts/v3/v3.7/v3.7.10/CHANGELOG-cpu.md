# Change log: 3.7.10 (cpu)

This page lists all package changes since the previous release (3.7.9).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-code-editor|1.8.9|1.8.10|patch
sagemaker-studio|1.1.20|1.1.22|patch
sagemaker-studio-dataengineering-extensions|1.3.10|1.3.12|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python-json-logger|3.2.1|4.1.0|major
ca-certificates|2026.5.20|2026.6.17|minor
certifi|2026.5.20|2026.6.17|minor
idna|3.17|3.18|minor
tqdm|4.67.3|4.68.2|minor
safetensors|0.7.0|0.8.0|minor
accelerate|1.13.0|1.14.0|minor
aiohttp|3.13.5|3.14.1|minor
anyio|4.13.0|4.14.0|minor
wcwidth|0.7.0|0.8.1|minor
jupyter_client|8.8.0|8.9.1|minor
ipykernel|7.2.0|7.3.0|minor
beautifulsoup4|4.14.3|4.15.0|minor
bleach|6.3.0|6.4.0|minor
bleach-with-css|6.3.0|6.4.0|minor
nbclient|0.10.4|0.11.0|minor
jupyter_server|2.19.0|2.20.0|minor
dask-core|2026.3.0|2026.6.0|minor
distributed|2026.3.0|2026.6.0|minor
google-auth|2.53.0|2.55.0|minor
virtualenv|21.4.2|21.5.1|minor
ujson|5.12.1|5.13.0|minor
conda-package-streaming|0.12.0|0.13.0|minor
conda-package-handling|2.4.0|2.5.0|minor
menuinst|2.4.2|2.5.0|minor
rich-toolkit|0.19.10|0.20.1|minor
google-cloud-bigquery-core|3.41.0|3.42.0|minor
pytest|9.0.3|9.1.0|minor
llvm-openmp|22.1.7|22.1.8|patch
libuuid|2.42.1|2.42.2|patch
openssl|3.6.2|3.6.3|patch
filelock|3.29.1|3.29.4|patch
sqlalchemy|2.0.50|2.0.51|patch
alsa-lib|1.2.16|1.2.16.1|patch
narwhals|2.22.0|2.22.1|patch
tornado|6.5.6|6.5.7|patch
langsmith|0.8.9|0.8.16|patch
fastcore|1.13.2|1.13.5|patch
arro3-core|0.8.0|0.8.1|patch
distlib|0.4.1|0.4.3|patch
python-discovery|1.4.0|1.4.2|patch
charls|2.4.3|2.4.4|patch
bokeh|3.9.0|3.9.1|patch
python-duckdb|1.5.3|1.5.4|patch
duckdb|1.5.3|1.5.4|patch
graphql-core|3.2.8|3.2.11|patch
param|2.4.0|2.4.1|patch
pylint|4.0.5|4.0.6|patch
snowflake-sqlalchemy|1.10.0|1.10.1|patch

### New

Package | Version
---|---
nest-asyncio2|1.7.2
backports.zstd|1.6.0
tomli-w|1.2.0
oracledb|3.4.2
