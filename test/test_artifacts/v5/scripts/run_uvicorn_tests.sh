#!/bin/bash
set -e

uvicorn_version=$(micromamba list | awk '$1=="uvicorn" {print $2}')

# Uvicorn release tags have no "v" prefix.
git checkout tags/$uvicorn_version

# Test dependencies live in the "dev" dependency group of pyproject.toml (includes pytest-xdist, required by addopts).
pip install --group dev

pytest tests -v -k "not test_main.py"
