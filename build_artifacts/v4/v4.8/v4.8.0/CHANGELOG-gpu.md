# Change log: 4.8.0 (gpu)

This page lists all package changes since the previous release (4.7.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
fastapi|0.162.0|0.163.1|minor
mlflow|3.17.2|3.18.0|minor
sagemaker-python-sdk|3.26.0|3.29.0|minor
jupyter-server-proxy|4.6.0|4.6.1|patch
sagemaker-studio-dataengineering-sessions|1.3.27|1.3.28|patch
uv|0.13.7|0.13.8|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libsystemd0|262.1|262.2|minor
libudev1|262.1|262.2|minor
tornado|6.5.10|6.6.1|minor
jsonpointer|3.8|3.12|minor
soupsieve|4.0|4.1.1|minor
send2trash|2.1.0|2.2.0|minor
pandoc|3.13|3.14|minor
google-api-core|2.29.0|2.33.0|minor
threadpoolctl|3.7.0|3.8.0|minor
markdown-it-py|4.2.0|4.3.0|minor
regex|2026.9.29|2026.11.15|minor
typer|0.27.3|0.29.1|minor
cachetools|7.2.8|7.3.0|minor
conda-rattler-solver|26.10.2|26.11.0|minor
cyclopts|5.3.3|5.5.0|minor
databricks-sdk|0.161.0|0.166.0|minor
email-validator|2.3.0|2.4.0|minor
email_validator|2.3.0|2.4.0|minor
fastapi-core|0.162.0|0.163.1|minor
sse-starlette|3.6.0|3.7.0|minor
google-cloud-bigquery-core|3.47.0|3.18.0|minor
jiter|0.18.0|0.19.0|minor
jsonpatch|1.33|1.47|minor
mdit-py-plugins|0.6.1|0.7.0|minor
mlflow-skinny|3.17.2|3.18.0|minor
mlflow-ui|3.17.2|3.18.0|minor
pyroaring|1.1.0|1.2.0|minor
sagemaker-core|2.28.0|2.29.0|minor
sagemaker-train|1.26.0|1.29.0|minor
sagemaker-serve|1.26.0|1.29.0|minor
sagemaker-mlops|1.26.0|1.29.0|minor
sqlalchemy-bigquery|1.17.3|1.16.0|minor
sqlglot|30.29.0|30.31.0|minor
slack-sdk|3.46.0|3.47.0|minor
mpc|1.4.0|1.4.1|patch
triad|1.0.3|1.0.4|patch
pydantic-core|2.50.2|2.50.4|patch
pydantic|2.14.2|2.14.3|patch
annotated-doc|0.0.5|0.0.6|patch
authlib|1.9.3|1.9.6|patch
google-auth|2.62.1|2.62.2|patch
opentelemetry-api|1.45.1|1.45.2|patch
opentelemetry-sdk|1.45.1|1.45.2|patch
smart_open|9.0.2|9.0.4|patch
python-discovery|1.9.4|1.9.5|patch
markdown|3.11.2|3.11.3|patch
libaec|1.1.7|1.1.8|patch
fastcore|2.2.37|2.2.41|patch
python-fasthtml|0.14.18|0.14.23|patch
smart-open|9.0.2|9.0.4|patch
fugue|0.9.7|0.9.9|patch
coverage|7.17.0|7.17.3|patch
dnspython|2.9.1|2.9.2|patch
pydantic-settings|2.16.2|2.16.3|patch
py-key-value-aio|0.4.5|0.4.6|patch
pymysql|1.2.3|1.2.4|patch
rope|1.15.0|1.15.2|patch
opentelemetry-semantic-conventions|0.66b1|0.66b2|
opentelemetry-exporter-prometheus|0.66b1|0.66b2|
opentelemetry-instrumentation|0.66b1|0.66b2|
opentelemetry-instrumentation-threading|0.66b1|0.66b2|

### Removed

Package | Last Version
---|---
google-api-core-grpc|2.29.0
