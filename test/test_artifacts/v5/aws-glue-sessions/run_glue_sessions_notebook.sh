#!/bin/bash

# Create an empty notebook file for papermill's output
touch nb_output.ipynb

kernels=('glue_pyspark' 'glue_spark')
nb='script'
for kernel in ${kernels[@]}; do
     papermill 'glue_notebook.ipynb' 'nb_output.ipynb' -k $kernel
done
