# Change log: 4.2.4 (cpu)

This page lists all package changes since the previous release (4.2.3).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.9|4.5.10|patch
boto3|1.43.0|1.43.46|patch
sagemaker-jupyterlab-extension-common|0.4.6|0.4.7|patch
sagemaker-jupyterlab-extension|0.5.9|0.5.10|patch
sagemaker-studio|1.1.22|1.1.26|patch
uv|0.11.28|0.11.30|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
ld_impl_linux-64|2.45.1|2.46.1|minor
filelock|3.29.7|3.32.0|minor
tqdm|4.68.4|4.69.0|minor
gflags|2.2.2|2.3.0|minor
libjpeg-turbo|3.1.4.1|3.2.0|minor
aiobotocore|3.7.0|3.8.0|minor
narwhals|2.23.0|2.24.0|minor
platformdirs|4.10.0|4.11.0|minor
soupsieve|2.8.4|2.9.1|minor
s3transfer|0.17.1|0.19.1|minor
pyathena|3.32.0|3.35.2|minor
fastcore|2.0.1|2.1.4|minor
wayland|1.25.0|1.26.0|minor
google-auth|2.55.1|2.56.0|minor
opentelemetry-proto|1.43.0|1.44.0|minor
python-discovery|1.4.4|1.5.0|minor
virtualenv|21.6.0|21.7.0|minor
regex|2026.6.28|2026.7.19|minor
typer|0.26.8|0.27.0|minor
llvmlite|0.47.0|0.48.0|minor
numba|0.65.1|0.66.0|minor
colorlog|6.10.1|6.11.0|minor
conda-libmamba-solver|26.6.0|26.7.0|minor
cyclopts|4.20.0|4.22.0|minor
databricks-sdk|0.120.0|0.122.0|minor
pynacl|1.6.2|1.5.0|minor
docker-py|7.1.0|7.2.0|minor
jaraco.functools|4.5.0|4.6.0|minor
python-flatbuffers|25.9.23|25.12.19|minor
thrift|0.23.0|0.24.0|minor
sagemaker-core|2.15.0|2.16.0|minor
snowflake-sqlalchemy|1.10.2|1.11.0|minor
slack-bolt|1.29.0|1.30.0|minor
hf-xet|1.5.1|1.5.2|patch
c-ares|1.34.6|1.34.8|patch
yarl|1.24.2|1.24.5|patch
aiohttp|3.14.1|3.14.2|patch
botocore|1.43.0|1.43.46|patch
anyio|4.14.1|4.14.2|patch
asttokens|3.0.1|3.0.2|patch
tomlkit|0.15.0|0.15.1|patch
apsw|3.53.3.0|3.53.3.1|patch
joserfc|1.7.3|1.7.4|patch
proto-plus|1.28.0|1.28.1|patch
opencensus|0.11.3|0.11.4|patch
smart_open|8.0.0|8.0.1|patch
smart-open|8.0.0|8.0.1|patch
menuinst|2.5.1|2.5.2|patch
coverage|7.15.0|7.15.2|patch
python-duckdb|1.5.4|1.5.1|patch
duckdb|1.5.4|1.5.1|patch
rich-toolkit|0.20.1|0.20.3|patch
websockets|16.1|16.1.1|patch
fastapi-cli|0.0.29|0.0.32|patch
sse-starlette|3.4.5|3.4.6|patch
gitpython|3.1.50|3.1.53|patch
google-cloud-bigquery-core|3.42.1|3.42.2|patch
langsmith|0.10.2|0.10.9|patch
schema|0.7.7|0.7.8|patch
tzdata|2025c|2026c|

### New

Package | Version
---|---
pywin32|312
