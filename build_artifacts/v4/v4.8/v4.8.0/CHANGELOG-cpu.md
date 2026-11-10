# Change log: 4.8.0 (cpu)

This page lists all package changes since the previous release (4.7.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
mlflow|3.17.2|3.18.0|minor
sagemaker-python-sdk|3.26.0|3.29.0|minor
fastapi|0.162.0|0.162.2|patch
jupyter-activity-monitor-extension|0.3.2|0.3.3|patch
sagemaker-studio-dataengineering-sessions|1.3.27|1.3.28|patch
uv|0.13.6|0.13.7|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
pyzmq|26.4.0|27.3.0|major
soupsieve|3.0.4|4.0.1|major
conda-rattler-solver|0.2.0|26.10.2|major
hf-xet|1.7.0|1.8.0|minor
libnghttp2|1.70.0|1.71.0|minor
lerc|4.2.0|4.3.0|minor
anyio|4.15.1|4.16.0|minor
platformdirs|4.13.7|4.14.5|minor
tornado|6.5.10|6.6|minor
jsonpointer|3.6|3.10|minor
joserfc|1.7.7|1.8.0|minor
lcms2|2.19.1|2.20|minor
google-api-core|2.33.0|2.29.0|minor
python-discovery|1.6.7|1.9.5|minor
gdown|6.4.2|6.5.1|minor
regex|2026.9.29|2026.11.9|minor
typer|0.27.3|0.28.0|minor
awswrangler|3.17.1|3.18.0|minor
cachetools|7.2.6|7.3.0|minor
unearth|0.18.3|0.19.0|minor
py-rattler|0.27.1|0.28.1|minor
frozendict|2.4.7|2.5.0|minor
cyclopts|5.3.2|5.4.0|minor
databricks-sdk|0.157.0|0.163.0|minor
websockets|17.3|17.4|minor
sse-starlette|3.6.0|3.7.0|minor
google-crc32c|1.8.0|1.9.0|minor
google-cloud-bigquery-core|3.18.0|3.47.0|minor
jiter|0.18.0|0.19.0|minor
jsonpatch|1.33|1.44|minor
mlflow-skinny|3.17.2|3.18.0|minor
mlflow-ui|3.17.2|3.18.0|minor
python-rapidjson|1.25|1.26|minor
sagemaker-core|2.27.0|2.29.0|minor
sagemaker-train|1.26.0|1.29.0|minor
sagemaker-serve|1.26.0|1.29.0|minor
sagemaker-mlops|1.26.0|1.29.0|minor
sqlalchemy-bigquery|1.16.0|1.17.3|minor
sqlglot|30.25.0|30.30.0|minor
slack-sdk|3.45.0|3.46.0|minor
llvm-openmp|23.1.4|23.1.5|patch
triad|1.0.2|1.0.3|patch
fribidi|1.0.17|1.0.18|patch
pydantic-core|2.50.1|2.50.4|patch
typing-inspection|0.4.4|0.4.5|patch
pydantic|2.14.1|2.14.3|patch
wrapt|2.5.1|2.5.2|patch
python-fastjsonschema|2.22.2|2.22.3|patch
authlib|1.9.1|1.9.5|patch
google-auth|2.62.0|2.62.1|patch
py-spy|0.4.2|0.4.3|patch
smart_open|9.0.0|9.0.2|patch
markdown|3.11.2|3.11.3|patch
blosc|1.21.6|1.21.7|patch
libaec|1.1.5|1.1.7|patch
fastcore|2.2.35|2.2.40|patch
oauthlib|4.0.0|4.0.1|patch
python-multipart|0.0.32|0.0.33|patch
python-fasthtml|0.14.14|0.14.21|patch
smart-open|9.0.0|9.0.2|patch
numba|0.68.0|0.68.1|patch
conda-libmamba-solver|26.10.0|26.10.1|patch
coverage|7.17.0|7.17.2|patch
deprecated|3.0.0|3.0.1|patch
dnspython|2.9.0|2.9.1|patch
fastapi-core|0.162.0|0.162.2|patch
huey|3.5.3|3.5.4|patch
langsmith|0.14.14|0.14.17|patch
pymysql|1.2.3|1.2.4|patch
rope|1.15.0|1.15.2|patch

### New

Package | Version
---|---
google-api-core-grpc|2.29.0
