#!/bin/bash

kernel_type=$2
connection_file=$4

MAXDOME_CONNECTION_NAME=default.iam
export AWS_REGION=`maxdome-toolkit connection read -n $MAXDOME_CONNECTION_NAME -ws | jq .location.awsRegion -r`

/opt/conda/bin/python -m ${kernel_type} -f ${connection_file}
