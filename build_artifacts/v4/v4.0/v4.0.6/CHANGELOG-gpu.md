# Change log: 4.0.6 (gpu)

This page lists all package changes since the previous release (4.0.5).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.8|4.5.9|patch
sagemaker-code-editor|1.9.6|1.9.8|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.16|1.0.17|patch
sagemaker-studio-dataengineering-extensions|1.3.10|1.3.12|patch
uv|0.11.21|0.11.24|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libsystemd0|260.2|261.1|major
libudev1|260.2|261.1|major
boltons|25.0.0|26.0.0|major
ca-certificates|2026.5.20|2026.6.17|minor
certifi|2026.5.20|2026.6.17|minor
idna|3.17|3.18|minor
accelerate|1.13.0|1.14.0|minor
dask-core|2026.3.0|2026.6.0|minor
deepmerge|2.0|2.1.0|minor
msgpack-python|1.1.2|1.2.1|minor
distributed|2026.3.0|2026.6.0|minor
anyio|4.13.0|4.14.1|minor
hpack|4.1.0|4.2.0|minor
langsmith|0.8.14|0.9.2|minor
mistune|3.2.1|3.3.2|minor
jupyter_server|2.19.0|2.20.0|minor
json5|0.14.0|0.15.0|minor
xkeyboard-config|2.47|2.48|minor
google-auth|2.53.0|2.55.1|minor
opentelemetry-proto|1.42.1|1.43.0|minor
virtualenv|21.4.2|21.5.1|minor
ujson|5.12.1|5.13.0|minor
awswrangler|3.16.1|3.17.0|minor
conda-package-streaming|0.12.0|0.13.0|minor
databricks-sdk|0.116.0|0.119.0|minor
google-cloud-bigquery-core|3.41.0|3.42.1|minor
prettytable|3.17.0|3.18.0|minor
pytest|9.0.3|9.1.1|minor
sagemaker-core|2.13.1|2.14.0|minor
sagemaker-train|1.13.1|1.14.0|minor
tzlocal|5.3.1|5.4.3|minor
llvm-openmp|22.1.7|22.1.8|patch
libuuid|2.42.1|2.42.2|patch
filelock|3.29.3|3.29.4|patch
hf-xet|1.5.0|1.5.1|patch
tqdm|4.68.2|4.68.3|patch
greenlet|3.5.1|3.5.2|patch
sqlalchemy|2.0.50|2.0.51|patch
alembic|1.18.4|1.18.5|patch
alsa-lib|1.2.16|1.2.16.1|patch
uuid-utils|0.16.0|0.16.1|patch
pydantic-settings|2.14.1|2.14.2|patch
scramp|1.4.8|1.4.9|patch
fastcore|1.13.3|1.13.7|patch
arro3-core|0.8.0|0.8.1|patch
distlib|0.4.2|0.4.3|patch
python-discovery|1.4.0|1.4.2|patch
starlette|1.3.0|1.3.1|patch
python-fasthtml|0.14.2|0.14.3|patch
typer|0.26.7|0.26.8|patch
menuinst|2.5.0|2.5.1|patch
coverage|7.14.1|7.14.3|patch
python-duckdb|1.5.3|1.5.4|patch
duckdb|1.5.3|1.5.4|patch
fastapi-cli|0.0.24|0.0.27|patch
sqlite-anyio|0.2.8|0.2.10|patch
sse-starlette|3.4.4|3.4.5|patch
nh3|0.3.5|0.3.6|patch
param|2.4.0|2.4.1|patch
pylint|4.0.5|4.0.6|patch
snowflake-sqlalchemy|1.10.0|1.10.2|patch

### New

Package | Version
---|---
httpcore2|2.5.0
httpx2|2.5.0
backports.zstd|1.6.0
