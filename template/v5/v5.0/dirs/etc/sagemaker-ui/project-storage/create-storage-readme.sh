#!/bin/bash

if [ ! -f "$HOME/README.md" ]; then
  echo "README file not found in $HOME, creating"

  cat /etc/sagemaker-ui/project-storage/README.md > "$HOME/README.md"
else
  echo "README already exists, skipping"
fi

