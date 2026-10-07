# Change log: 4.4.6 (gpu)

This page lists all package changes since the previous release (4.4.5).

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
conda|26.7.2|26.7.3|patch
sagemaker-code-editor|1.10.1|1.10.3|patch
sagemaker-studio-dataengineering-sessions|1.3.25|1.3.27|patch
uv|0.12.17|0.12.21|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
oauthlib|3.3.1|4.0.0|major
cyclopts|4.25.2|5.2.0|major
deprecated|1.3.1|3.0.0|major
nccl|2.30.7.1|2.32.3.1|minor
python-tzdata|2026.3|2026.5|minor
yarl|1.24.5|1.25.1|minor
wrapt|2.4.1|2.5.0|minor
narwhals|2.26.0|2.27.0|minor
platformdirs|4.11.11|4.12.3|minor
fqdn|1.5.1|1.6.0|minor
jsonpointer|3.1.1|3.2.0|minor
soupsieve|2.9.2|2.10|minor
pandoc|3.11|3.12|minor
wcwidth|0.8.4|0.9.2|minor
ipykernel|7.3.0|7.4.0|minor
pyjwt|2.14.0|2.15.1|minor
tenacity|9.1.4|9.2.1|minor
pyathena|3.36.0|3.38.0|minor
arro3-core|0.8.2|0.9.0|minor
fonttools|4.65.0|4.66.1|minor
google-auth|2.58.0|2.60.0|minor
opentelemetry-api|1.44.0|1.45.0|minor
opentelemetry-sdk|1.44.0|1.45.0|minor
opentelemetry-proto|1.44.0|1.45.1|minor
virtualenv|21.10.0|21.14.5|minor
markdown|3.10.3|3.11|minor
imageio|2.37.4|2.38.0|minor
lazy-loader|0.5|0.6|minor
starlette|1.6.0|1.7.0|minor
cloudpathlib|0.25.0|0.26.0|minor
llvmlite|0.49.0|0.50.0|minor
numba|0.67.0|0.68.0|minor
colorlog|6.11.0|6.12.0|minor
tomli|2.4.1|2.5.0|minor
conda-pypi|0.12.0|0.13.0|minor
py-rattler|0.25.0|0.26.0|minor
conda-rattler-solver|0.1.1|0.2.0|minor
rich-rst|2.1.0|2.2.0|minor
databricks-sdk|0.138.0|0.147.0|minor
websockets|17.1|17.2|minor
sse-starlette|3.4.11|3.5.0|minor
openapi-pydantic|0.5.1|0.6.0|minor
gitpython|3.1.62|3.2.0|minor
google-resumable-media|2.10.2|2.11.0|minor
google-cloud-bigquery-core|3.45.0|3.46.1|minor
langsmith|0.13.0|0.14.4|minor
skops|0.15|0.16.0|minor
panel-material-ui|0.14.1|0.16.1|minor
thrift|0.24.0|0.25.0|minor
rope|1.14.0|1.15.0|minor
sagemaker-core|2.21.0|2.23.0|minor
sqlglot|30.18.0|30.21.0|minor
trino-python-client|0.339.0|0.340.0|minor
slack-sdk|3.44.1|3.45.0|minor
llvm-openmp|23.1.1|23.1.3|patch
libexpat|2.8.4|2.8.5|patch
libpython|3.12.14|3.12.15|patch
libuuid|2.42.3|2.42.4|patch
openssl|3.6.4|3.6.5|patch
cpython|3.12.14|3.12.15|patch
python-gil|3.12.14|3.12.15|patch
charset-normalizer|3.5.1|3.5.2|patch
markupsafe|3.0.3|3.0.4|patch
gmpy2|2.3.1|2.3.2|patch
libedit|3.1.20250104|3.1.20260512|patch
libpng|1.6.58|1.6.59|patch
propcache|0.5.2|0.5.4|patch
aiohttp|3.14.3|3.14.4|patch
botocore|1.43.75|1.43.106|patch
aiobotocore|3.9.1|3.9.2|patch
caio|0.12.4|0.12.9|patch
zipp|4.1.0|4.1.1|patch
mako|1.4.1|1.4.3|patch
pandocfilters|1.5.0|1.5.1|patch
nest-asyncio2|1.7.2|1.7.3|patch
ansi2html|1.9.2|1.9.5|patch
archspec|0.2.5|0.2.6|patch
expat|2.8.4|2.8.5|patch
msgpack-python|1.2.2|1.2.3|patch
smart_open|8.0.1|8.0.2|patch
gdown|6.4.0|6.4.1|patch
regex|2026.9.10|2026.9.29|patch
werkzeug|3.1.8|3.1.9|patch
fastcore|2.2.29|2.2.33|patch
typer|0.27.2|0.27.3|patch
smart-open|8.0.1|8.0.2|patch
cachetools|7.2.0|7.2.1|patch
libsolv|0.7.39|0.7.40|patch
conda-lockfiles|0.2.1|0.2.2|patch
python-build|1.6.0|1.6.1|patch
coverage|7.16.1|7.16.2|patch
deltalake|1.6.3|1.6.6|patch
python-dotenv|1.2.3|1.2.4|patch
griffelib|2.3.0|2.3.2|patch
graphql-core|3.2.12|3.2.13|patch
isort|9.0.1|9.0.2|patch
jupyter-ai-persona-manager|0.2.0|0.2.2|patch
jupyter-ai-acp-client|0.3.0|0.3.2|patch
mmh3|5.3.0|5.3.1|patch
pylint|4.0.8|4.0.10|patch
pymysql|1.2.0|1.2.3|patch
sqlalchemy-bigquery|1.17.2|1.17.3|patch
libsystemd0|261.3|262|
libudev1|261.3|262|
opentelemetry-semantic-conventions|0.65b0|0.66b0|
opentelemetry-exporter-prometheus|0.65b0|0.66b0|
opentelemetry-instrumentation|0.65b0|0.66b0|
opentelemetry-instrumentation-threading|0.65b0|0.66b0|
