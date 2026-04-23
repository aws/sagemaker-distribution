# Change log: 4.0.0 (cpu)

This page lists all package changes since the previous release (3.9.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
altair|5.5.0|6.0.0|major
pip|25.3|26.0.1|major
conda|25.11.1|26.3.1|major
docker-cli|27.5.1|29.4.0|major
jupyter-collaboration|3.1.2|4.3.0|major
mlflow|2.22.0|3.11.1|major
s3fs|2024.12.0|2026.3.0|major
sagemaker-python-sdk|2.245.0|3.7.1|major
pytorch|2.6.0|2.8.0|minor
boto3|1.37.3|1.42.70|minor
jupyter-scheduler|2.11.0|2.12.0|minor
amazon-sagemaker-jupyter-scheduler|3.1.16|3.2.0|minor
amazon_sagemaker_sql_editor|0.1.21|0.2.1|minor
torchvision|0.21.0|0.24.0|minor
uvicorn|0.41.0|0.44.0|minor
aws-s3-access-grants-boto3-plugin|1.2.0|1.3.0|minor
jupyter-server-proxy|4.4.0|4.5.0|minor
keras|3.13.2|3.14.0|minor
mcp|1.26.0|1.27.0|minor
tensorflow|2.18.0|2.19.1|minor
uv|0.10.8|0.11.4|minor
python|3.12.9|3.12.13|patch
jupyter-lsp|2.3.0|2.3.1|patch
jupyterlab|4.5.5|4.5.6|patch
sagemaker-jupyterlab-extension-common|0.3.0|0.3.3|patch
notebook|7.5.4|7.5.5|patch
fastapi|0.135.1|0.135.3|patch
langchain-aws|0.2.19|0.2.35|patch
sagemaker-code-editor|1.9.2|1.9.4|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.14|1.0.15|patch
sagemaker-jupyterlab-extension|0.5.2|0.5.4|patch
sagemaker-studio-dataengineering-extensions|1.3.7|1.3.8|patch
sagemaker-studio-dataengineering-sessions|1.3.13|1.3.18|patch

### Removed

Package | Last Version
---|---
aioboto3|14.3.0
tf-keras|2.18.0

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
fsspec|2024.12.0|2026.3.0|major
packaging|24.2|25.0|major
tbb|2021.13.0|2022.3.0|major
mkl|2024.2.2|2025.3.1|major
libabseil|20240722.0|20250512.1|major
libprotobuf|5.28.3|6.31.1|major
python-tzdata|2025.3|2026.1|major
libarrow|19.0.1|21.0.0|major
libarrow-acero|19.0.1|21.0.0|major
libparquet|19.0.1|21.0.0|major
libarrow-dataset|19.0.1|21.0.0|major
libarrow-substrait|19.0.1|21.0.0|major
pyarrow-core|19.0.1|21.0.0|major
pyarrow|19.0.1|21.0.0|major
harfbuzz|11.2.1|12.2.0|major
attrs|23.2.0|26.1.0|major
aiobotocore|2.22.0|3.3.0|major
protobuf|5.28.3|6.31.1|major
cryptography|46.0.5|44.0.3|major
pyopenssl|25.3.0|24.3.0|major
graphviz|12.2.1|13.1.2|major
starlette|0.52.1|1.0.0|major
confection|0.1.5|1.3.3|major
weasel|0.4.3|1.0.0|major
xyzservices|2025.11.0|2026.3.0|major
cachetools|5.5.2|6.2.6|major
conda-libmamba-solver|25.11.0|26.3.0|major
invoke|2.2.1|3.0.3|major
flatbuffers|24.12.23|25.2.10|major
jupyter-collaboration-ui|1.1.2|2.3.0|major
jupyter-docprovider|1.1.2|2.3.0|major
jupyter_server_ydoc|1.1.2|2.3.0|major
mlflow-skinny|2.22.0|3.11.1|major
mlflow-ui|2.22.0|3.11.1|major
sagemaker-core|1.0.76|2.7.1|major
libffi|3.4.6|3.5.2|minor
libsqlite|3.48.0|3.52.0|minor
libuuid|2.41.3|2.42|minor
hf-xet|1.2.1|1.4.3|minor
requests|2.32.5|2.33.1|minor
libblas|3.9.0|3.11.0|minor
libcblas|3.9.0|3.11.0|minor
liblapack|3.9.0|3.11.0|minor
libtorch|2.6.0|2.8.0|minor
mpc|1.3.1|1.4.0|minor
gmpy2|2.2.1|2.3.0|minor
aws-c-cal|0.8.7|0.9.2|minor
aws-c-io|0.17.0|0.22.0|minor
aws-c-http|0.9.4|0.10.4|minor
aws-c-auth|0.8.6|0.9.1|minor
aws-c-mqtt|0.12.2|0.13.3|minor
aws-c-s3|0.7.13|0.8.6|minor
aws-crt-cpp|0.31.0|0.34.4|minor
libnghttp2|1.67.0|1.68.1|minor
azure-core-cpp|1.14.0|1.16.0|minor
azure-identity-cpp|1.10.0|1.12.0|minor
azure-storage-common-cpp|12.8.0|12.10.0|minor
azure-storage-blobs-cpp|12.13.0|12.14.0|minor
libgrpc|1.67.1|1.73.1|minor
libgoogle-cloud|2.36.0|2.39.0|minor
libgoogle-cloud-storage|2.36.0|2.39.0|minor
libopentelemetry-cpp-headers|1.18.0|1.21.0|minor
libopentelemetry-cpp|1.18.0|1.21.0|minor
orc|2.1.1|2.2.1|minor
libutf8proc|2.10.0|2.11.3|minor
libthrift|0.21.0|0.22.0|minor
pcre2|10.44|10.46|minor
libglib|2.84.1|2.86.2|minor
lerc|4.0.0|4.1.0|minor
gdk-pixbuf|2.42.12|2.44.4|minor
botocore|1.37.3|1.42.70|minor
narwhals|2.17.0|2.19.0|minor
s3transfer|0.11.3|0.16.0|minor
async-lru|2.2.0|2.3.0|minor
anyio|4.12.1|4.13.0|minor
pygments|2.19.2|2.20.0|minor
jsonpointer|3.0.0|3.1.1|minor
json5|0.13.0|0.14.0|minor
libfaiss|1.9.0|1.10.0|minor
faiss|1.9.0|1.10.0|minor
faiss-cpu|1.9.0|1.10.0|minor
click|8.3.1|8.2.1|minor
dask-core|2026.1.2|2026.3.0|minor
distributed|2026.1.2|2026.3.0|minor
pyjwt|2.11.0|2.12.1|minor
regex|2026.2.28|2026.4.4|minor
jupyter_scheduler|2.11.0|2.12.0|minor
snowflake-connector-python|3.17.4|3.13.2|minor
apsw|3.48.0.0|3.52.0.0|minor
dbus|1.13.6|1.16.2|minor
fonttools|4.61.1|4.62.0|minor
kiwisolver|1.4.9|1.5.0|minor
wayland|1.24.0|1.25.0|minor
qt6-main|6.8.2|6.9.2|minor
pyside6|6.8.2|6.9.2|minor
grpcio|1.67.1|1.73.1|minor
google-auth|2.48.0|2.49.1|minor
googleapis-common-protos|1.72.0|1.74.0|minor
google-api-core|2.29.0|2.30.2|minor
opentelemetry-api|1.39.1|1.40.0|minor
opentelemetry-sdk|1.39.1|1.40.0|minor
ray-core|2.44.1|2.53.0|minor
python-discovery|1.1.0|1.2.2|minor
virtualenv|21.1.0|21.2.0|minor
ray-default|2.44.1|2.53.0|minor
ray-tune|2.44.1|2.53.0|minor
binaryornot|0.4.4|0.6.0|minor
nss|3.108|3.118|minor
tensorboard|2.18.0|2.19.0|minor
glib-tools|2.84.1|2.86.2|minor
python-fasthtml|0.12.47|0.13.3|minor
plum-dispatch|2.7.1|2.8.0|minor
ujson|5.11.0|5.12.0|minor
llvmlite|0.46.0|0.47.0|minor
numba|0.64.0|0.65.0|minor
optuna|4.7.0|4.8.0|minor
black|26.1.0|26.3.1|minor
bokeh|3.8.2|3.9.0|minor
databricks-sdk|0.73.0|0.102.0|minor
dnspython|2.8.0|2.7.0|minor
python-duckdb|1.4.4|1.5.1|minor
duckdb|1.4.4|1.5.1|minor
uvicorn-standard|0.41.0|0.44.0|minor
grpcio-status|1.67.1|1.73.1|minor
google-cloud-bigquery-core|3.40.1|3.18.0|minor
h5py|3.15.1|3.16.0|minor
pycrdt-websocket|0.15.5|0.16.0|minor
ml_dtypes|0.4.0|0.5.4|minor
pyspnego|0.11.2|0.12.1|minor
pytest-cov|7.0.0|7.1.0|minor
slack-sdk|3.40.1|3.41.0|minor
slack-bolt|1.27.0|1.28.0|minor
tensorflow-base|2.18.0|2.19.1|minor
tensorflow-estimator|2.18.0|2.19.1|minor
llvm-openmp|22.1.0|22.1.2|patch
libzlib|1.3.1|1.3.2|patch
libexpat|2.7.4|2.7.5|patch
openssl|3.6.1|3.6.2|patch
filelock|3.25.0|3.25.2|patch
charset-normalizer|3.4.5|3.4.7|patch
setuptools|82.0.0|82.0.1|patch
mpfr|4.2.1|4.2.2|patch
mpmath|1.4.0|1.4.1|patch
aws-c-common|0.12.0|0.12.4|patch
s2n|1.5.14|1.5.26|patch
aws-c-sdkutils|0.2.3|0.2.4|patch
aws-checksums|0.2.3|0.2.7|patch
aws-c-event-stream|0.5.4|0.5.6|patch
aws-sdk-cpp|1.11.510|1.11.606|patch
zlib|1.3.1|1.3.2|patch
libpng|1.6.55|1.6.56|patch
libfreetype6|2.14.2|2.14.3|patch
libfreetype|2.14.2|2.14.3|patch
freetype|2.14.2|2.14.3|patch
pango|1.56.3|1.56.4|patch
aiohttp|3.13.3|3.13.5|patch
sqlalchemy|2.0.48|2.0.49|patch
tomli|2.4.0|2.4.1|patch
platformdirs|4.9.2|4.9.4|patch
tornado|6.5.4|6.5.5|patch
nbconvert-core|7.17.0|7.17.1|patch
orjson|3.11.7|3.11.8|patch
langsmith|0.7.14|0.7.26|patch
pandoc|3.9|3.9.0.2|patch
nbconvert-pandoc|7.17.0|7.17.1|patch
nbconvert|7.17.0|7.17.1|patch
pyathena|3.30.0|3.30.1|patch
fastcore|1.12.23|1.12.34|patch
pyasn1|0.6.2|0.6.3|patch
proto-plus|1.27.1|1.27.2|patch
libsentencepiece|0.2.0|0.2.1|patch
sentencepiece-python|0.2.0|0.2.1|patch
sentencepiece-spm|0.2.0|0.2.1|patch
sentencepiece|0.2.0|0.2.1|patch
nltk|3.9.3|3.9.4|patch
libavif16|1.4.0|1.4.1|patch
werkzeug|3.1.6|3.1.8|patch
python-multipart|0.0.22|0.0.24|patch
preshed|3.0.12|3.0.13|patch
srsly|2.5.2|2.5.3|patch
thinc|8.3.10|8.3.13|patch
typer|0.24.0|0.24.1|patch
spacy|3.8.11|3.8.14|patch
libsolv|0.7.35|0.7.36|patch
coverage|7.13.4|7.13.5|patch
fastapi-core|0.135.1|0.135.3|patch
pydantic-extra-types|2.11.0|2.11.2|patch
smmap|5.0.2|5.0.3|patch
pycrdt|0.12.47|0.12.50|patch
sse-starlette|3.3.2|3.3.4|patch
panel|1.8.9|1.8.10|patch
pydynamodb|0.8.1|0.8.2|patch
pyroaring|1.0.3|1.0.4|patch
pytest|9.0.2|9.0.3|patch
libre2-11|2024.07.02|2025.11.05|
re2|2024.07.02|2025.11.05|
opentelemetry-semantic-conventions|0.60b1|0.61b0|
poppler|25.02.0|25.12.0|
opentelemetry-instrumentation|0.60b1|0.61b0|
opentelemetry-instrumentation-threading|0.60b1|0.61b0|

### New

Package | Version
---|---
_x86_64-microarch-level|4
libarrow-compute|21.0.0
libclang-cpp21.1|21.1.0
opentelemetry-exporter-prometheus|0.61b0
opentelemetry-proto|1.40.0
orderly-set|5.5.0
deepdiff|9.0.0
flask-cors|6.0.2
huey|2.6.0
pycrdt-store|0.1.3
libml_dtypes-headers|0.5.4
libtensorflow_framework|2.19.1
libtensorflow_cc|2.19.1
prettytable|3.17.0
skops|0.13.0
onnx|1.20.0
python-rapidjson|1.23
sagemaker-schema-inference-artifacts|0.0.5
sagemaker-train|1.7.1
tritonclient|2.41.1
sagemaker-serve|1.7.1
sagemaker-mlops|1.7.1

### Removed

Package | Last Version
---|---
aiofiles|25.1.0
pycalverter|1.6.1
sqlite|3.48.0
expat|2.7.4
libllvm19|19.1.7
libclang-cpp19.1|19.1.7
mysql-common|9.0.1
mysql-libs|9.0.1
setproctitle|1.3.7
chardet|5.2.0
google-api-core-grpc|2.29.0
pox|0.3.7
ppft|1.7.8
pathos|0.3.5
