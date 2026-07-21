#!/bin/bash
# this is to replace sagemaker unfied studio jupyter scheduler label from "Job" to "Scheudule" to align with overall experience
set -ex

BASE_PATH="/opt/conda/share/jupyter/labextensions/@jupyterlab/scheduler/static"

# Function to perform replacement
replace_string() {
    local search="$1"
    local replace="$2"
    echo "Replacing '$search' with '$replace'..."
    grep -l -i -r "$search" "$BASE_PATH" | xargs sed -i "s/$search/$replace/gI"
}

# List of replacements
replace_string "\"Schedule\"" "\" \""
replace_string "Create Job\"" "Create Schedule\""
replace_string "Job name\"" "Schedule name\""
replace_string "Run job with input folder\"" "Run schedule with input folder\""
replace_string "\"The scheduled job will have access to all files under" "\"The schedule will have access to all files under"
replace_string "Notebook Jobs\"" "Notebook Schedules\""
replace_string "Notebook Job Definitions\"" "Notebook Schedule Definitions\""
replace_string "job definitions" "schedule definitions"
replace_string "Create Notebook Job" "Create Notebook Schedule"
replace_string "notebook job definition" "notebook schedule definition"
replace_string "Job definition name" "Schedule definition name"
replace_string "Job Detail\"" "Schedule Detail\""
replace_string "Job ID\"" "Schedule ID\""
replace_string "Your job definition" "Your schedule definition"
replace_string "Your job" "Your schedule"
replace_string "Job Definition\"" "Schedule Definition\""
replace_string "Run Job\"" "Run Schedule\""
replace_string "Creating job" "Creating schedule"
replace_string "Reload Job\"" "Reload Schedule\""
replace_string "Delete Job\"" "Delete Schedule\""
replace_string "Download Job Files\"" "Download Schedule Files\""
replace_string "No notebook jobs associated with this job definition" "No notebook schedules associated with this schedule definition"
replace_string "Create Job from Schedule Definition\"" "Create Schedule from Schedule Definition\""
replace_string "Job definition ID\"" "Schedule definition ID\""
replace_string "Create a notebook job" "Create a notebook schedule"
replace_string "Stop Job\"" "Stop Schedule\""

echo "All replacements completed!"
