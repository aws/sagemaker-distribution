# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional
documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary
information to effectively respond to your bug report or contribution.


## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of our code being used
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment


## Contributing via Pull Requests
Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the *main* branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source; please focus on the specific change you are contributing. If you also reformat all the code, it will be hard for us to focus on your change.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages.
5. Send us a pull request, answering any default questions in the pull request interface.
6. Pay attention to any automated CI failures reported in the pull request, and stay involved in the conversation.

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).


## For adding new Conda packages to SageMaker Distribution

Follow these steps for sending out a pull request for adding new packages:
1. Identify the latest version of SageMaker Distribution.
2. Create the next minor/major version's build artifacts folder here: https://github.com/aws/sagemaker-distribution/tree/main/build_artifacts
3. Currently, SageMaker Distribution is using Conda forge channel as our source (for Conda
   packages).
   Ensure that the new package which you are trying to add is present in Conda forge channel. https://conda-forge.org/feedstock-outputs/
4. Create {cpu/gpu}.additional_packages_env.in file in that folder containing the new packages.
   Specify the new package based on the following examples:

   i. conda-forge::new-package

   ii. conda-forge::new-package[version='>=some-version-number,<some-version-number']
5. Run the following commands to verify whether the new package which you are trying to add is
   compatible with the existing packages in SageMaker Distribution
   ```
   This project uses Conda to manage its dependencies. Run the following to setup your local environment:

   conda env update --file environment.lock -n sagemaker-distribution

   conda activate sagemaker-distribution

   export BASE_PATCH_VERSION='current.latest.version'

   # NEXT_VERSION refers to the version number corresponding to the folder you created as part
   of Step 2.

   export NEXT_VERSION='specify.next.version'

   # If NEXT_VERSION is a new minor version:

   python ./src/main.py create-minor-version-artifacts --base-patch-version=$BASE_PATCH_VERSION --force

   # Or for a new major version:

   python src/main.py create-major-version-artifacts --base-patch-version=$BASE_PATCH_VERSION --force

   # Build the image:
   python ./src/main.py build \
     --target-patch-version=$NEXT_VERSION --skip-tests

   ```
6. Ensure that the build command succeeds. If it fails, then it means that the package isn't
   compatible with the existing packages in SageMaker Distribution. Create a Github Issue, so
   that we can look more into it.
7. Add the relevant tests in https://github.com/aws/sagemaker-distribution/blob/main/test/test_dockerfile_based_harness.py
    and run the build command once again without `--skip-tests` flag.
   ```
   # When writing or debugging tests, you can use standard pytest commands and arguments (https://docs.pytest.org/en/8.0.x/how-to/usage.html) to run specific tests and change test execution behavior. Some useful commands:

   # The sagemaker-distribution conda env set up earlier should be activated before running below commands

   # Runs only tests for cpu image, verbose, shows reason for skipped tests
   python -m pytest -n auto -m cpu -vv -rs --local-image-version $VERSION

   # In addition to above, running only tests matching a name pattern
   python -m pytest -n auto -m cpu -vv -rs -k "<test_name>" --local-image-version $VERSION
    ```
8. Submit the PR containing the following files.
   * {cpu/gpu}.additional_packages_env.in files
   * All the test files and test_dockerfile_based_harness.py changes

   Note: you don't have to include other files such as env.in/ env.out/ Dockerfile etc in your PR

   Also Note: We might ask you to include the test results as part of the PR.

## Modifying the Dockerfile or dirs/ (static files)

Each minor version has its own template directory under `template/v{major}/v{major}.{minor}/` containing a `Dockerfile` and a `dirs/` folder. These are the static files that get copied into every new patch release of that minor version.

### Template directory structure

```
template/
├── v2/
│   ├── v2.13/
│   │   ├── Dockerfile
│   │   └── dirs/
│   └── v2.14/
│       ├── Dockerfile
│       └── dirs/
├── v3/
│   ├── v3.8/
│   │   ├── Dockerfile
│   │   └── dirs/
│   └── v3.9/
│       ├── Dockerfile
│       └── dirs/
└── v4/
    ├── v4.0/
    ├── v4.1/
    ├── v4.2/
    └── v4.3/
```

### Deciding where to make your change

First, identify the latest minor version's template (e.g., `template/v4/v4.3/`). Then check whether that minor version has already been released by looking for its `.0` patch in `build_artifacts/`:

```shell
# Example: checking if v4.3 has been released
ls build_artifacts/v4/v4.3/v4.3.0/
```

#### Adding a new feature (applies since upcoming new minor versions only)

Find the latest minor version's template directory (e.g., `template/v4/v4.3/`). Then decide:

- **If the latest minor version has NOT been released** (e.g., `build_artifacts/v4/v4.3/v4.3.0/` does not exist): edit the latest minor's template directly. It doesn't matter whether the template was created by you or by someone else — as long as v4.3.0 hasn't been released, all changes for the next minor go into `template/v4/v4.3/`.

- **If the latest minor version has already been released** (e.g., `build_artifacts/v4/v4.3/v4.3.0/` exists): create a new minor version's template by copying from the latest, then make your changes there:

  ```shell
  cp -r template/v4/v4.3 template/v4/v4.4
  # Now edit template/v4/v4.4/ as needed
  ```

  Include the new template directory in your PR.

In either case, older minor versions (4.0, 4.1, 4.2) are unaffected. Their next patch release will continue using their own frozen template.

Note: Since future minor versions are created by copying from the previous minor's template, any change made to the latest unreleased minor's template will also be inherited by subsequent minor versions when they are created.

#### Applying a security fix or infrastructure change (applies to all supported minor versions)

If the latest minor version has already been released, first create the next minor version's template:

```shell
cp -r template/v4/v4.3 template/v4/v4.4
```

Then apply the fix to **all** supported minor version templates (including the newly created one):

```
template/v4/v4.0/Dockerfile
template/v4/v4.1/Dockerfile
template/v4/v4.2/Dockerfile
template/v4/v4.3/Dockerfile
template/v4/v4.4/Dockerfile
```

If the latest minor version has NOT been released yet, simply apply the fix to all existing supported minor version templates.

This approach is intentional — it makes the scope of the fix auditable and prevents accidental feature leakage.

### How new minor version templates are auto-created at build time

If no one creates the template directory before `create-minor-version-artifacts` runs, the tooling will automatically copy it from the previous minor's template (e.g., v4.3 → v4.4). This means any change in v4.3's template will be inherited by v4.4 if its template hasn't been pre-created.


## Finding contributions to work on
Looking at the existing issues is a great way to find something to contribute on. As our projects, by default, use the default GitHub issue labels (enhancement/bug/duplicate/help wanted/invalid/question/wontfix), looking at any 'help wanted' issues is a great place to start.


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security issue notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.
