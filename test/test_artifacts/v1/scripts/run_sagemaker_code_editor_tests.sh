#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

sagemaker-code-editor --version
echo "Verified that sagemaker-code-editor is installed"

# Check that extensions are installed correctly
extensions_base_dir="/opt/amazon/sagemaker/sagemaker-code-editor-server-data/extensions"
if [[ ! -d $extensions_base_dir ]]; then
    echo "Extension base directory $extensions_base_dir does not exist."
    exit 1
fi

installed_extensions=("ms-python.python" "ms-toolsai.jupyter" "amazonwebservices.aws-toolkit-vscode")
for extension in "${installed_extensions[@]}"; do
    # In this pattern, we're looking for versioning to follow immediately after the extension name
    # For ex - ms-toolsai.jupyter-2023.9.100
    pattern="${extension}-[0-9]*"

    # Use the find command to search for directories matching the current pattern
    found_dirs=$(find "$extensions_base_dir" -maxdepth 1 -type d -name "$pattern")

    if [[ -z $found_dirs ]]; then
        echo "Directory matching pattern '$pattern' does not exist in $extensions_base_dir."
        exit 1
    else
        echo "Directory exists for pattern '$pattern':"
        echo "$found_dirs"
    fi
done
echo "Verified that all extension folders are present in $extensions_base_dir."

# Check that settings file is copied
MACHINE_SETTINGS_FILE_PATH="/opt/amazon/sagemaker/sagemaker-code-editor-server-data/data/Machine/settings.json"
if [ ! -f "$MACHINE_SETTINGS_FILE_PATH" ]; then
    echo "Error: Settings file does not exist at $MACHINE_SETTINGS_FILE_PATH."
    exit 1
fi

echo "Settings file exists at $FILE_PATH."