#!/bin/bash
set -e

fastapi_version=$(micromamba list | awk '$1=="fastapi" {print $2}')

# FastAPI release tags have no "v" prefix.
git checkout tags/$fastapi_version

# Test dependencies live in the "tests" dependency group of pyproject.toml.
pip install --group tests

pytest tests/ -v -k "not test_tutorial"
