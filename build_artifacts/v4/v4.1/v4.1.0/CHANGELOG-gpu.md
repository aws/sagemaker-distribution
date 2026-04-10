# Change log: 4.1.0 (gpu)

This page lists all package changes since the previous release (4.0.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
uv|0.11.4|0.11.6|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
cryptography|44.0.3|46.0.7|major
pyopenssl|24.3.0|25.3.0|major
libsqlite|3.52.0|3.53.0|minor
greenlet|3.3.2|3.4.0|minor
prometheus_client|0.24.1|0.25.0|minor
snowflake-connector-python|3.13.2|3.17.4|minor
opentelemetry-proto|1.40.0|1.41.0|minor
fastprogress|1.1.3|1.0.3|minor
awswrangler|3.15.1|3.16.0|minor
deltalake|1.3.2|1.5.0|minor
dnspython|2.7.0|2.8.0|minor
llvm-openmp|22.1.2|22.1.3|patch
libpng|1.6.56|1.6.57|patch
platformdirs|4.9.4|4.9.6|patch
langsmith|0.7.26|0.7.29|patch
virtualenv|21.2.0|21.2.1|patch
param|2.3.2|2.3.3|patch

### Removed

Package | Last Version
---|---
apsw|3.52.0.0
apswutils|0.1.2
fastlite|0.2.3
oauthlib|3.3.1
python-fasthtml|0.13.3
