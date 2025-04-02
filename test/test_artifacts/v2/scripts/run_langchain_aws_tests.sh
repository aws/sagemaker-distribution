#!/bin/bash

set -e

jupyter nbconvert --execute --to python samples/agents/agents_with_nova.ipynb

