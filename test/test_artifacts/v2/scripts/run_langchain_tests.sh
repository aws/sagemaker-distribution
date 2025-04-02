#!/bin/bash

pip install ".[test]"
pip install blockbuster

pytest -v libs/langchain/tests/unit_tests/test_formatting.py 


