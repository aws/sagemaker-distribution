#!/usr/bin/env python3
"""
Fetch feature flags from DataZone domain and write to file.
This script is intended to be called from the post-startup script.
"""

import json
import logging
import os
import re
import sys
import urllib.request
import urllib.parse
import html

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def fetch_feature_flags():
    """
    Read domain metadata, fetch feature flags from domain login page,
    and write to ~/.aws/enabled_features/enabled_features.json
    """
    try:
        # Read resource metadata
        metadata_path = "/opt/ml/metadata/resource-metadata.json"
        logger.info(f"Reading metadata from {metadata_path}")

        with open(metadata_path, "r") as f:
            data = json.load(f)
            additional_metadata = data.get("AdditionalMetadata", {})
            domain_id = additional_metadata.get("DataZoneDomainId")
            region = additional_metadata.get("DataZoneDomainRegion")
            stage = additional_metadata.get("DataZoneStage")

        if not domain_id or not region:
            logger.warning("Domain metadata not found in resource metadata")
            return False

        # Construct domain login URL
        stage_prefix = f"-{stage}" if stage and stage != "prod" else ""
        domain_url = f"https://{domain_id}.sagemaker{stage_prefix}.{region}.on.aws/login"
        logger.info(f"Fetching feature flags from {domain_url}")

        # Validate URL scheme for security
        parsed_url = urllib.parse.urlparse(domain_url)
        if parsed_url.scheme != "https":
            logger.error(f"Only HTTPS URLs are allowed, got: {parsed_url.scheme}")
            return False

        # Fetch domain login page
        with urllib.request.urlopen(domain_url, timeout=10) as response:
            html_content = response.read().decode("utf-8")

        # Parse feature flags from meta tag
        match = re.search(
            r'<meta[^>]+name=["\']enabled-features["\'][^>]+content=["\']([^"\']+)["\']',
            html_content,
            re.IGNORECASE,
        )

        if not match:
            logger.warning("Feature flags meta tag not found in domain login page")
            return False

        # Unescape HTML entities (&quot; -> ")
        raw_content = html.unescape(match.group(1))
        feature_flags = json.loads(raw_content)
        logger.info(f"Found {len(feature_flags)} feature flags")

        # Write feature flags to file
        feature_flags_dir = os.path.expanduser("~/.aws/enabled_features")
        os.makedirs(feature_flags_dir, exist_ok=True)
        feature_flags_file = os.path.join(feature_flags_dir, "enabled_features.json")

        with open(feature_flags_file, "w") as f:
            json.dump({"enabled_features": feature_flags}, f, indent=2)

        logger.info(f"Feature flags written to {feature_flags_file}")
        return True

    except FileNotFoundError:
        logger.error(f"Metadata file not found: {metadata_path}")
        return False
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return False
    except urllib.error.URLError as e:
        logger.error(f"Failed to fetch domain page: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = fetch_feature_flags()
    sys.exit(0 if success else 1)
