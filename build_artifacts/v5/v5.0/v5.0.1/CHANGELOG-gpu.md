# Change log: 5.0.1 (gpu)

This page lists all package changes since the previous release (5.0.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
fastapi|0.162.4|0.162.7|patch
sagemaker-studio-dataengineering-extensions|1.3.15|1.3.16|patch
sagemaker-studio-dataengineering-sessions|1.3.28|1.3.29|patch
uv|0.13.7|0.13.9|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
accelerate|1.15.0|1.16.0|minor
pcre2|10.47|10.49|minor
send2trash|2.1.0|2.2.0|minor
pandoc|3.13|3.14|minor
libpq|18.6|18.7|minor
python-slugify|9.1.3|9.2.0|minor
ujson|6.0.0|6.1.0|minor
optuna|5.0.0|5.1.0|minor
conda-rattler-solver|26.10.2|26.11.0|minor
cyclopts|5.4.0|5.5.2|minor
databricks-sdk|0.164.0|0.167.0|minor
email-validator|2.3.0|2.4.0|minor
email_validator|2.3.0|2.4.0|minor
langsmith|0.14.17|0.15.0|minor
prettytable|3.18.0|3.19.0|minor
pyroaring|1.1.0|1.2.0|minor
sagemaker-core|2.29.0|2.30.0|minor
sqlglot|30.31.0|30.33.0|minor
slack-sdk|3.46.0|3.47.0|minor
typer|0.29.0|0.29.1|patch
mpc|1.4.0|1.4.1|patch
tornado|6.6|6.6.1|patch
soupsieve|4.1|4.1.1|patch
authlib|1.9.5|1.9.8|patch
opentelemetry-api|1.45.1|1.45.2|patch
opentelemetry-sdk|1.45.1|1.45.2|patch
smart_open|9.0.3|9.0.4|patch
virtualenv|21.15.6|21.15.7|patch
regex|2026.11.9|2026.11.15|patch
imageio|2.38.1|2.38.2|patch
tifffile|2026.11.8|2026.11.16|patch
fastcore|2.2.41|2.2.44|patch
python-multipart|0.0.33|0.0.34|patch
python-fasthtml|0.14.22|0.14.24|patch
smart-open|9.0.3|9.0.4|patch
fugue|0.9.8|0.9.9|patch
coverage|7.17.2|7.17.3|patch
dnspython|2.9.1|2.9.2|patch
fastapi-core|0.162.4|0.162.7|patch
pydantic-settings|2.16.2|2.16.3|patch
py-key-value-aio|0.4.5|0.4.6|patch
libaec|1.1.7|1.1.8|patch
langchain-core|1.8.0|1.8.1|patch
langgraph-checkpoint|4.3.1|4.3.2|patch
langgraph-prebuilt|1.1.1|1.1.2|patch
langgraph|1.2.20|1.2.22|patch
nh3|0.3.7|0.3.8|patch
opentelemetry-semantic-conventions|0.66b1|0.66b2|
opentelemetry-exporter-prometheus|0.66b1|0.66b2|
opentelemetry-instrumentation|0.66b1|0.66b2|
opentelemetry-instrumentation-threading|0.66b1|0.66b2|

### New

Package | Version
---|---
pkgconf|3.0.11

### Removed

Package | Last Version
---|---
libstdcxx-ng|16.2.0
