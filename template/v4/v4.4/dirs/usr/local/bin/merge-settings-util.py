import json
import re
import sys
from sys import argv


def _strip_jsonc(text):
    """Strip // and /* */ comments and trailing commas so VS Code-style
    settings.json (JSONC) can be parsed with the stdlib json module."""
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def _load_jsonc(path):
    with open(path, "r") as f:
        raw = f.read()
    return json.loads(_strip_jsonc(raw))


# merges json files file1 and file2, keys in file2 overwriting any keys that already exist in file1
def main():
    file1, file2 = argv[1], argv[2]

    try:
        data1 = _load_jsonc(file1)
        data2 = _load_jsonc(file2)
    except (json.JSONDecodeError, OSError) as e:
        print(
            f"merge-settings-util: failed to merge settings ({e}); leaving {file1} unchanged",
            file=sys.stderr,
        )
        return

    # Merge the data (simple update)
    merged_data = {**data1, **data2}

    # Write the merged data to a new file
    with open(file1, "w") as f:
        json.dump(merged_data, f)


if __name__ == "__main__":
    main()
