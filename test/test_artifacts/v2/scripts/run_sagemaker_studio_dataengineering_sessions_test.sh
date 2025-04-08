#!/bin/bash

cat << 'EOF' > /tmp/run_sagemaker_studio_dataengineering_sessions.py
get_ipython().run_line_magic('load_ext', 'sagemaker_studio_dataengineering_sessions.sagemaker_connection_magic')
get_ipython().run_line_magic('help', '')
EOF

# Run the Python script via Ipython
ipython /tmp/run_sagemaker_studio_dataengineering_sessions.py || exit $?