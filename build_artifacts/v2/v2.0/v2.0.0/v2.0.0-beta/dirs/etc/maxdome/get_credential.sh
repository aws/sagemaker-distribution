#!/bin/bash

maxdome-toolkit connection read -n $MAXDOME_CONNECTION_NAME -ws | jq .environmentCredentials -r
