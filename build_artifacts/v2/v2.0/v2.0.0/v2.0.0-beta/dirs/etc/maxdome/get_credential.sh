#!/bin/bash
maxdome get connection --name $MAXDOME_CONNECTION_NAME --authorization-mode PROJECT --with-secret | jq .environmentCredentials -r
