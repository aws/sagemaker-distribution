#!/bin/bash

set -eux

# Function to compare version numbers
# Returns 0 if version1 >= version2, 1 otherwise
version_gte() {
    local version1="$1"
    local version2="$2"
    
    # Handle empty versions
    [ -z "$version1" ] && return 1
    [ -z "$version2" ] && return 0
    
    # If versions are identical, return true
    [ "$version1" = "$version2" ] && return 0
    
    # Use sort -V (version sort) to compare versions
    # Check if version1 comes after version2 in version sort
    local sorted=$(printf '%s\n%s\n' "$version1" "$version2" | sort -V)
    local first_line=$(echo "$sorted" | head -n1)
    
    # If version2 comes first in sort, then version1 >= version2
    [ "$first_line" = "$version2" ]
}

get_package_version() {
    local package_name="$1"
    
    # Try to get version using pip show
    local pkg_version=$(pip show "$package_name" 2>/dev/null | grep "Version:" | cut -d' ' -f2)
    
    if [ -z "$pkg_version" ]; then
        # Try using conda list as fallback
        pkg_version=$(conda list "$package_name" 2>/dev/null | grep "^$package_name " | awk '{print $2}' | head -n1)
    fi
    
    echo "$pkg_version"
}

# NOTE: Consider removing these patches entirely if all non-deprecating SMD versions 
# have package versions larger than the specified thresholds, as the patches would 
# no longer be needed.
should_skip_patch() {
    local patch_file="$1"
    local patch_basename=$(basename "$patch_file")
    
    # Check if patch filename contains "fix-ipython-display"
    if [[ "$patch_basename" == *"fix-ipython-display"* ]]; then
        # Skip this patch if hdijupyterutils >= 0.23.0
        local hdijupyterutils_version=$(get_package_version "hdijupyterutils")
        if [ -n "$hdijupyterutils_version" ]; then
            if version_gte "$hdijupyterutils_version" "0.23.0"; then
                echo "Skipping $patch_basename: hdijupyterutils version $hdijupyterutils_version >= 0.23"
                return 0
            fi
        fi
    fi
    
    # Check if patch filename contains "fix-boto3-endpoints"
    if [[ "$patch_basename" == *"fix-boto3-endpoints"* ]]; then
        # Skip this patch if botocore >= 1.37.17
        local botocore_version=$(get_package_version "botocore")
        if [ -n "$botocore_version" ]; then
            if version_gte "$botocore_version" "1.37.17"; then
                echo "Skipping $patch_basename: botocore version $botocore_version >= 1.37.17"
                return 0
            fi
        fi
    fi
    
    return 1
}

# Check if parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 [smus|smus-code-editor]"
    exit 1
fi

# Validate parameter
case "$1" in
    "smus")
        bash "/etc/patches/smus-script/replace-job-with-schedule.sh"
        PATCH_DIR="/etc/patches/smus"
        ;;
    "smus-code-editor")
        PATCH_DIR="/etc/patches/smus-code-editor"
        ;;
    *)
        echo "Error: Parameter must be either 'smus' or 'smus-code-editor'"
        exit 1
        ;;
esac

# Check if patch directory exists
if [ ! -d "$PATCH_DIR" ]; then
    echo "Error: Patch directory $PATCH_DIR does not exist"
    exit 1
fi

# Patch files can be generated via "diff -u /path/to/original_file /path/to/new_file > XXX_bad_package.patch"
# See https://www.thegeekstuff.com/2014/12/patch-command-examples/
for PATCHFILE in "$PATCH_DIR"/*.patch; do
    [ -f "$PATCHFILE" ] || continue
    
    # Check if this patch should be skipped due to version constraints
    if should_skip_patch "$PATCHFILE"; then
        continue
    fi
    
    echo "Applying $PATCHFILE"
    (cd "/opt/conda" && patch --strip=3 < "$PATCHFILE")
done
