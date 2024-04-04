"""
Read installed Conda packages with sorted size.
"""

import json
import os
import pathlib


def dump_conda_package_metadata():
    prefix = os.environ["CONDA_PREFIX"]
    meta_data_path = pathlib.Path(prefix) / "conda-meta"
    meta_data_files = meta_data_path.glob("*.json")

    meta_data = dict()
    for meta_data_file in meta_data_files:
        name = meta_data_file.name.split("-")[0]
        with open(meta_data_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            version = metadata["version"]
            size = metadata["size"]
        meta_data[name] = {"version": version, "size": size}

    # Sort the pakcage sizes in decreasing order
    meta_data = {k: v for k, v in sorted(meta_data.items(), key=lambda item: item[1]["size"], reverse=True)}

    print(json.dumps(meta_data))


if __name__ == "__main__":
    dump_conda_package_metadata()
