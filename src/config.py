_image_generator_configs = [
    {
        "build_args": {
            "ENV_IN_FILENAME": "gpu.env.in",
            "ARG_BASED_ENV_IN_FILENAME": "gpu.arg_based_env.in",
        },
        "additional_packages_env_in_file": "gpu.additional_packages_env.in",
        "image_tag_generator": "{image_version}-gpu",
        "env_out_filename": "gpu.env.out",
        "pytest_flags": ["--use-gpu"],
        "image_type": "gpu",
    },
    {
        "build_args": {
            "TAG_FOR_BASE_MICROMAMBA_IMAGE": "jammy",
            "ENV_IN_FILENAME": "cpu.env.in",
        },
        "additional_packages_env_in_file": "cpu.additional_packages_env.in",
        "image_tag_generator": "{image_version}-cpu",
        "env_out_filename": "cpu.env.out",
        "pytest_flags": [],
        "image_type": "cpu",
    },
]
