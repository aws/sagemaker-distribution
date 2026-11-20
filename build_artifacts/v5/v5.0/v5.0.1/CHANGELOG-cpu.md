# Change log: 5.0.1 (cpu)

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
cachebox|5.2.3|6.2.11|major
tbb|2023.1.0|2023.2.0|minor
accelerate|1.15.0|1.16.0|minor
pcre2|10.47|10.49|minor
narwhals|2.28.0|2.29.0|minor
send2trash|2.1.0|2.2.0|minor
pandoc|3.13|3.14|minor
openldap|2.6.13|2.7.2|minor
libpq|18.6|18.7|minor
qt6-main|6.11.3|6.12.0|minor
pyside6|6.11.3|6.12.0|minor
python-slugify|9.1.3|9.2.0|minor
nspr|4.40|4.41|minor
ujson|6.0.0|6.1.0|minor
optuna|5.0.0|5.1.0|minor
conda-rattler-solver|26.10.2|26.11.0|minor
cyclopts|5.4.0|5.5.2|minor
databricks-sdk|0.164.0|0.169.0|minor
deepdiff|9.1.0|9.2.1|minor
email-validator|2.3.0|2.4.0|minor
email_validator|2.3.0|2.4.0|minor
jsonpatch|1.47|1.48|minor
langsmith|0.14.17|0.15.1|minor
openai|2.53.0|2.54.0|minor
prettytable|3.18.0|3.19.0|minor
pyroaring|1.1.0|1.2.0|minor
sagemaker-core|2.29.0|2.30.0|minor
sagemaker-train|1.29.0|1.30.0|minor
sagemaker-serve|1.29.0|1.30.0|minor
sqlglot|30.31.0|30.33.0|minor
slack-sdk|3.46.0|3.48.0|minor
llvm-openmp|23.1.5|23.1.6|patch
annotated-doc|0.0.6|0.0.7|patch
pydantic-core|2.50.4|2.50.5|patch
pydantic|2.14.3|2.14.4|patch
typer|0.29.0|0.29.2|patch
mpc|1.4.0|1.4.1|patch
fontconfig|2.18.3|2.18.4|patch
platformdirs|4.14.5|4.14.8|patch
tornado|6.6|6.6.1|patch
soupsieve|4.1|4.1.2|patch
exceptiongroup|1.3.1|1.3.2|patch
authlib|1.9.5|1.9.9|patch
cloudpickle|3.1.2|3.1.3|patch
libllvm23|23.1.5|23.1.6|patch
libclang-cpp23.1|23.1.5|23.1.6|patch
libclang13|23.1.5|23.1.6|patch
opentelemetry-api|1.45.1|1.45.2|patch
opentelemetry-sdk|1.45.1|1.45.2|patch
py-spy|0.4.3|0.4.4|patch
smart_open|9.0.3|9.0.6|patch
python-discovery|1.9.5|1.9.6|patch
virtualenv|21.15.6|21.15.9|patch
gdown|6.5.1|6.5.2|patch
regex|2026.11.9|2026.11.19|patch
imageio|2.38.1|2.38.2|patch
tifffile|2026.11.8|2026.11.16|patch
fastcore|2.2.41|2.2.45|patch
python-multipart|0.0.33|0.0.34|patch
python-fasthtml|0.14.22|0.14.26|patch
smart-open|9.0.3|9.0.6|patch
fugue|0.9.8|0.9.9|patch
coverage|7.17.2|7.17.3|patch
dnspython|2.9.1|2.9.2|patch
fastapi-core|0.162.4|0.162.7|patch
pydantic-settings|2.16.2|2.16.3|patch
py-key-value-aio|0.4.5|0.4.6|patch
freetds|1.5.21|1.5.22|patch
libaec|1.1.7|1.1.8|patch
langchain-protocol|0.0.21|0.0.22|patch
langchain-core|1.8.0|1.8.4|patch
langgraph-checkpoint|4.3.1|4.3.2|patch
langgraph-prebuilt|1.1.1|1.1.3|patch
langgraph|1.2.20|1.2.24|patch
nh3|0.3.7|0.3.8|patch
opentelemetry-semantic-conventions|0.66b1|0.66b2|
opentelemetry-exporter-prometheus|0.66b1|0.66b2|
opentelemetry-instrumentation|0.66b1|0.66b2|
opentelemetry-instrumentation-threading|0.66b1|0.66b2|

### New

Package | Version
---|---
tcm|1.6.0

### Removed

Package | Last Version
---|---
libstdcxx-ng|16.2.0
