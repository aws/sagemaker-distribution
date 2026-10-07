# Change log: 4.3.8 (gpu)

This page lists all package changes since the previous release (4.3.7).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python|3.12.14|3.12.15|patch
boto3|1.43.75|1.43.106|patch
notebook|7.5.7|7.5.8|patch
aws-smus-cicd-cli|1.0.8|1.0.9|patch
sagemaker-code-editor|1.10.1|1.10.2|patch
sagemaker-studio-dataengineering-sessions|1.3.25|1.3.27|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python-tzdata|2026.4|2026.5|minor
yarl|1.24.5|1.25.1|minor
narwhals|2.26.0|2.27.0|minor
arro3-core|0.8.3|0.9.0|minor
google-auth|2.59.0|2.60.0|minor
google-api-core|2.29.0|2.33.0|minor
opentelemetry-api|1.44.0|1.45.0|minor
opentelemetry-sdk|1.44.0|1.45.0|minor
cloudpathlib|0.25.0|0.26.0|minor
llvmlite|0.49.0|0.50.0|minor
numba|0.67.0|0.68.0|minor
cyclopts|5.1.0|5.2.0|minor
databricks-sdk|0.143.0|0.147.0|minor
websockets|17.1|17.2|minor
openapi-pydantic|0.5.1|0.6.0|minor
google-cloud-bigquery-core|3.45.2|3.18.0|minor
thrift|0.24.0|0.25.0|minor
sagemaker-core|2.21.0|2.23.0|minor
sqlalchemy-bigquery|1.17.2|1.16.0|minor
sqlglot|30.20.0|30.21.0|minor
slack-sdk|3.44.1|3.45.0|minor
libpython|3.12.14|3.12.15|patch
openssl|3.6.4|3.6.5|patch
cpython|3.12.14|3.12.15|patch
python-gil|3.12.14|3.12.15|patch
markupsafe|3.0.3|3.0.4|patch
gmpy2|2.3.1|2.3.2|patch
libedit|3.1.20250104|3.1.20260512|patch
propcache|0.5.2|0.5.4|patch
aiohttp|3.14.3|3.14.4|patch
botocore|1.43.75|1.43.106|patch
aiobotocore|3.9.1|3.9.2|patch
zipp|4.1.0|4.1.1|patch
platformdirs|4.12.2|4.12.3|patch
pandocfilters|1.5.0|1.5.1|patch
wcwidth|0.9.1|0.9.2|patch
fastcore|2.2.31|2.2.33|patch
archspec|0.2.5|0.2.6|patch
opentelemetry-proto|1.45.0|1.45.1|patch
virtualenv|21.14.1|21.14.5|patch
typer|0.27.2|0.27.3|patch
cachetools|7.2.0|7.2.1|patch
python-dotenv|1.2.3|1.2.4|patch
griffelib|2.3.0|2.3.2|patch
jupyter-ai-acp-client|0.3.1|0.3.2|patch
langsmith|0.14.1|0.14.4|patch
mmh3|5.3.0|5.3.1|patch
panel-material-ui|0.16.0|0.16.1|patch
opentelemetry-semantic-conventions|0.65b0|0.66b0|
opentelemetry-exporter-prometheus|0.65b0|0.66b0|
opentelemetry-instrumentation|0.65b0|0.66b0|
opentelemetry-instrumentation-threading|0.65b0|0.66b0|

### Removed

Package | Last Version
---|---
google-api-core-grpc|2.29.0
