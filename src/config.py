_image_generator_configs = {
    0: [
        {
            "build_args": {
                "TAG_FOR_BASE_MICROMAMBA_IMAGE": "jammy-cuda-11.8.0",
                "CUDA_MAJOR_MINOR_VERSION": "11.8",  # Should match the previous one.
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
    ],
    1: [
        {
            "build_args": {
                "TAG_FOR_BASE_MICROMAMBA_IMAGE": "jammy-cuda-11.8.0",
                "CUDA_MAJOR_MINOR_VERSION": "11.8",  # Should match the previous one.
                "ENV_IN_FILENAME": "gpu.env.in",
                "PINNED_ENV_IN_FILENAME": "gpu.pinned_env.in",
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
                "PINNED_ENV_IN_FILENAME": "cpu.pinned_env.in",
            },
            "additional_packages_env_in_file": "cpu.additional_packages_env.in",
            "image_tag_generator": "{image_version}-cpu",
            "env_out_filename": "cpu.env.out",
            "pytest_flags": [],
            "image_type": "cpu",
        },
    ],
    2: [
        {
            "build_args": {
                "TAG_FOR_BASE_MICROMAMBA_IMAGE": "jammy-cuda-12.5.0",
                "CUDA_MAJOR_MINOR_VERSION": "12.5",  # Should match the previous one.
                "ENV_IN_FILENAME": "gpu.env.in",
                "PINNED_ENV_IN_FILENAME": "gpu.pinned_env.in",
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
                "PINNED_ENV_IN_FILENAME": "cpu.pinned_env.in",
            },
            "additional_packages_env_in_file": "cpu.additional_packages_env.in",
            "image_tag_generator": "{image_version}-cpu",
            "env_out_filename": "cpu.env.out",
            "pytest_flags": [],
            "image_type": "cpu",
        },
    ],
    3: [
        {
            "build_args": {
                "TAG_FOR_BASE_MICROMAMBA_IMAGE": "cuda12.6.3-ubuntu22.04",
                "CUDA_MAJOR_MINOR_VERSION": "12.6",  # Should match the previous one.
                "ENV_IN_FILENAME": "gpu.env.in",
                "PINNED_ENV_IN_FILENAME": "gpu.pinned_env.in",
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
                "TAG_FOR_BASE_MICROMAMBA_IMAGE": "ubuntu22.04",
                "ENV_IN_FILENAME": "cpu.env.in",
                "PINNED_ENV_IN_FILENAME": "cpu.pinned_env.in",
            },
            "additional_packages_env_in_file": "cpu.additional_packages_env.in",
            "image_tag_generator": "{image_version}-cpu",
            "env_out_filename": "cpu.env.out",
            "pytest_flags": [],
            "image_type": "cpu",
        },
    ],
}
