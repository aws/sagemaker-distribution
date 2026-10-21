# Change log: 4.7.0 (gpu)

This page lists all package changes since the previous release (4.6.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
amazon-sagemaker-sql-magic|0.1.4|0.2.0|minor
docker-cli|29.8.2|29.9.0|minor
fastapi|0.142.2|0.154.0|minor
jupyterlab-git|0.54.1|0.55.0|minor
mlflow|3.16.1|3.17.1|minor
sagemaker-python-sdk|3.12.0|3.25.0|minor
uv|0.12.21|0.13.4|minor
amazon_sagemaker_sql_editor|0.2.6|0.2.8|patch
pip|26.2.1|26.2.2|patch
sagemaker-code-editor|1.10.2|1.10.3|patch
sagemaker-studio|1.1.32|1.1.35|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
cffi|1.17.1|2.1.1|major
soupsieve|2.10|3.0.3|major
cryptography|46.0.7|50.0.2|major
pyopenssl|25.3.0|26.4.0|major
snowflake-connector-python|3.17.4|4.8.0|major
ca-certificates|2026.7.22|2026.10.19|minor
hf-xet|1.5.2|1.7.0|minor
certifi|2026.7.22|2026.10.19|minor
setuptools|84.0.0|84.2.0|minor
pydantic-core|2.46.5|2.50.1|minor
pydantic|2.13.5|2.14.1|minor
multidict|6.7.1|6.9.1|minor
async-lru|2.3.0|2.4.0|minor
pycparser|3.0|3.11|minor
platformdirs|4.12.3|4.13.5|minor
jsonpointer|3.1.1|3.4|minor
mistune|3.3.4|3.4.0|minor
executing|2.2.1|2.3.0|minor
json5|0.15.0|0.17.3|minor
tenacity|9.1.4|9.2.1|minor
pyathena|3.36.0|3.38.0|minor
amazon-sagemaker-sql-execution|0.1.9|0.2.0|minor
authlib|1.8.0|1.9.1|minor
fonttools|4.66.1|4.67.0|minor
qt6-main|6.8.3|6.9.0|minor
pyside6|6.8.3|6.9.0|minor
google-auth|2.60.0|2.62.0|minor
google-api-core|2.29.0|2.33.0|minor
python-slugify|9.0.0|9.1.3|minor
starlette|1.7.0|1.9.0|minor
beartype|0.22.9|0.23.1|minor
orjson|3.12.0|3.13.0|minor
tomli|2.4.1|2.5.0|minor
backports.zstd|1.7.0|1.8.0|minor
pyproject_hooks|1.2.0|1.3.3|minor
python-installer|1.0.1|1.1.0|minor
pluggy|1.6.0|1.7.0|minor
databricks-sdk|0.147.0|0.154.0|minor
pynacl|1.5.0|1.6.2|minor
paramiko|5.0.0|5.1.0|minor
httptools|0.8.0|0.9.0|minor
websockets|17.2|17.3|minor
fastapi-core|0.142.2|0.154.0|minor
pydantic-settings|2.15.0|2.16.1|minor
griffelib|2.3.2|2.4.0|minor
more-itertools|11.1.0|11.2.1|minor
google-cloud-bigquery-core|3.46.1|3.18.0|minor
jupyter_server_fileid|0.9.2|0.10.0|minor
jupyterlab-git-core|0.54.1|0.55.0|minor
mlflow-skinny|3.16.1|3.17.1|minor
mlflow-ui|3.16.1|3.17.1|minor
onnxruntime|1.30.0|1.31.0|minor
sagemaker-core|2.23.0|2.26.0|minor
sagemaker-train|1.14.0|1.26.0|minor
sagemaker-serve|1.12.0|1.25.0|minor
sagemaker-mlops|1.12.0|1.25.0|minor
sqlalchemy-bigquery|1.17.3|1.16.0|minor
sqlglot|30.21.0|30.23.0|minor
llvm-openmp|23.1.2|23.1.3|patch
absl-py|2.5.0|2.5.1|patch
c-ares|1.34.8|1.34.9|patch
xorg-libxrender|0.9.12|0.9.13|patch
aiohttp|3.14.4|3.14.5|patch
wrapt|2.5.0|2.5.1|patch
narwhals|2.27.0|2.27.1|patch
nbconvert-core|7.17.1|7.17.2|patch
pandoc|3.12|3.12.1|patch
nbconvert-pandoc|7.17.1|7.17.2|patch
nbconvert|7.17.1|7.17.2|patch
jedi|0.20.0|0.20.1|patch
wcwidth|0.9.2|0.9.3|patch
s3transfer|0.19.2|0.19.3|patch
tomlkit|0.15.1|0.15.2|patch
arro3-core|0.9.0|0.9.1|patch
xorg-libxtst|1.2.5|1.2.6|patch
joserfc|1.7.5|1.7.7|patch
opentelemetry-api|1.45.0|1.45.1|patch
opentelemetry-sdk|1.45.0|1.45.1|patch
opentelemetry-proto|1.45.0|1.45.1|patch
smart_open|8.0.2|8.0.4|patch
distlib|0.4.3|0.4.4|patch
python-discovery|1.6.1|1.6.4|patch
virtualenv|21.14.5|21.14.6|patch
gdown|6.4.1|6.4.2|patch
markdown|3.11|3.11.2|patch
imageio|2.38.0|2.38.1|patch
charls|2.4.4|2.4.5|patch
truststore|0.10.4|0.10.5|patch
smart-open|8.0.2|8.0.4|patch
spacy|3.8.14|3.8.16|patch
cachetools|7.2.1|7.2.4|patch
entrypoints|0.4|0.4.2|patch
rich-toolkit|0.20.5|0.20.6|patch
opentelemetry-exporter-otlp-proto-common|1.45.0|1.45.1|patch
opentelemetry-exporter-otlp-proto-http|1.45.0|1.45.1|patch
gitpython|3.2.0|3.2.1|patch
iniconfig|2.3.0|2.3.1|patch
jupyterlab-chat|0.25.1|0.25.2|patch
jupyter-ai-acp-client|0.3.2|0.3.3|patch
jupyter-live-content|0.1.1|0.1.2|patch
langsmith|0.14.4|0.14.11|patch
panel-material-ui|0.16.1|0.16.5|patch
pyspnego|0.12.2|0.12.4|patch
libsystemd0|262|262.1|
libudev1|262|262.1|
opentelemetry-semantic-conventions|0.66b0|0.66b1|
opentelemetry-exporter-prometheus|0.66b0|0.66b1|
opentelemetry-exporter-http-transport|0.66b0|0.66b1|
opentelemetry-exporter-otlp-common|0.66b0|0.66b1|
opentelemetry-instrumentation|0.66b0|0.66b1|
opentelemetry-instrumentation-threading|0.66b0|0.66b1|

### Removed

Package | Last Version
---|---
rsa|4.9.1
google-api-core-grpc|2.29.0
