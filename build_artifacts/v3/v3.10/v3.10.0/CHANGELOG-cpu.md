# Change log: 3.10.0 (cpu)

This page lists all package changes since the previous release (3.9.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
uvicorn|0.41.0|0.42.0|minor
jupyter-server-proxy|4.4.0|4.5.0|minor
uv|0.10.8|0.11.2|minor
jupyterlab|4.5.5|4.5.6|patch
sagemaker-jupyterlab-extension-common|0.3.0|0.3.3|patch
notebook|7.5.4|7.5.5|patch
fastapi|0.135.1|0.135.3|patch
sagemaker-code-editor|1.9.2|1.9.4|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.14|1.0.15|patch
sagemaker-jupyterlab-extension|0.5.2|0.5.4|patch
sagemaker-studio-dataengineering-extensions|1.3.7|1.3.8|patch
sagemaker-studio-dataengineering-sessions|1.3.13|1.3.18|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
starlette|0.52.1|1.0.0|major
confection|0.1.5|1.3.3|major
weasel|0.4.3|1.0.0|major
xyzservices|2025.11.0|2026.3.0|major
libuuid|2.41.3|2.42|minor
hf-xet|1.2.1|1.4.3|minor
requests|2.32.5|2.33.1|minor
mpc|1.3.1|1.4.0|minor
gmpy2|2.2.1|2.3.0|minor
libnghttp2|1.67.0|1.68.1|minor
lerc|4.0.0|4.1.0|minor
narwhals|2.17.0|2.18.1|minor
async-lru|2.2.0|2.3.0|minor
anyio|4.12.1|4.13.0|minor
pygments|2.19.2|2.20.0|minor
jsonpointer|3.0.0|3.1.1|minor
json5|0.13.0|0.14.0|minor
libfaiss|1.9.0|1.10.0|minor
faiss|1.9.0|1.10.0|minor
faiss-cpu|1.9.0|1.10.0|minor
dask-core|2026.1.2|2026.3.0|minor
distributed|2026.1.2|2026.3.0|minor
pyjwt|2.11.0|2.12.1|minor
regex|2026.2.28|2026.3.32|minor
fonttools|4.61.1|4.62.0|minor
kiwisolver|1.4.9|1.5.0|minor
google-auth|2.48.0|2.49.1|minor
googleapis-common-protos|1.72.0|1.73.1|minor
python-discovery|1.1.0|1.2.1|minor
virtualenv|21.1.0|21.2.0|minor
binaryornot|0.4.4|0.6.0|minor
python-fasthtml|0.12.47|0.13.2|minor
plum-dispatch|2.7.1|2.8.0|minor
ujson|5.11.0|5.12.0|minor
llvmlite|0.46.0|0.47.0|minor
numba|0.64.0|0.65.0|minor
optuna|4.7.0|4.8.0|minor
black|26.1.0|26.3.1|minor
bokeh|3.8.2|3.9.0|minor
python-duckdb|1.4.4|1.5.1|minor
duckdb|1.4.4|1.5.1|minor
uvicorn-standard|0.41.0|0.42.0|minor
google-cloud-bigquery-core|3.40.1|3.41.0|minor
h5py|3.15.1|3.16.0|minor
opentelemetry-api|1.39.1|1.40.0|minor
opentelemetry-sdk|1.39.1|1.40.0|minor
pyspnego|0.11.2|0.12.1|minor
pytest-cov|7.0.0|7.1.0|minor
slack-sdk|3.40.1|3.41.0|minor
llvm-openmp|22.1.0|22.1.2|patch
libzlib|1.3.1|1.3.2|patch
libexpat|2.7.4|2.7.5|patch
filelock|3.25.0|3.25.2|patch
charset-normalizer|3.4.5|3.4.6|patch
setuptools|82.0.0|82.0.1|patch
mpfr|4.2.1|4.2.2|patch
mpmath|1.4.0|1.4.1|patch
zlib|1.3.1|1.3.2|patch
libpng|1.6.55|1.6.56|patch
libfreetype6|2.14.2|2.14.3|patch
libfreetype|2.14.2|2.14.3|patch
freetype|2.14.2|2.14.3|patch
aiohttp|3.13.3|3.13.5|patch
tomli|2.4.0|2.4.1|patch
platformdirs|4.9.2|4.9.4|patch
tornado|6.5.4|6.5.5|patch
orjson|3.11.7|3.11.8|patch
langsmith|0.7.14|0.7.24|patch
pandoc|3.9|3.9.0.2|patch
pyathena|3.30.0|3.30.1|patch
fastcore|1.12.23|1.12.34|patch
expat|2.7.4|2.7.5|patch
pyasn1|0.6.2|0.6.3|patch
proto-plus|1.27.1|1.27.2|patch
nltk|3.9.3|3.9.4|patch
libavif16|1.4.0|1.4.1|patch
werkzeug|3.1.6|3.1.7|patch
preshed|3.0.12|3.0.13|patch
srsly|2.5.2|2.5.3|patch
thinc|8.3.10|8.3.13|patch
spacy|3.8.11|3.8.14|patch
libsolv|0.7.35|0.7.36|patch
coverage|7.13.4|7.13.5|patch
fastapi-core|0.135.1|0.135.3|patch
pydantic-extra-types|2.11.0|2.11.1|patch
pycrdt|0.12.47|0.12.50|patch
sse-starlette|3.3.2|3.3.4|patch
panel|1.8.9|1.8.10|patch
pyroaring|1.0.3|1.0.4|patch
opentelemetry-semantic-conventions|0.60b1|0.61b0|
opentelemetry-instrumentation|0.60b1|0.61b0|
opentelemetry-instrumentation-threading|0.60b1|0.61b0|

### Removed

Package | Last Version
---|---
chardet|5.2.0
