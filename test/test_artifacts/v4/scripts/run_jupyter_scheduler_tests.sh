#!/bin/bash
jupyter_scheduler_version=$(micromamba list | grep jupyter-scheduler | tr -s ' ' | cut -d ' ' -f 3)

git checkout tags/v$jupyter_scheduler_version


pip install ".[test]"

test_files=(
    "jupyter_scheduler/tests/test_execution_manager.py"
    "jupyter_scheduler/tests/test_handlers.py"
    "jupyter_scheduler/tests/test_job_files_manager.py"
    "jupyter_scheduler/tests/test_orm.py"
    "jupyter_scheduler/tests/test_scheduler.py"
)

for test_file in "${test_files[@]}"; do
    echo "Running tests in $test_file"
    pytest -v "$test_file"
done