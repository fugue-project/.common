#!/usr/bin/env python3
"""
Generic release tag validator for GitHub Actions.
Validates that the git tag matches the installed package version.
"""

import os
import sys
from importlib.metadata import version


def main():
    # Check for project name argument
    if len(sys.argv) < 2:
        print("❌ Usage: validate_release.py <project_name>")
        print("   Example: validate_release.py my-package")
        sys.exit(1)

    project_name = sys.argv[1]

    # Get the tag from GitHub environment
    github_ref = os.environ.get("GITHUB_REF")
    if not github_ref:
        print("❌ GITHUB_REF environment variable not set")
        print("This script should only run in GitHub Actions on tag push")
        sys.exit(1)

    if not github_ref.startswith("refs/tags/"):
        print(f"❌ GITHUB_REF is not a tag: {github_ref}")
        sys.exit(1)

    # Extract tag name
    tag = github_ref.replace("refs/tags/", "")

    # Strip 'v' prefix if present
    tag_version = tag[1:] if tag.startswith("v") else tag

    # Get version from installed package
    try:
        package_version = version(project_name)
    except Exception as e:
        print(f"❌ Failed to get version for package '{project_name}': {e}")
        sys.exit(1)

    # Compare versions
    print(f"GitHub tag: {tag}")
    print(f"Package version ({project_name}): {package_version}")

    if tag_version == package_version:
        print("✅ Version validation passed!")
        sys.exit(0)
    else:
        print("❌ Version mismatch!")
        print(f"   Tag version: {tag_version}")
        print(f"   Package version: {package_version}")
        sys.exit(1)


if __name__ == "__main__":
    main()
