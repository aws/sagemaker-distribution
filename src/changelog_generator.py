import os

from semver import Version

from utils import (
    Changeset,
    create_markdown_table,
    derive_changeset,
    get_dir_for_version,
    get_semver,
)


def _classify_bump(prev: str, curr: str) -> str:
    """Return 'major', 'minor', 'patch', or '' if versions can't be parsed."""
    try:
        p = get_semver(prev)
        c = get_semver(curr)
        if c.major != p.major:
            return "major"
        if c.minor != p.minor:
            return "minor"
        return "patch"
    except Exception:
        return ""


def _write_dependency_section(f, changeset_section):
    if changeset_section.changed:
        f.write("### Changed\n\n")
        _bump_order = {"major": 0, "minor": 1, "patch": 2, "": 3}
        rows = sorted(
            [
                {
                    "Package": p,
                    "Previous Version": prev,
                    "Current Version": curr,
                    "Change Type": _classify_bump(prev, curr),
                }
                for p, (prev, curr) in changeset_section.changed.items()
            ],
            key=lambda r: _bump_order.get(r["Change Type"], 3),
        )
        f.write(create_markdown_table(["Package", "Previous Version", "Current Version", "Change Type"], rows))
    if changeset_section.added:
        f.write("\n### New\n\n")
        rows = [{"Package": p, "Version": v} for p, v in changeset_section.added.items()]
        f.write(create_markdown_table(["Package", "Version"], rows))
    if changeset_section.removed:
        f.write("\n### Removed\n\n")
        rows = [{"Package": p, "Last Version": v} for p, v in changeset_section.removed.items()]
        f.write(create_markdown_table(["Package", "Last Version"], rows))


def generate_change_log(target_version: Version, image_config):
    target_version_dir = get_dir_for_version(target_version)
    source_version_txt_file_path = f"{target_version_dir}/source-version.txt"
    if not os.path.exists(source_version_txt_file_path):
        print("[WARN]: Generating CHANGELOG is skipped because 'source-version.txt' isn't found.")
        return
    with open(source_version_txt_file_path, "r") as f:
        source_patch_version = f.readline()
    source_version = get_semver(source_patch_version)
    source_version_dir = get_dir_for_version(source_version)
    image_type = image_config["image_type"]
    changeset: Changeset = derive_changeset(source_version_dir, target_version_dir, image_config)

    has_direct = any(
        [
            changeset.direct.changed,
            changeset.direct.added,
            changeset.direct.removed,
        ]
    )
    has_indirect = any(
        [
            changeset.indirect.changed,
            changeset.indirect.added,
            changeset.indirect.removed,
        ]
    )

    with open(f"{target_version_dir}/CHANGELOG-{image_type}.md", "w") as f:
        f.write(f"# Change log: {target_version} ({image_type})\n\n")
        f.write(f"This page lists all package changes since the previous release ({source_version}).\n\n")

        if has_direct:
            f.write("## Direct dependencies\n\n")
            f.write(
                "> [!NOTE]\n"
                "> These packages are explicitly included in the image. Their updates follow"
                " SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).\n\n"
            )
            _write_dependency_section(f, changeset.direct)

        if has_indirect:
            f.write("\n## Indirect dependencies\n\n")
            f.write(
                "> [!NOTE]\n"
                "> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. "
                "Their versions may vary between releases.\n\n"
            )
            _write_dependency_section(f, changeset.indirect)
