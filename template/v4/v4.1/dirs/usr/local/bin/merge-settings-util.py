import json
import sys


def _strip_jsonc(text):
    """Strip // and /* */ comments and trailing commas so VS Code-style
    settings.json (JSONC) can be parsed with the stdlib json module.

    Scans character-by-character and tracks whether we're inside a string
    literal, so occurrences of "//", "/*", or "," inside string values
    (e.g. "http.proxy": "http://proxy:8080") are left untouched.
    """
    out = []
    i, n = 0, len(text)
    in_string = False
    pending_comma = False

    while i < n:
        c = text[i]

        if in_string:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue

        if c == '"':
            if pending_comma:
                out.append(",")
                pending_comma = False
            in_string = True
            out.append(c)
            i += 1
            continue

        if c == "/" and i + 1 < n and text[i + 1] == "/":
            end = text.find("\n", i)
            i = end if end != -1 else n
            continue

        if c == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            i = end + 2 if end != -1 else n
            continue

        if c == ",":
            pending_comma = True
            i += 1
            continue

        if c in "}]":
            pending_comma = False
            out.append(c)
            i += 1
            continue

        if not c.isspace() and pending_comma:
            out.append(",")
            pending_comma = False
        out.append(c)
        i += 1

    if pending_comma:
        out.append(",")

    return "".join(out)


def _load_jsonc(path):
    with open(path, "r") as f:
        raw = f.read()
    return json.loads(_strip_jsonc(raw))


# merges json files file1 and file2, keys in file2 overwriting any keys that already exist in file1
def main():
    file1, file2 = sys.argv[1], sys.argv[2]

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
