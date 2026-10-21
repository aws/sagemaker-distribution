ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import ray; ray.init(num_cpus=2, include_dashboard=False); f = ray.remote(lambda x: x * x); assert ray.get([f.remote(i) for i in range(4)]) == [0, 1, 4, 9]; print(ray.__version__); ray.shutdown()"]
