# Change log: 4.3.9 (gpu)

This page lists all package changes since the previous release (4.3.8).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
amazon_sagemaker_sql_editor|0.2.6|0.2.7|patch
sagemaker-studio|1.1.32|1.1.35|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
cffi|1.17.1|2.1.1|major
soupsieve|2.10|3.0.3|major
pyopenssl|25.3.0|26.2.0|major
snowflake-connector-python|3.17.4|4.8.0|major
hf-xet|1.5.2|1.7.0|minor
pydantic-core|2.46.5|2.50.1|minor
pydantic|2.13.5|2.14.1|minor
async-lru|2.3.0|2.4.0|minor
pycparser|3.0|3.11|minor
platformdirs|4.12.3|4.13.0|minor
executing|2.2.1|2.3.0|minor
json5|0.15.0|0.17.3|minor
amazon-sagemaker-sql-execution|0.1.9|0.2.0|minor
authlib|1.8.0|1.9.1|minor
fonttools|4.66.1|4.67.0|minor
qt6-main|6.9.0|6.8.3|minor
pyside6|6.9.0|6.8.3|minor
google-auth|2.60.0|2.62.0|minor
google-api-core|2.33.0|2.29.0|minor
orjson|3.12.0|3.13.0|minor
backports.zstd|1.7.0|1.8.0|minor
pyproject_hooks|1.2.0|1.3.3|minor
python-installer|1.0.1|1.1.0|minor
pluggy|1.6.0|1.7.0|minor
databricks-sdk|0.148.0|0.153.0|minor
pynacl|1.5.0|1.6.2|minor
httptools|0.8.0|0.9.0|minor
pydantic-settings|2.15.0|2.16.0|minor
more-itertools|11.1.0|11.2.1|minor
google-cloud-bigquery-core|3.18.0|3.46.1|minor
jupyter_server_fileid|0.9.2|0.10.0|minor
onnxruntime|1.30.0|1.31.0|minor
sagemaker-core|2.23.0|2.25.0|minor
sagemaker-train|1.14.0|1.25.0|minor
sagemaker-serve|1.12.0|1.25.0|minor
sagemaker-mlops|1.12.0|1.25.0|minor
sqlalchemy-bigquery|1.16.0|1.17.3|minor
sqlglot|30.21.0|30.23.0|minor
absl-py|2.5.0|2.5.1|patch
aiohttp|3.14.4|3.14.5|patch
wrapt|2.5.0|2.5.1|patch
narwhals|2.27.0|2.27.1|patch
jsonpointer|3.2.0|3.2.1|patch
nbconvert-core|7.17.1|7.17.2|patch
pandoc|3.12|3.12.1|patch
nbconvert-pandoc|7.17.1|7.17.2|patch
nbconvert|7.17.1|7.17.2|patch
arro3-core|0.9.0|0.9.1|patch
opentelemetry-api|1.45.0|1.45.1|patch
opentelemetry-sdk|1.45.0|1.45.1|patch
smart_open|8.0.2|8.0.3|patch
python-discovery|1.6.1|1.6.2|patch
virtualenv|21.14.5|21.14.6|patch
gdown|6.4.1|6.4.2|patch
markdown|3.11|3.11.1|patch
imageio|2.38.0|2.38.1|patch
charls|2.4.4|2.4.5|patch
smart-open|8.0.2|8.0.3|patch
spacy|3.8.14|3.8.16|patch
cachetools|7.2.1|7.2.2|patch
truststore|0.10.4|0.10.5|patch
entrypoints|0.4|0.4.2|patch
rich-toolkit|0.20.5|0.20.6|patch
gitpython|3.2.0|3.2.1|patch
iniconfig|2.3.0|2.3.1|patch
jupyterlab-chat|0.25.1|0.25.2|patch
jupyter-ai-acp-client|0.3.2|0.3.3|patch
jupyter-live-content|0.1.1|0.1.2|patch
langsmith|0.14.4|0.14.9|patch
panel-material-ui|0.16.1|0.16.3|patch
opentelemetry-semantic-conventions|0.66b0|0.66b1|
opentelemetry-exporter-prometheus|0.66b0|0.66b1|
opentelemetry-instrumentation|0.66b0|0.66b1|
opentelemetry-instrumentation-threading|0.66b0|0.66b1|

### New

Package | Version
---|---
google-api-core-grpc|2.29.0

### Removed

Package | Last Version
---|---
rsa|4.9.1
