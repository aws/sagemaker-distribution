# Change log: 2.14.2 (gpu)

This page lists all package changes since the previous release (2.14.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyter-lsp|2.3.0|2.3.1|patch
sagemaker-jupyterlab-extension-common|0.3.2|0.3.3|patch
fastapi|0.135.2|0.135.3|patch
sagemaker-code-editor|1.9.2|1.9.4|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.14|1.0.15|patch
sagemaker-studio|1.1.8|1.1.12|patch
sagemaker-studio-dataengineering-sessions|1.3.14|1.3.18|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python-tzdata|2025.3|2026.1|major
importlib_resources|6.5.2|7.1.0|major
gdown|5.2.1|6.0.0|major
xyzservices|2025.11.0|2026.3.0|major
invoke|2.2.1|3.0.3|major
libuuid|2.41.3|2.42|minor
requests|2.32.5|2.33.1|minor
mpc|1.3.1|1.4.0|minor
greenlet|3.3.2|3.4.0|minor
narwhals|2.18.1|2.19.0|minor
pygments|2.19.2|2.20.0|minor
prometheus_client|0.24.1|0.25.0|minor
json5|0.13.0|0.14.0|minor
pydantic-core|2.41.5|2.46.0|minor
pydantic|2.12.5|2.13.0|minor
regex|2026.2.28|2026.4.4|minor
googleapis-common-protos|1.73.0|1.74.0|minor
smart_open|7.5.1|7.6.0|minor
smart-open|7.5.1|7.6.0|minor
llvmlite|0.46.0|0.47.0|minor
numba|0.64.0|0.65.0|minor
awswrangler|3.15.1|3.16.0|minor
deltalake|1.3.2|1.5.0|minor
google-cloud-bigquery-core|3.40.1|3.41.0|minor
jupyter-docprovider|2.2.1|2.3.0|minor
opentelemetry-api|1.40.0|1.41.0|minor
opentelemetry-sdk|1.40.0|1.41.0|minor
slack-bolt|1.27.0|1.28.0|minor
llvm-openmp|22.1.1|22.1.3|patch
libexpat|2.7.4|2.7.5|patch
liblzma|5.8.2|5.8.3|patch
openssl|3.6.1|3.6.2|patch
hf-xet|1.4.2|1.4.3|patch
charset-normalizer|3.4.6|3.4.7|patch
libpng|1.6.55|1.6.57|patch
libjpeg-turbo|3.1.2|3.1.4.1|patch
aiohttp|3.13.3|3.13.5|patch
sqlalchemy|2.0.48|2.0.49|patch
tomli|2.4.0|2.4.1|patch
platformdirs|4.9.4|4.9.6|patch
nbconvert-core|7.17.0|7.17.1|patch
click|8.3.1|8.3.2|patch
orjson|3.11.7|3.11.8|patch
langsmith|0.7.22|0.7.30|patch
nbconvert-pandoc|7.17.0|7.17.1|patch
nbconvert|7.17.0|7.17.1|patch
cryptography|46.0.5|46.0.7|patch
pyathena|3.30.0|3.30.1|patch
fastcore|1.12.31|1.12.37|patch
expat|2.7.4|2.7.5|patch
google-auth|2.49.1|2.49.2|patch
proto-plus|1.27.1|1.27.2|patch
python-discovery|1.2.0|1.2.2|patch
virtualenv|21.2.0|21.2.1|patch
rich|14.3.3|14.3.4|patch
werkzeug|3.1.7|3.1.8|patch
python-multipart|0.0.22|0.0.26|patch
python-fasthtml|0.13.0|0.13.3|patch
typer|0.24.0|0.24.1|patch
spacy|3.8.13|3.8.14|patch
python-duckdb|1.5.1|1.5.2|patch
duckdb|1.5.1|1.5.2|patch
fastapi-core|0.135.2|0.135.3|patch
pydantic-extra-types|2.11.1|2.11.2|patch
smmap|5.0.2|5.0.3|patch
sse-starlette|3.3.3|3.3.4|patch
param|2.3.2|2.3.3|patch
pydynamodb|0.8.1|0.8.2|patch
pytest|9.0.2|9.0.3|patch
opentelemetry-semantic-conventions|0.61b0|0.62b0|
opentelemetry-instrumentation|0.61b0|0.62b0|
opentelemetry-instrumentation-threading|0.61b0|0.62b0|

### New

Package | Version
---|---
sqlglot|28.10.1
