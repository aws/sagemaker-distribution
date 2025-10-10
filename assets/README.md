# Assets

This directory contains utility scripts and files used during the Docker image build process.

## extract_amazon_q_agentic_chat_urls.py

A Python script that extracts Amazon Q Agentic Chat artifact URLs from a manifest file for Linux x64 platform.

### Usage
```bash
python extract_amazon_q_agentic_chat_urls.py <manifest_file> <version>
```

### Parameters
- `manifest_file`: Path to the JSON manifest file containing artifact information
- `version`: The server version to extract artifacts for

### Output
The script outputs environment variables for use in shell scripts:
- `SERVERS_URL`: URL for the servers.zip artifact
- `CLIENTS_URL`: URL for the clients.zip artifact

## download_amazon_q_agentic_chat_artifacts.sh

A modular shell script that downloads and extracts Amazon Q Agentic Chat artifacts for IDE integration.

### Usage
```bash
bash download_amazon_q_agentic_chat_artifacts.sh <version> <target_dir> <ide_type>
```

### Parameters
- `version`: Amazon Q server version (defaults to $FLARE_SERVER_VERSION_JL)
- `target_dir`: Target directory for artifacts (defaults to /etc/amazon-q-agentic-chat/artifacts/jupyterlab)
- `ide_type`: IDE type for logging (defaults to jupyterlab)

### Features
- Downloads JSZip library to shared web client location (/etc/web-client/libs/) for reuse across all web applications
- Modular design supports future VSCode integration
- Comprehensive error handling with retry logic
- Automatic cleanup of temporary files

### Directory Structure
- `/etc/web-client/libs/` - Shared web client libraries (JSZip, etc.) for any web application
- `/etc/amazon-q-agentic-chat/artifacts/jupyterlab/` - Amazon Q specific artifacts for JupyterLab
- `/etc/amazon-q-agentic-chat/artifacts/vscode/` - Future Amazon Q artifacts for VSCode