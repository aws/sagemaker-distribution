## Amazon SageMaker Distribution

Amazon SageMaker Distribution is a set of Docker images that include popular frameworks for machine learning, data
science and visualization.

These images come in two variants, CPU and GPU, and include deep learning frameworks like PyTorch, TensorFlow and
Keras; popular Python packages like numpy, scikit-learn and pandas; and IDEs like Jupyter Lab. The distribution contains
the _latest_ versions of all these packages _such that_ they are _mutually compatible_.

This project follows semver (more on that below) and comes with a helper tool to automate new releases of the
distribution.

## Getting started

If you just want to use the images, you do _not_ need to use this GitHub repository. Instead, you can pull pre-built
and ready-to-use images from our [AWS ECR Gallery repository](https://gallery.ecr.aws/sagemaker/sagemaker-distribution).

### Dependency versions included in a particular Amazon SageMaker Distribution version

If you want to check what packages are installed in a given version of Amazon SageMaker Distribution, you can find that
in the relevant _RELEASE.md_ file in the [build_artifacts](build_artifacts) directory.

### Versioning strategy

Amazon SageMaker Distribution supports semantic versioning as described on [semver.org](https://semver.org/). A major
version upgrade of Amazon SageMaker Distribution allows major version upgrades of all its dependencies, and similarly
for minor and patch version upgrades. However, it is important to note that Amazon SageMaker Distribution’s ability to
follow semver guidelines is currently dependent on how its dependencies adhere to them.

Some dependencies, such as Python, will be treated differently. Amazon SageMaker Distribution will allow a minor
upgrade of Python (say, 3.10 to 3.11) only during a major upgrade (say, 4.8 to 5.0).

### Image tags

Our current image tagging scheme is: `<AMAZON_SAGEMAKER_DISTRIBUTION_VERSION_NUMBER>-<CPU_OR_GPU>`. For example, the CPU
version of Amazon SageMaker Distribution's _v0.1.2_ will carry the following tags:

1. `0.1.2-cpu`: Once an image is tagged with such a patch version, that tag will _not_ be assigned to any other image
in future.
1. `0.1-cpu`: this, and the two below, _can_ change when new versions of Amazon SageMaker Distribution are released.
1. `0-cpu`
1. `latest-cpu`

So, if you want to stay on the latest software as and when release by Amazon SageMaker Distribution, you can use
`latest-cpu` and do a `docker pull latest-cpu` when needed. If you use, say, `0.1.2-cpu`, the underlying distribution
will remain the same over time.

### Package Staleness Report

If you want to generate/view the staleness report for each of the individual packages in a given
SageMaker distribution image version, then run the following command:

```
VERSION=<Insert SageMaker Distribution version in semver format here. example: 0.4.2>
python ./src/main.py generate-staleness-report --target-patch-version $VERSION
```

### Package Size Delta Report

If you want to generate/view the package size delta report for a given
SageMaker distribution image version comparing to a base image version, then run the following command:

```
BASE_PATCH_VERSION=<Insert SageMaker Distribution version of the base image in semver format here. example: 1.6.1>
VERSION=<Insert SageMaker Distribution version of the target image in semver format here. example: 1.6.2>
python ./src/main.py generate-size-report --base-patch-version $BASE_PATCH_VERSION --target-patch-version $VERSION
```


## Example use cases

Here are some examples on how you can try out one of our images.

### _Local_ environment, such as your laptop

The easiest way to get it running on your laptop is through the Docker CLI:

```shell
export ECR_IMAGE_ID='INSERT_IMAGE_YOU_WANT_TO_USE'
docker run -it \
    -p 8888:8888 \
    -v `pwd`/sample-notebooks:/home/sagemaker-user/sample-notebooks \
    $ECR_IMAGE_ID jupyter-lab --no-browser --ip=0.0.0.0
```

(If you have access to Nvidia GPUs, you can pass `--gpus=all` to the Docker command.)

In the image, we also have entrypoints built in, that automatically starts IDE server and automatically restarts
IDE server in case of minor IDE server interruptions or crashes. For example, to start JupyterLab server using the
entrypoint built in:
```shell
export ECR_IMAGE_ID='INSERT_IMAGE_YOU_WANT_TO_USE'
docker run -it \
    -p 8888:8888 \
    --entrypoint entrypoint-jupyter-server \
    -v `pwd`/sample-notebooks:/home/sagemaker-user/sample-notebooks \
    $ECR_IMAGE_ID
```

In the console output, you'll then see a URL similar to `http://127.0.0.1:8888/lab?token=foo`. Just open that URL in
your browser, create a Jupyter Lab notebook or open a terminal, and start hacking.

Note that the sample command above bind mounts a directory in `pwd` inside the container. That way, if you were to
re-create the container (say, to use a different version or CPU/GPU variant), any files you created within that
directory (such as Jupyter Lab notebooks) will persist.

### Amazon SageMaker Studio

> [Amazon SageMaker Studio](https://docs.aws.amazon.com/sagemaker/latest/dg/studio.html) is a web-based, integrated
> development environment (IDE) for machine learning that lets you build, train, debug, deploy, and monitor your
> machine learning models.

To use the sagemaker-distribution image in SageMaker Studio, select `SageMaker Distribution v{Major_version} {CPU/GPU}` using the [SageMaker Studio Launcher](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-launcher.html).

### "I want to directly use the Conda environment, not via a Docker image"

Amazon SageMaker Distribution supports full reproducibility of Conda environments, so you don't necessarily need to use
Docker. Just find the version number you want to use in the [build_artifacts](build_artifacts) directory, open one of
_cpu.env.out_ or _gpu.env.out_ and follow the instructions in the first 2 lines.

### Customizing image

If you'd like to create a new Docker image on top of what we offer, we recommend you use `micromamba install ...` instead of `pip install ...`.

For example:
```
FROM public.ecr.aws/sagemaker/sagemaker-distribution:latest-cpu
USER $ROOT
RUN apt-get install -y vim
USER $MAMBA_USER
RUN micromamba install sagemaker-inference --freeze-installed --yes --channel conda-forge --name base
```

## FIPS

As of sagemaker-distribution: v0.12+, v1.6+, and v2+, the images come with FIPS 140-2 validated openssl provider
available for use. You can enable the FIPS provider by running:

`export OPENSSL_CONF=/opt/conda/ssl/openssl-fips.cnf`

For more info on the FIPS provider see: https://github.com/openssl/openssl/blob/master/README-FIPS.md

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
