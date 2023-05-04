_image_generator_configs = [
    {
        'build_args': {
            'TAG_FOR_BASE_MICROMAMBA_IMAGE': 'jammy-cuda-11.8.0',
            'CUDA_MAJOR_MINOR_VERSION': '11.8',  # Should match the previous one.
            'ENV_IN_FILENAME': 'gpu.env.in',
            'ARG_BASED_ENV_IN_FILENAME': 'gpu.arg_based_env.in',
        },
        'image_tag_generator': '{image_version}-gpu',
        'env_out_filename': 'gpu.env.out',
        'pytest_flags': ['--use-gpu']
    },
    {
        'build_args': {
            'TAG_FOR_BASE_MICROMAMBA_IMAGE': 'jammy',
            'ENV_IN_FILENAME': 'cpu.env.in',
        },
        'image_tag_generator': '{image_version}-cpu',
        'env_out_filename': 'cpu.env.out',
        'pytest_flags': []
    }
]
