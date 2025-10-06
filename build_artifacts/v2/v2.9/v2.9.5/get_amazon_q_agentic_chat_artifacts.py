#!/usr/bin/env python3
"""Extract Amazon Q artifact URLs from manifest for Linux x64 platform."""

import json
import sys

def extract_urls(manifest_file, version, platform='linux', arch='x64'):
    """Extract servers.zip and clients.zip URLs for specified platform/arch."""
    with open(manifest_file) as f:
        manifest = json.load(f)
    
    for ver in manifest['versions']:
        if ver['serverVersion'] == version:
            for target in ver['targets']:
                if target['platform'] == platform and target.get('arch') == arch:
                    servers_url = None
                    clients_url = None
                    
                    for content in target['contents']:
                        if content['filename'] == 'servers.zip':
                            servers_url = content['url']
                        elif content['filename'] == 'clients.zip':
                            clients_url = content['url']
                    
                    return servers_url, clients_url
    
    raise ValueError(f"Version {version} not found for {platform} {arch}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: get_amazon_q_agentic_chat_artifacts.py <manifest_file> <version>")
        sys.exit(1)
    
    manifest_file, version = sys.argv[1], sys.argv[2]
    servers_url, clients_url = extract_urls(manifest_file, version)
    
    print(f"SERVERS_URL={servers_url}")
    print(f"CLIENTS_URL={clients_url}")