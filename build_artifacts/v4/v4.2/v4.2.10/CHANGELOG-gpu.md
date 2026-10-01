# Change log: 4.2.10 (gpu)

This page lists all package changes since the previous release (4.2.9).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.10|4.5.11|patch
sagemaker-jupyterlab-extension-common|0.4.8|0.4.9|patch
sagemaker-studio-dataengineering-extensions|1.3.14|1.3.15|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
adwaita-icon-theme|50.0|51.0|major
unicodedata2|17.0.1|18.0.0|major
oauthlib|3.3.1|4.0.0|major
cyclopts|4.25.2|5.1.0|major
deprecated|1.3.1|3.0.0|major
idna|3.19|3.20|minor
nccl|2.30.7.1|2.32.3.1|minor
networkx|3.6.1|3.7|minor
python-tzdata|2026.3|2026.4|minor
wrapt|2.4.0|2.5.0|minor
platformdirs|4.11.8|4.12.2|minor
fqdn|1.5.1|1.6.0|minor
soupsieve|2.9.2|2.10|minor
pandoc|3.11|3.12|minor
wcwidth|0.8.3|0.9.1|minor
ipykernel|7.3.0|7.4.0|minor
pyjwt|2.13.0|2.15.1|minor
fonttools|4.65.0|4.66.1|minor
google-auth|2.58.0|2.59.0|minor
google-api-core|2.33.0|2.29.0|minor
opentelemetry-proto|1.44.0|1.45.0|minor
virtualenv|21.7.9|21.14.1|minor
threadpoolctl|3.6.0|3.7.0|minor
gdown|6.2.0|6.4.1|minor
markdown|3.10.3|3.11|minor
imageio|2.37.4|2.38.0|minor
lazy-loader|0.5|0.6|minor
colorlog|6.11.0|6.12.0|minor
cachetools|7.1.8|7.2.0|minor
conda-pypi|0.12.0|0.13.0|minor
conda-self|0.2.1|0.3.0|minor
rich-rst|2.1.0|2.2.0|minor
databricks-sdk|0.138.0|0.143.0|minor
watchfiles|1.2.0|1.3.0|minor
sse-starlette|3.4.11|3.5.0|minor
gitpython|3.1.62|3.2.0|minor
google-resumable-media|2.10.2|2.11.0|minor
google-cloud-bigquery-core|3.18.0|3.45.2|minor
langsmith|0.12.4|0.14.1|minor
skops|0.14|0.16.0|minor
panel-material-ui|0.14.1|0.16.0|minor
pytoolconfig|1.2.5|1.3.1|minor
rope|1.14.0|1.15.0|minor
sqlalchemy-bigquery|1.16.0|1.17.2|minor
sqlglot|30.18.0|30.20.0|minor
trino-python-client|0.339.0|0.340.0|minor
llvm-openmp|23.1.1|23.1.2|patch
libexpat|2.8.1|2.8.5|patch
libuuid|2.42.3|2.42.4|patch
charset-normalizer|3.5.1|3.5.2|patch
libpng|1.6.58|1.6.59|patch
fribidi|1.0.16|1.0.17|patch
caio|0.12.4|0.12.9|patch
mako|1.4.1|1.4.3|patch
greenlet|3.5.5|3.5.6|patch
sqlalchemy|2.0.52|2.0.54|patch
tornado|6.5.8|6.5.10|patch
debugpy|1.8.21|1.8.22|patch
nest-asyncio2|1.7.2|1.7.3|patch
jupyterlab_server|2.28.0|2.28.1|patch
ansi2html|1.9.2|1.9.5|patch
fastcore|2.2.25|2.2.31|patch
arro3-core|0.8.2|0.8.3|patch
expat|2.8.1|2.8.5|patch
pyparsing|3.3.2|3.3.3|patch
msgpack-python|1.2.2|1.2.3|patch
smart_open|8.0.1|8.0.2|patch
python-discovery|1.6.0|1.6.1|patch
regex|2026.9.10|2026.9.29|patch
werkzeug|3.1.8|3.1.9|patch
smart-open|8.0.1|8.0.2|patch
libsolv|0.7.39|0.7.40|patch
conda-lockfiles|0.2.1|0.2.2|patch
python-build|1.6.0|1.6.1|patch
coverage|7.16.0|7.16.2|patch
deltalake|1.6.3|1.6.6|patch
graphql-core|3.2.12|3.2.13|patch
isort|9.0.1|9.0.2|patch
jupyterlab-chat|0.25.0|0.25.1|patch
jupyter-ai-persona-manager|0.2.0|0.2.2|patch
jupyter-ai-acp-client|0.3.0|0.3.1|patch
pylint|4.0.8|4.0.10|patch
pymysql|1.2.0|1.2.3|patch
libsystemd0|261.3|262|
libudev1|261.3|262|

### New

Package | Version
---|---
python-abi3|3.12
google-api-core-grpc|2.29.0
