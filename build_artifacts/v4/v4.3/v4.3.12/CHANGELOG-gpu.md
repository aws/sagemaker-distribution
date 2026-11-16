# Change log: 4.3.12 (gpu)

This page lists all package changes since the previous release (4.3.11).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyter-activity-monitor-extension|0.3.2|0.3.3|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
pyzmq|26.4.0|27.3.0|major
soupsieve|3.0.4|4.0|major
simdjson|3.13.0|4.0.7|major
hf-xet|1.7.1|1.8.0|minor
libnghttp2|1.70.0|1.71.0|minor
nlohmann_json|3.11.3|3.12.0|minor
lerc|4.2.0|4.3.0|minor
anyio|4.15.1|4.16.0|minor
jsonpointer|3.6|3.8|minor
joserfc|1.7.7|1.8.0|minor
lcms2|2.19.1|2.20|minor
python-discovery|1.6.7|1.9.4|minor
awswrangler|3.17.1|3.18.0|minor
fmt|11.1.4|11.2.0|minor
cpp-expected|1.1.0|1.3.1|minor
libarchive|3.7.7|3.8.1|minor
libmamba|2.2.0|2.3.2|minor
libmambapy|2.2.0|2.3.2|minor
unearth|0.18.3|0.19.0|minor
frozendict|2.4.7|2.5.0|minor
databricks-sdk|0.158.0|0.161.0|minor
websockets|17.3|17.4|minor
google-crc32c|1.8.0|1.9.0|minor
python-rapidjson|1.25|1.26|minor
sagemaker-core|2.27.0|2.28.0|minor
sqlglot|30.25.0|30.29.0|minor
slack-sdk|3.45.0|3.46.0|minor
llvm-openmp|23.1.4|23.1.5|patch
triad|1.0.2|1.0.3|patch
fribidi|1.0.17|1.0.18|patch
pydantic-core|2.50.1|2.50.2|patch
typing-inspection|0.4.4|0.4.5|patch
pydantic|2.14.1|2.14.2|patch
wrapt|2.5.1|2.5.2|patch
platformdirs|4.14.0|4.14.5|patch
python-fastjsonschema|2.22.2|2.22.3|patch
fastcore|2.2.35|2.2.37|patch
authlib|1.9.1|1.9.3|patch
google-auth|2.62.0|2.62.1|patch
opentelemetry-proto|1.45.1|1.45.2|patch
py-spy|0.4.2|0.4.3|patch
smart_open|9.0.0|9.0.2|patch
blosc|1.21.6|1.21.7|patch
oauthlib|4.0.0|4.0.1|patch
python-multipart|0.0.32|0.0.33|patch
smart-open|9.0.0|9.0.2|patch
numba|0.68.0|0.68.1|patch
cachetools|7.2.7|7.2.8|patch
cyclopts|5.3.2|5.3.3|patch
deprecated|3.0.0|3.0.1|patch
dnspython|2.9.0|2.9.1|patch
langsmith|0.14.16|0.14.17|patch

### New

Package | Version
---|---
nlohmann_json-abi|3.12.0
