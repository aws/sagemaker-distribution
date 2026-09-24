# justfile — developer conveniences for sagemaker-distribution.
# Requires `just` (added to environment.yml) and Docker. Run `just --list` to see recipes.

# List available recipes.
default:
    @just --list

# Regenerate both {cpu,gpu}.env.out lockfiles for a version. e.g. `just update-outfiles 4.5.0`
update-outfiles version: (update-cpu-outfile version) (update-gpu-outfile version)

# Regenerate cpu.env.out for a version.
update-cpu-outfile version:
    @just _update-outfile {{version}} cpu

# Regenerate gpu.env.out for a version.
update-gpu-outfile version:
    @just _update-outfile {{version}} gpu

# Regenerate a single <image_type> (cpu|gpu) .env.out for <version>.
#
# A lockfile is just the fully-resolved base conda environment, so this reproduces exactly what
# the image build does to produce it: solve the {cpu,gpu}.env.in (+ pinned_env.in, plus the CUDA
# arg_based_env.in for gpu) in the matching mambaorg/micromamba base image, then record it with
# `micromamba env export --explicit`. No full image build and no GPU hardware — GPU packages
# resolve against the CONDA_OVERRIDE_CUDA virtual package.
#
# The base images / CUDA version match src/config.py for SMD major v4.
_update-outfile version image_type:
    #!/usr/bin/env bash
    set -euo pipefail
    version="{{version}}"
    image_type="{{image_type}}"
    version_dir="build_artifacts/v${version%%.*}/v${version%.*}/v${version}"
    if [ ! -d "$version_dir" ]; then
        echo "No version directory found at $version_dir" >&2
        exit 1
    fi
    if [ "$image_type" = "gpu" ]; then
        base_image="mambaorg/micromamba:cuda12.9.1-ubuntu24.04"
        cuda_override="12.9"
        arg_based="gpu.arg_based_env.in"
    elif [ "$image_type" = "cpu" ]; then
        base_image="mambaorg/micromamba:ubuntu24.04"
        cuda_override=""
        arg_based=""
    else
        echo "image_type must be 'cpu' or 'gpu', got '$image_type'" >&2
        exit 1
    fi
    echo "Regenerating ${image_type}.env.out for $version in $base_image ..." >&2
    # Solve inside the base image (env.in append happens on a writable copy), export the lock to
    # stdout, and capture it into the .env.out. Install chatter goes to stderr so stdout is clean.
    docker run --rm -e CONDA_OVERRIDE_CUDA="$cuda_override" \
        -v "$PWD/$version_dir:/work:ro" "$base_image" bash -c "
            set -euo pipefail
            cp /work/${image_type}.env.in /work/${image_type}.pinned_env.in /tmp/
            if [ -n '${arg_based}' ]; then cat /work/${arg_based} >> /tmp/${image_type}.env.in; fi
            micromamba install -y --name base \
                --file /tmp/${image_type}.env.in --file /tmp/${image_type}.pinned_env.in 1>&2
            micromamba env export --name base --explicit
        " > "$version_dir/${image_type}.env.out"
    echo "Wrote $version_dir/${image_type}.env.out" >&2
