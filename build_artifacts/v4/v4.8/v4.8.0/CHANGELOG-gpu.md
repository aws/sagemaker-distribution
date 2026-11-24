# Change log: 4.8.0 (gpu)

This page lists all package changes since the previous release (4.7.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
fastapi|0.162.0|0.165.0|minor
mlflow|3.17.2|3.18.0|minor
sagemaker-python-sdk|3.26.0|3.29.0|minor
jupyter-server-proxy|4.6.0|4.6.1|patch
sagemaker-code-editor|1.10.3|1.10.5|patch
sagemaker-studio-dataengineering-extensions|1.3.15|1.3.16|patch
sagemaker-studio-dataengineering-sessions|1.3.27|1.3.29|patch
uv|0.13.7|0.13.9|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
rdma-core|65.0|66.0|major
smart_open|9.0.2|10.0.0|major
python-xxhash|3.7.0|4.1.0|major
smart-open|9.0.2|10.0.0|major
cachebox|5.2.3|6.2.11|major
ca-certificates|2026.10.23|2026.11.20|minor
certifi|2026.10.23|2026.11.20|minor
libsystemd0|262.1|262.2|minor
libudev1|262.1|262.2|minor
accelerate|1.15.0|1.16.0|minor
narwhals|2.28.0|2.29.0|minor
argon2-cffi-bindings|26.1.0|26.2.0|minor
tornado|6.5.10|6.6.1|minor
jsonpointer|3.8|3.12|minor
soupsieve|4.0|4.1.3|minor
send2trash|2.1.0|2.2.0|minor
pandoc|3.13|3.14|minor
qt6-main|6.9.0|6.8.3|minor
pyside6|6.9.0|6.8.3|minor
google-auth|2.62.1|2.63.1|minor
google-api-core|2.29.0|2.33.0|minor
threadpoolctl|3.7.0|3.8.0|minor
python-slugify|9.1.3|9.2.0|minor
markdown-it-py|4.2.0|4.3.0|minor
regex|2026.9.29|2026.11.19|minor
nspr|4.40|4.41|minor
ujson|6.0.0|6.1.0|minor
typer|0.27.3|0.29.2|minor
optuna|5.0.0|5.1.0|minor
cachetools|7.2.8|7.3.0|minor
conda-rattler-solver|26.10.2|26.11.0|minor
cyclopts|5.3.3|5.5.2|minor
databricks-sdk|0.161.0|0.170.0|minor
deepdiff|9.1.0|9.2.1|minor
email-validator|2.3.0|2.4.0|minor
email_validator|2.3.0|2.4.0|minor
fastapi-core|0.162.0|0.165.0|minor
sse-starlette|3.6.0|3.7.1|minor
google-cloud-bigquery-core|3.47.0|3.18.0|minor
jiter|0.18.0|0.19.0|minor
jsonpatch|1.33|1.48|minor
langsmith|0.14.17|0.16.0|minor
mdit-py-plugins|0.6.1|0.7.0|minor
mlflow-skinny|3.17.2|3.18.0|minor
mlflow-ui|3.17.2|3.18.0|minor
prettytable|3.18.0|3.19.0|minor
pyroaring|1.1.0|1.2.0|minor
sagemaker-core|2.28.0|2.30.0|minor
sagemaker-train|1.26.0|1.30.0|minor
sagemaker-serve|1.26.0|1.30.0|minor
sagemaker-mlops|1.26.0|1.29.0|minor
sqlalchemy-bigquery|1.17.3|1.16.0|minor
sqlglot|30.29.0|30.33.0|minor
slack-sdk|3.46.0|3.48.0|minor
llvm-openmp|23.1.5|23.1.6|patch
yaml|0.2.5|0.2.6|patch
charset-normalizer|3.5.2|3.5.3|patch
nccl|2.32.3.1|2.32.6.1|patch
mpc|1.4.0|1.4.1|patch
triad|1.0.3|1.0.4|patch
fontconfig|2.18.3|2.18.4|patch
pydantic-core|2.50.2|2.50.5|patch
pydantic|2.14.2|2.14.4|patch
platformdirs|4.14.5|4.14.8|patch
decorator|5.3.1|5.3.2|patch
exceptiongroup|1.3.1|1.3.2|patch
wcwidth|0.9.4|0.9.5|patch
annotated-doc|0.0.5|0.0.7|patch
authlib|1.9.3|1.9.10|patch
cloudpickle|3.1.2|3.1.3|patch
opentelemetry-api|1.45.1|1.45.2|patch
opentelemetry-sdk|1.45.1|1.45.2|patch
py-spy|0.4.3|0.4.4|patch
python-discovery|1.9.4|1.9.6|patch
gdown|6.5.1|6.5.2|patch
markdown|3.11.2|3.11.3|patch
imageio|2.38.1|2.38.2|patch
libaec|1.1.7|1.1.8|patch
fastcore|2.2.37|2.2.46|patch
python-multipart|0.0.33|0.0.34|patch
python-fasthtml|0.14.18|0.14.30|patch
fugue|0.9.7|0.9.9|patch
coverage|7.17.0|7.17.5|patch
dnspython|2.9.1|2.9.2|patch
pydantic-settings|2.16.2|2.16.3|patch
py-key-value-aio|0.4.5|0.4.6|patch
nh3|0.3.7|0.3.8|patch
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
