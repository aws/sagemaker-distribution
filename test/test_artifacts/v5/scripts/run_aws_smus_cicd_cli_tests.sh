#!/bin/bash

# Check if aws-smus-cicd-cli is installed
function check_cli_installed {
    if ! command -v aws-smus-cicd-cli &> /dev/null; then
        echo "aws-smus-cicd-cli is not installed."
        exit 1
    else
        echo "aws-smus-cicd-cli is installed."
    fi
}

# Check if the CLI can create a manifest file
function check_cli_create {
    local output_file="/tmp/test-manifest.yaml"
    if aws-smus-cicd-cli create --output "$output_file" --name TestPipeline; then
        echo "aws-smus-cicd-cli create succeeded."
    else
        echo "aws-smus-cicd-cli create failed."
        exit 1
    fi

    if [ -f "$output_file" ]; then
        echo "Manifest file created successfully at $output_file."
    else
        echo "Manifest file was not created."
        exit 1
    fi

    # Clean up
    rm -f "$output_file"
}

# Run the checks
check_cli_installed
check_cli_create
echo "aws-smus-cicd-cli validation successful."
