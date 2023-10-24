#!/bin/bash

AUTOGLUON_VERSION=$(micromamba list | grep autogluon | tr -s ' ' | cut -d ' ' -f 3)
git checkout tags/v$AUTOGLUON_VERSION

# Run autogluon quick start as end-to-end check
jupyter nbconvert --execute --to python docs/tutorials/tabular/tabular-quick-start.ipynb
jupyter nbconvert --execute --to python docs/tutorials/timeseries/forecasting-quick-start.ipynb

# Detect gpu and run multimodal quick start if presented
python -c "import torch; exit(0) if torch.cuda.is_available() else exit(1)"
ret=$?

if [ $ret -eq 0 ]
then 
    jupyter nbconvert --execute --to python docs/tutorials/multimodal/multimodal_prediction/multimodal-quick-start.ipynb
fi
