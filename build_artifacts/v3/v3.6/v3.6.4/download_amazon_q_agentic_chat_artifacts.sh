#!/bin/bash
set -e

# Download Amazon Q artifacts for IDE integration
# Usage: download_amazon_q_artifacts.sh <version> <target_dir> <ide_type>
# Example: download_amazon_q_artifacts.sh 1.25.0 /etc/amazon-q/artifacts/agentic-chat jupyterlab

VERSION=${1:-$FLARE_SERVER_VERSION_JL}
TARGET_DIR=${2:-"/etc/amazon-q-agentic-chat/artifacts/jupyterlab"}
IDE_TYPE=${3:-"jupyterlab"}

if [ -z "$VERSION" ]; then
    echo "Error: Version not specified and FLARE_SERVER_VERSION_JL not set"
    exit 1
fi

echo "Downloading Amazon Q artifacts for $IDE_TYPE (version: $VERSION)"

# Create target directories
sudo mkdir -p "$TARGET_DIR"

# Download manifest and extract artifact URLs
MANIFEST_URL="https://aws-toolkit-language-servers.amazonaws.com/qAgenticChatServer/0/manifest.json"
curl -L --retry 3 --retry-delay 5 --fail "$MANIFEST_URL" -o "/tmp/manifest.json" || {
    echo "Failed to download manifest"
    exit 1
}

# Extract artifact URLs
ARTIFACT_URLS=$(python3 /tmp/extract_amazon_q_agentic_chat_urls.py /tmp/manifest.json "$VERSION")
if [ $? -ne 0 ] || [ -z "$ARTIFACT_URLS" ]; then
    echo "Failed to extract Amazon Q artifact URLs"
    exit 1
fi

eval "$ARTIFACT_URLS"

# Download and extract servers.zip
echo "Downloading servers.zip..."
curl -L --retry 3 --retry-delay 5 --fail "$SERVERS_URL" -o "/tmp/servers.zip" || {
    echo "Failed to download servers.zip"
    exit 1
}
sudo unzip "/tmp/servers.zip" -d "$TARGET_DIR/servers" || {
    echo "Failed to extract servers.zip"
    exit 1
}

# Download and extract clients.zip
echo "Downloading clients.zip..."
curl -L --retry 3 --retry-delay 5 --fail "$CLIENTS_URL" -o "/tmp/clients.zip" || {
    echo "Failed to download clients.zip"
    exit 1
}
sudo unzip "/tmp/clients.zip" -d "$TARGET_DIR/clients" || {
    echo "Failed to extract clients.zip"
    exit 1
}

# Clean up temporary files
rm -f /tmp/manifest.json /tmp/servers.zip /tmp/clients.zip

echo "Amazon Q artifacts downloaded successfully to $TARGET_DIR"