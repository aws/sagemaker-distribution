#!/bin/bash

jupyter nbconvert --execute --to python tests/test_borders.ipynb
jupyter nbconvert --execute --to python tests/test_sanitizer.ipynb
