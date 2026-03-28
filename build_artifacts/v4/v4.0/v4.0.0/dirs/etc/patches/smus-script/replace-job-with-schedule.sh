#!/bin/bash
# this is to replace sagemaker unfied studio jupyter scheduler label from "Job" to "Scheudule" to align with overall experience
set -ex

BASE_PATH="/opt/conda/share/jupyter/labextensions/@jupyterlab/scheduler/static"

# Function to perform replacement
replace_string() {
    local search="$1"
    local replace="$2"
    echo "Replacing '$search' with '$replace'..."
    grep -l -i -r "$search" "$BASE_PATH" | xargs sed -i "s/$search/$replace/g"
}

# List of replacements
replace_string "\"Schedule\"" "\" \""
replace_string "Create Job\"" "Create Schedule\""
replace_string "Job name\"" "Schedule name\""
replace_string "Run job with input folder\"" "Run schedule with input folder\""
replace_string "\"The scheduled job will have access to all files under" "\"The schedule will have access to all files under"
replace_string "Jobs\"" "Schedules\""
replace_string "jobs\"" "schedules\""
replace_string "Job Definitions\"" "Schedule Definitions\""
replace_string "Job definitions" "Schedule definitions"
replace_string "Job definition" "Schedule definition"
replace_string "job definitions" "schedule definitions"
replace_string "Create Job" "Create Schedule"
replace_string "Job Detail\"" "Schedule Detail\""
replace_string "Job ID\"" "Schedule ID\""
replace_string "Your job" "Your schedule"
replace_string "Job Definition\"" "Schedule Definition\""
replace_string "job definition" "schedule definition"
replace_string "Run Job\"" "Run Schedule\""
replace_string "Creating job" "Creating schedule"
replace_string "Reload Job\"" "Reload Schedule\""
replace_string "Delete Job\"" "Delete Schedule\""
replace_string "Download Job Files\"" "Download Schedule Files\""
replace_string "No jobs associated with this schedule definition" "No schedules associated with this schedule definition"
replace_string "There are no jobs. Jobs run" "There are no schedules. Schedules run"
replace_string "Create a job" "Create a schedule"
replace_string "create a job" "create a schedule"
replace_string "Stop Job\"" "Stop Schedule\""

echo "All replacements completed!"
