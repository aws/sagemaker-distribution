from __future__ import absolute_import

import json
import os
import tempfile

import pytest

pytestmark = pytest.mark.unit

# Import the module under test
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "assets"))
from extract_amazon_q_agentic_chat_urls import extract_urls


class TestAmazonQAgenticChatUrlExtraction:
    """Test cases for Amazon Q Agentic Chat artifacts extraction."""

    def test_extract_urls_success(self):
        """Test successful URL extraction from manifest."""
        manifest_data = {
            "versions": [
                {
                    "serverVersion": "1.0.0",
                    "targets": [
                        {
                            "platform": "linux",
                            "arch": "x64",
                            "contents": [
                                {"filename": "servers.zip", "url": "https://example.com/servers.zip"},
                                {"filename": "clients.zip", "url": "https://example.com/clients.zip"},
                            ],
                        }
                    ],
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest_data, f)
            manifest_file = f.name

        try:
            servers_url, clients_url = extract_urls(manifest_file, "1.0.0")
            assert servers_url == "https://example.com/servers.zip"
            assert clients_url == "https://example.com/clients.zip"
        finally:
            os.unlink(manifest_file)

    def test_extract_urls_version_not_found(self):
        """Test error when version is not found."""
        manifest_data = {"versions": [{"serverVersion": "1.0.0", "targets": []}]}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest_data, f)
            manifest_file = f.name

        try:
            with pytest.raises(ValueError, match="Version 2.0.0 not found for linux x64"):
                extract_urls(manifest_file, "2.0.0")
        finally:
            os.unlink(manifest_file)

    def test_extract_urls_platform_not_found(self):
        """Test error when platform/arch combination is not found."""
        manifest_data = {
            "versions": [
                {"serverVersion": "1.0.0", "targets": [{"platform": "windows", "arch": "x64", "contents": []}]}
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest_data, f)
            manifest_file = f.name

        try:
            with pytest.raises(ValueError, match="Version 1.0.0 not found for linux x64"):
                extract_urls(manifest_file, "1.0.0")
        finally:
            os.unlink(manifest_file)

    def test_extract_urls_missing_files(self):
        """Test behavior when required files are missing."""
        manifest_data = {
            "versions": [
                {
                    "serverVersion": "1.0.0",
                    "targets": [
                        {
                            "platform": "linux",
                            "arch": "x64",
                            "contents": [{"filename": "other.zip", "url": "https://example.com/other.zip"}],
                        }
                    ],
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest_data, f)
            manifest_file = f.name

        try:
            with pytest.raises(ValueError, match=r"Required files \(servers.zip/clients.zip\) not found"):
                extract_urls(manifest_file, "1.0.0")
        finally:
            os.unlink(manifest_file)

    def test_extract_urls_custom_platform(self):
        """Test URL extraction with custom platform and arch."""
        manifest_data = {
            "versions": [
                {
                    "serverVersion": "1.0.0",
                    "targets": [
                        {
                            "platform": "darwin",
                            "arch": "arm64",
                            "contents": [
                                {"filename": "servers.zip", "url": "https://example.com/darwin-servers.zip"},
                                {"filename": "clients.zip", "url": "https://example.com/darwin-clients.zip"},
                            ],
                        }
                    ],
                }
            ]
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(manifest_data, f)
            manifest_file = f.name

        try:
            servers_url, clients_url = extract_urls(manifest_file, "1.0.0", "darwin", "arm64")
            assert servers_url == "https://example.com/darwin-servers.zip"
            assert clients_url == "https://example.com/darwin-clients.zip"
        finally:
            os.unlink(manifest_file)

    def test_extract_urls_invalid_json(self):
        """Test error handling for invalid JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json")
            manifest_file = f.name

        try:
            with pytest.raises(ValueError, match="Invalid JSON in manifest file"):
                extract_urls(manifest_file, "1.0.0")
        finally:
            os.unlink(manifest_file)

    def test_extract_urls_file_not_found(self):
        """Test error handling for missing manifest file."""
        with pytest.raises(FileNotFoundError):
            extract_urls("nonexistent.json", "1.0.0")
