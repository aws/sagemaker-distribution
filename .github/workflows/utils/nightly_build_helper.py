import argparse
import json
import os
import semver
import sys
from github import Github
from packaging.version import Version

class NightlyBuildHelper:
    def __init__(self):
        """Initialize with GitHub credentials from environment variables."""
        token = os.environ.get('GH_TOKEN')
        repo_name = os.environ.get('GITHUB_REPOSITORY')

        if not token:
            raise ValueError("GH_TOKEN environment variable is required")
        if not repo_name:
            raise ValueError("GITHUB_REPOSITORY environment variable is required")

        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)
        self.schedule_variable, self.current_schedule = self._load_schedule()

    def _load_schedule(self):
        """Load the schedule from GitHub Actions variable."""
        try:
            # Get the NIGHTLY_BUILD_SCHEDULE variable
            schedule_var = self.repo.get_variable("NIGHTLY_BUILD_SCHEDULE")
            schedule = json.loads(schedule_var.value)

            # Initialize lists if they don't exist
            schedule.setdefault("active_nightly_builds", [])
            schedule.setdefault("patch_base_versions", [])
            schedule.setdefault("minor_base_versions", [])
            return schedule_var, schedule
        except Exception as e:
            print(f"Error loading schedule from GitHub: {e}")
            sys.exit(1)

    def _save_schedule(self):
        """Save the current schedule to GitHub Actions variable."""
        try:
            schedule_json = json.dumps(self.current_schedule, indent=4, sort_keys=True)
            print(f"Updated schedule: {schedule_json}")
            # Update the existing variable
            self.schedule_variable.edit(schedule_json)
            print("Successfully updated NIGHTLY_BUILD_SCHEDULE variable: https://github.com/aws/sagemaker-distribution/settings/variables/actions")
        except Exception as e:
            print(f"Error saving schedule to GitHub: {e}")
            sys.exit(1)

    def _sort_lists(self):
        """Sort all version lists in the schedule."""
        self.current_schedule["active_nightly_builds"].sort(key=Version)
        self.current_schedule["patch_base_versions"].sort(key=Version)
        self.current_schedule["minor_base_versions"].sort(key=Version)

    def remove_version(self, version):
        """Remove a version from active builds and update base versions accordingly."""
        print(f"Current schedule: {json.dumps(self.current_schedule, indent=4, sort_keys=True)}")
        print(f"Removing version: {version}")

        if version not in self.current_schedule["active_nightly_builds"]:
            print(f"Version {version} not found in active nightly builds schedule.")
            return

        # Remove from active builds
        self.current_schedule["active_nightly_builds"].remove(version)

        version_obj = semver.VersionInfo.parse(version)

        if version_obj.patch == 0:  # Handling minor version
            # Remove previous minor version from minor_base_versions
            self.current_schedule["minor_base_versions"] = [
                v for v in self.current_schedule["minor_base_versions"]
                if not v.startswith(f"{version_obj.major}.{version_obj.minor-1}")
            ]
        else:  # Handling patch version
            prev_version = str(version_obj.replace(patch=version_obj.patch - 1))
            if prev_version in self.current_schedule["patch_base_versions"]:
                self.current_schedule["patch_base_versions"].remove(prev_version)

        self._sort_lists()
        self._save_schedule()

    def add_next_versions(self, version):
        """Add next version(s) based on the removed version."""
        print(f"Current schedule: {self.current_schedule}")
        print(f"Adding next versions for released: {version}")

        version_obj = semver.VersionInfo.parse(version)

        next_versions = [str(version_obj.bump_patch())]
        if version_obj.patch == 0:  # Handling minor version
            next_versions.append(str(version_obj.bump_minor()))
            self.current_schedule["active_nightly_builds"].extend(next_versions)
            self.current_schedule["patch_base_versions"].append(version)
            self.current_schedule["minor_base_versions"].append(version)
        else:  # Handling patch version
            self.current_schedule["active_nightly_builds"].extend(next_versions)
            self.current_schedule["patch_base_versions"].append(version)
            prev_version = str(version_obj.replace(patch=version_obj.patch - 1))
            if prev_version in self.current_schedule["minor_base_versions"]:
                self.current_schedule["minor_base_versions"].remove(prev_version)
                self.current_schedule["minor_base_versions"].append(version)

        self._sort_lists()
        self._save_schedule()

def main():
    parser = argparse.ArgumentParser(description='Nightly build helper tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Remove version command
    remove_parser = subparsers.add_parser('remove-version',
        help='Remove a version from active builds')
    remove_parser.add_argument('version',
        help='Version to remove (e.g., 1.2.3)')

    # Add next versions command
    add_parser = subparsers.add_parser('add-next-versions',
        help='Add next version(s) based on released version')
    add_parser.add_argument('version',
        help='Version that was released (e.g., 1.2.3)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        helper = NightlyBuildHelper()

        if args.command == 'remove-version':
            helper.remove_version(args.version)
        elif args.command == 'add-next-versions':
            helper.add_next_versions(args.version)
        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()