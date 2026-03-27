from __future__ import absolute_import

import pytest

pytestmark = pytest.mark.unit

from config import _image_generator_configs
from utils import derive_changeset

# Use the v1 cpu config — shape is what matters, not the specific version
_CPU_CONFIG = next(c for c in _image_generator_configs[1] if c["image_type"] == "cpu")


def _write_env_in(path, packages: list[str]):
    with open(path, "w") as f:
        f.write("\n".join(packages) + "\n")


def _write_env_out(path, urls: list[str]):
    with open(path, "w") as f:
        f.write(
            "# This file may be used to create an environment using:\n"
            "# $ conda create --name <env> --file <this file>\n"
            "# platform: linux-64\n"
            "@EXPLICIT\n"
        )
        f.write("\n".join(urls) + "\n")


def _setup_dirs(tmp_path):
    source_dir = tmp_path / "v1.0.5"
    target_dir = tmp_path / "v1.0.6"
    source_dir.mkdir()
    target_dir.mkdir()
    return str(source_dir), str(target_dir)


def test_derive_changeset_upgrades_and_new_packages(tmp_path):
    source_dir, target_dir = _setup_dirs(tmp_path)

    _write_env_in(source_dir + "/cpu.env.in", ["conda-forge::ipykernel"])
    _write_env_out(
        source_dir + "/cpu.env.out",
        ["https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#abc"],
    )

    # Target adds boto3 as a new direct dep; ipykernel gets a version bump
    _write_env_in(target_dir + "/cpu.env.in", ["conda-forge::ipykernel", "conda-forge::boto3"])
    _write_env_out(
        target_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.6-pyh210e3f2_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    changeset = derive_changeset(source_dir, target_dir, _CPU_CONFIG)

    assert changeset.direct.changed == {"ipykernel": ["6.21.3", "6.21.6"]}
    assert changeset.direct.added == {"boto3": "1.2"}
    assert changeset.direct.removed == {}


def test_derive_changeset_removed_package(tmp_path):
    source_dir, target_dir = _setup_dirs(tmp_path)

    _write_env_in(source_dir + "/cpu.env.in", ["conda-forge::ipykernel", "conda-forge::boto3"])
    _write_env_out(
        source_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    # Target drops boto3 entirely
    _write_env_in(target_dir + "/cpu.env.in", ["conda-forge::ipykernel"])
    _write_env_out(
        target_dir + "/cpu.env.out",
        ["https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#abc"],
    )

    changeset = derive_changeset(source_dir, target_dir, _CPU_CONFIG)

    assert changeset.direct.removed == {"boto3": "1.2"}


def test_derive_changeset_demotion(tmp_path):
    source_dir, target_dir = _setup_dirs(tmp_path)

    _write_env_in(source_dir + "/cpu.env.in", ["conda-forge::ipykernel"])
    _write_env_out(
        source_dir + "/cpu.env.out",
        ["https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#abc"],
    )

    # Target drops ipykernel from env.in but it's still pulled in transitively (same version)
    _write_env_in(target_dir + "/cpu.env.in", ["conda-forge::boto3"])
    _write_env_out(
        target_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    changeset = derive_changeset(source_dir, target_dir, _CPU_CONFIG)

    # Demoted with no version change — not shown anywhere
    assert "ipykernel" not in changeset.direct.removed
    assert "ipykernel" not in changeset.indirect.added


def test_derive_changeset_demotion_with_version_change(tmp_path):
    source_dir, target_dir = _setup_dirs(tmp_path)

    _write_env_in(source_dir + "/cpu.env.in", ["conda-forge::ipykernel"])
    _write_env_out(
        source_dir + "/cpu.env.out",
        ["https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#abc"],
    )

    # Target drops ipykernel from env.in, still present transitively but at a new version
    _write_env_in(target_dir + "/cpu.env.in", ["conda-forge::boto3"])
    _write_env_out(
        target_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.6-pyh210e3f2_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    changeset = derive_changeset(source_dir, target_dir, _CPU_CONFIG)

    # Demoted with version change — shows in indirect.changed, not direct.removed
    assert "ipykernel" not in changeset.direct.removed
    assert changeset.indirect.changed == {"ipykernel": ["6.21.3", "6.21.6"]}


def test_derive_changeset_promotion(tmp_path):
    source_dir, target_dir = _setup_dirs(tmp_path)

    # boto3 is indirect in source (in env.out but not env.in)
    _write_env_in(source_dir + "/cpu.env.in", ["conda-forge::ipykernel"])
    _write_env_out(
        source_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    # Target promotes boto3 to direct (added to env.in), same version
    _write_env_in(target_dir + "/cpu.env.in", ["conda-forge::ipykernel", "conda-forge::boto3"])
    _write_env_out(
        target_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    changeset = derive_changeset(source_dir, target_dir, _CPU_CONFIG)

    # Promoted with no version change — not shown anywhere
    assert "boto3" not in changeset.direct.added
    assert "boto3" not in changeset.indirect.removed


def test_derive_changeset_promotion_with_version_change(tmp_path):
    source_dir, target_dir = _setup_dirs(tmp_path)

    # boto3 is indirect in source at 1.2
    _write_env_in(source_dir + "/cpu.env.in", ["conda-forge::ipykernel"])
    _write_env_out(
        source_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.2-cuda112py38hd_0.conda#abc",
        ],
    )

    # Target promotes boto3 to direct at a new version
    _write_env_in(target_dir + "/cpu.env.in", ["conda-forge::ipykernel", "conda-forge::boto3"])
    _write_env_out(
        target_dir + "/cpu.env.out",
        [
            "https://conda.anaconda.org/conda-forge/noarch/ipykernel-6.21.3-pyh210e3f2_0.conda#abc",
            "https://conda.anaconda.org/conda-forge/linux-64/boto3-1.26-cuda112py38hd_0.conda#abc",
        ],
    )

    changeset = derive_changeset(source_dir, target_dir, _CPU_CONFIG)

    # Promoted with version change — shows in direct.changed, not direct.added
    assert "boto3" not in changeset.direct.added
    assert changeset.direct.changed == {"boto3": ["1.2", "1.26"]}
