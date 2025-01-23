#!/bin/bash
# Function to check if Docker CLI is installed
function check_docker_installed {
    if ! command -v docker &> /dev/null; then
        echo "Docker CLI is not installed."
        exit 1
    else
        echo "Docker CLI is installed."
    fi
}
# Function to validate Docker can execute basic commands
function check_docker_functionality {
    # Try running a simple Docker command
    if docker --version &> /dev/null; then
        echo "Docker CLI is functioning correctly."
    else
        echo "Docker CLI is not functioning correctly."
        exit 1
    fi
}
# Run the checks
check_docker_installed
check_docker_functionality
echo "Docker CLI validation successful."