#!/bin/bash

pip install ".[test]"

pytest tests/ -v
