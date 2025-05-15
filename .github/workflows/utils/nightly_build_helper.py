#!/usr/bin/env python3
import argparse
import json
import os
import semver
import sys

from packaging.version import Version

def remove_version(version, current_schedule):
    """
    Remove a version from active builds and update base versions accordingly.

    Args:
        version (str): Version to remove (e.g., "1.2.3")
        current_schedule (dict): Current schedule data
    """
    print(f"Current schedule: {current_schedule}")
    print(f"Removing version: {version}")

    # Initialize lists if they don't exist
    if "active_nightly_builds" not in current_schedule:
        current_schedule["active_nightly_builds"] = []
    if "patch_base_versions" not in current_schedule:
        current_schedule["patch_base_versions"] = []
    if "minor_base_versions" not in current_schedule:
        current_schedule["minor_base_versions"] = []

    if version not in current_schedule["active_nightly_builds"]:
        print(f"Version {version} not found in active nightly builds schedule.")
        return current_schedule

    # Remove from active builds
    current_schedule["active_nightly_builds"].remove(version)

    version_obj = semver.VersionInfo.parse(version)

    if version_obj.patch == 0:  # Handling minor version (e.g., 3.2.0)
        # Remove previous minor version from minor_base_versions
        current_schedule["minor_base_versions"] = [
            v for v in current_schedule["minor_base_versions"]
            if not v.startswith(f"{version_obj.major}.{version_obj.minor-1}")
        ]
    else:  # Handling patch version (e.g., 3.0.2)
        prev_version = str(version_obj.replace(patch=version_obj.patch - 1))
        if prev_version in current_schedule["patch_base_versions"]:
            current_schedule["patch_base_versions"].remove(prev_version)

    # Sort all lists
    current_schedule["active_nightly_builds"].sort(key=Version)
    current_schedule["patch_base_versions"].sort(key=Version)
    current_schedule["minor_base_versions"].sort(key=Version)

    return current_schedule

def add_next_versions(version, current_schedule):
    """
    Add next version(s) based on the removed version.

    Args:
        version (str): Version that was removed (e.g., "1.2.3")
        current_schedule (dict): Current schedule data
    """
    print(f"Current schedule: {current_schedule}")
    print(f"Adding next versions for released: {version}")

    version_obj = semver.VersionInfo.parse(version)

    next_versions = [str(version_obj.bump_patch())]
    if version_obj.patch == 0:  # Handling minor version (e.g., 3.2.0)
        # Add next patch and minor versions
        next_versions.append(str(version.bump_minor()))
        current_schedule["active_nightly_builds"].extend(next_versions)
        # Add current version to both base version lists
        current_schedule["patch_base_versions"].append(version)
        current_schedule["minor_base_versions"].append(version)
    else:  # Handling patch version (e.g., 3.0.2)
        # Add next patch version
        current_schedule["active_nightly_builds"].extend(next_versions)
        # Add current version as base
        current_schedule["patch_base_versions"].append(version)
        # Update minor_base_versions if needed
        prev_version = str(version_obj.replace(patch=version_obj.patch - 1))
        if prev_version in current_schedule["minor_base_versions"]:
            current_schedule["minor_base_versions"].remove(prev_version)
            current_schedule["minor_base_versions"].append(version)

    # Sort all lists
    current_schedule["active_nightly_builds"].sort(key=Version)
    current_schedule["patch_base_versions"].sort(key=Version)
    current_schedule["minor_base_versions"].sort(key=Version)

    return current_schedule

def main():
    parser = argparse.ArgumentParser(description='Nightly build helper tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Remove version command
    remove_parser = subparsers.add_parser('remove-version',
        help='Remove a version from active builds')
    remove_parser.add_argument('version',
        help='Version to remove (e.g., 1.2.3)')
    remove_parser.add_argument(
        '--current-schedule-file',
        type=str,  # Changed from FileType('r') to str
        required=True,
        help='Path to schedule JSON file'
    )

    # Add next versions command
    add_parser = subparsers.add_parser('add-next-versions',
        help='Add next version(s) based on removed version')
    add_parser.add_argument('version',
        help='Version that was removed (e.g., 1.2.3)')
    add_parser.add_argument(
        '--current-schedule-file',
        type=str,  # Changed from FileType('r') to str
        required=True,
        help='Path to schedule JSON file'
    )

    args = parser.parse_args()

    # Parse current schedule from file
    try:
        with open(args.current_schedule_file, 'r') as f:
            current_schedule = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing current schedule file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {args.current_schedule_file}")
        sys.exit(1)

    if args.command == 'remove-version':
        updated_schedule = remove_version(args.version, current_schedule)
    elif args.command == 'add-next-versions':
        updated_schedule = add_next_versions(args.version, current_schedule)
    elif not args.command:
        parser.print_help()
        sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)

    print(f"Updated schedule: {updated_schedule}")

    # Write the updated schedule back to the file
    try:
        with open(args.current_schedule_file, 'w') as f:
            json.dump(updated_schedule, f, indent=4, sort_keys=True)
        print(f"Successfully updated {args.current_schedule_file}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()