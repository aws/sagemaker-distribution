import json
import os
import shutil
import sys
from datetime import datetime
from typing import Set


def backup_file(file_path):
    directory, filename = os.path.split(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{filename}.malformed_{timestamp}.bak"
    backup_path = os.path.join(directory, backup_filename)
    shutil.copy2(file_path, backup_path)
    print(f"A backup of the malformed file has been created: {backup_path}")


def load_json_file(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {file_path} contains malformed JSON.")
        if file_path == sys.argv[1]:  # If it's file1
            backup_file(file_path)
            print(f"Overwriting {file_path} with content from {sys.argv[2]}")
            shutil.copy2(sys.argv[2], file_path)
            with open(file_path, "r") as f:
                return json.load(f)
        else:
            raise


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1> <file2>")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]

    try:
        data1 = load_json_file(file1)
        data2 = load_json_file(file2)

        # Construct sets of extensions based on ID
        data1_exts = {ext["identifier"]["id"]: ext for ext in data1}
        data2_exts = {ext["identifier"]["id"]: ext for ext in data2}
        all_exts: Set[str] = set(data1_exts.keys()) | set(data2_exts.keys())

        # Merge extensions
        merged_exts = []
        for ext in all_exts:
            ext_data = data2_exts.get(ext, data1_exts.get(ext, {}))
            if "relativeLocation" in ext_data:
                del ext_data["relativeLocation"]
            merged_exts.append(ext_data)

        # Write the merged data back to file1
        print("Merged extensions: ", json.dumps(merged_exts, indent=2))
        with open(file1, "w") as f:
            json.dump(merged_exts, f, indent=2)

        print(f"Successfully merged extensions and wrote to {file1}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding failed - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
