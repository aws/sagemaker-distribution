# Change log: 4.2.14 (gpu)

This page lists all package changes since the previous release (4.2.13).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
boto3|1.43.106|1.43.117|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
multidict|6.9.1|7.2.1|major
smart_open|8.0.4|9.0.0|major
smart-open|8.0.4|9.0.0|major
simdjson|4.0.7|3.13.0|major
libexpat|2.8.5|2.9.0|minor
python-tzdata|2026.5|2026.6|minor
libnghttp2|1.68.1|1.70.0|minor
nlohmann_json|3.12.0|3.11.3|minor
aiobotocore|3.9.2|3.10.0|minor
narwhals|2.27.1|2.28.0|minor
pycparser|3.11|3.12|minor
platformdirs|4.13.5|4.14.0|minor
jsonpointer|3.4|3.6|minor
pandoc|3.12.1|3.13|minor
expat|2.8.5|2.9.0|minor
fonttools|4.67.0|4.68.0|minor
gdown|6.4.2|6.5.1|minor
black|26.5.1|26.10.1|minor
bokeh|3.9.2|3.10.0|minor
fmt|11.2.0|11.1.4|minor
cpp-expected|1.3.1|1.1.0|minor
libarchive|3.8.1|3.7.7|minor
libmamba|2.3.2|2.2.0|minor
libmambapy|2.3.2|2.2.0|minor
coverage|7.16.2|7.17.0|minor
cyclopts|5.2.0|5.3.2|minor
databricks-sdk|0.155.0|0.158.0|minor
dnspython|2.8.0|2.9.0|minor
sse-starlette|3.5.0|3.6.0|minor
jiter|0.17.0|0.18.0|minor
ml_dtypes|0.5.4|0.6.0|minor
panel-core|1.9.4|1.10.0|minor
panel|1.9.4|1.10.0|minor
pytest|9.1.1|9.2.0|minor
sagemaker-core|2.26.0|2.27.0|minor
sqlglot|30.23.0|30.25.0|minor
ca-certificates|2026.10.19|2026.10.23|patch
cpython|3.12.15|3.12.16|patch
python-gil|3.12.15|3.12.16|patch
hf-xet|1.7.0|1.7.1|patch
certifi|2026.10.19|2026.10.23|patch
brotli-python|1.1.0|1.1.1|patch
libbrotlicommon|1.1.0|1.1.1|patch
libbrotlidec|1.1.0|1.1.1|patch
libbrotlienc|1.1.0|1.1.1|patch
libjpeg-turbo|3.2.0|3.2.1|patch
botocore|1.43.106|1.43.117|patch
caio|0.12.9|0.12.10|patch
alembic|1.20.0|1.20.1|patch
soupsieve|3.0.3|3.0.4|patch
wcwidth|0.9.3|0.9.4|patch
nest-asyncio2|1.7.3|1.7.4|patch
scramp|1.4.17|1.4.18|patch
fastcore|2.2.33|2.2.35|patch
brotli-bin|1.1.0|1.1.1|patch
brotli|1.1.0|1.1.1|patch
pyasn1|0.6.4|0.6.5|patch
msgpack-python|1.2.3|1.2.4|patch
python-discovery|1.6.4|1.6.7|patch
libaec|1.1.5|1.1.7|patch
confection|1.3.3|1.3.4|patch
murmurhash|1.0.15|1.0.16|patch
srsly|2.5.3|2.5.5|patch
weasel|1.0.0|1.0.1|patch
cachetools|7.2.4|7.2.7|patch
libsolv|0.7.40|0.7.41|patch
pydantic-settings|2.16.1|2.16.2|patch
griffelib|2.4.0|2.4.1|patch
jupyter-ai-acp-client|0.3.3|0.3.4|patch
langsmith|0.14.12|0.14.16|patch
panel-material-ui|0.16.5|0.16.6|patch
tzlocal|5.4.4|5.4.5|patch
tzdata|2026c|2026e|

### Removed

Package | Last Version
---|---
nlohmann_json-abi|3.12.0
