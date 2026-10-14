import json
import re
import sys

# Matches a whole string literal (so its contents are never treated as a
# comment/trailing-comma below), or a "//"/"/* */" comment.
_STRING_OR_COMMENT = re.compile(r'"(?:[^"\\]|\\.)*"|//[^\n]*|/\*.*?\*/', re.DOTALL)
# Matches a whole string literal, or a trailing comma before "}"/"]".
_STRING_OR_TRAILING_COMMA = re.compile(r'"(?:[^"\\]|\\.)*"|,(\s*[}\]])')


def _strip_jsonc(text):
    """Strip // and /* */ comments and trailing commas so VS Code-style
    settings.json (JSONC) can be parsed with the stdlib json module.

    Both regexes also match a full string literal as their first
    alternative, so a value like "http.proxy": "http://proxy:8080" or
    "note": "a, b," is matched and re-emitted whole, never touched by the
    comment/trailing-comma branch.
    """
    had_comment = False

    def _drop_comment(m):
        nonlocal had_comment
        text = m.group()
        if text[0] == "/":
            had_comment = True
            return ""
        return text

    text = _STRING_OR_COMMENT.sub(_drop_comment, text)
    text = _STRING_OR_TRAILING_COMMA.sub(lambda m: m.group(1) or m.group(), text)
    return text, had_comment


def _load_jsonc(path):
    with open(path, "r") as f:
        raw = f.read()
    stripped, had_comment = _strip_jsonc(raw)
    return json.loads(stripped), had_comment


# merges json files file1 and file2, keys in file2 overwriting any keys that already exist in file1
def main():
    file1, file2 = sys.argv[1], sys.argv[2]

    try:
        data1, had_comments = _load_jsonc(file1)
        data2, _ = _load_jsonc(file2)
    except (ValueError, OSError) as e:
        # ValueError covers json.JSONDecodeError and UnicodeDecodeError
        # (invalid UTF-8), both subclasses of it.
        print(
            f"merge-settings-util: failed to merge settings ({e}); leaving {file1} unchanged",
            file=sys.stderr,
        )
        return

    if not isinstance(data1, dict) or not isinstance(data2, dict):
        # Valid JSON that isn't an object (e.g. "[1,2]" or "null") can't be
        # merged with dict unpacking below.
        print(
            f"merge-settings-util: {file1} and {file2} must both be JSON objects; leaving {file1} unchanged",
            file=sys.stderr,
        )
        return

    # Merge the data (simple update)
    merged_data = {**data1, **data2}

    # Write the merged data to a new file
    with open(file1, "w") as f:
        json.dump(merged_data, f)

    if had_comments:
        print(
            f"merge-settings-util: note: comments in {file1} were not preserved after merging",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
