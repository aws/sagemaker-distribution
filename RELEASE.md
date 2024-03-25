## Releasing new versions of AWS SageMaker Distribution

Releasing a new image version consists of two steps:

### Step 0: Setup your local environment

Follow the steps documented in [DEVELOPMENT.md](DEVELOPMENT.md) to setup your local environment.

The steps below assume you'll run them on the command line where you've already _activated_ the Conda environment for
the project. However, you can achieve the same through, say, PyCharm as well.

### Step 1: Create build artifacts for the _target version_

Let's say you want to create a new release on top of version _0.0.0_.

```shell
export BASE_PATCH_VERSION='0.0.0'
```

Now, run one of the following 3 commands depending on what _type_ of upgrade you want to do.

```shell
# If you want to create a new patch version on top of $BASE_PATCH_VERSION, run:
python src/main.py create-patch-version-artifacts --base-patch-version=$BASE_PATCH_VERSION

# Or for a new minor version:
python src/main.py create-minor-version-artifacts --base-patch-version=$BASE_PATCH_VERSION

# Or for a new major version:
python src/main.py create-major-version-artifacts --base-patch-version=$BASE_PATCH_VERSION
```

Note: if the directory for the _target version_ already exists, you can pass a `--force` flag to any of the commands
above. That will overwrite the directory.

### Step 2: Build images for the _target version_

Run the following to build the new images and upload them to one or more ECR repositories:

```shell
export TARGET_PATCH_VERSION='0.0.1'
export TARGET_REPO_1='...'
export TARGET_REPO_2='...'
export AWS_REGION_FOR_TARGET_REPO='...'

python src/main.py build \
  --target-patch-version=$TARGET_PATCH_VERSION \
  --target-ecr-repo=$TARGET_REPO_1 --target-ecr-repo=$TARGET_REPO_2 \
  --region=$AWS_REGION_FOR_TARGET_REPO
```

Note:

- As you can see above, the `--target-ecr-repo` parameter can be supplied zero or multiple times. If not supplied, the
tool will just build a local image. If supplied multiple times, it'll upload the images to all those ECR repositories.
- There is also a `--skip-tests` flag which, by default, is `false`. You can supply it if you'd like to skip tests
locally. However, we'll make sure the tests succeed before any image is release publicly.
