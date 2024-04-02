#!/bin/bash

kernel_type=$2
connection_file=$4

MAXDOME_CONNECTION_NAME=default.iam
export AWS_REGION=`maxdome get connection --name $MAXDOME_CONNECTION_NAME --authorization-mode PROJECT --with-secret | jq .location.awsRegion -r`

/opt/conda/bin/python -m ${kernel_type} -f ${connection_file}
