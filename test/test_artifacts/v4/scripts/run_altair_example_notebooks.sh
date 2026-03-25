#!/bin/bash

# Create an empty notebook file for papermill's output
touch nb_output.ipynb

# List of example notebooks under the altair_notebooks' notebooks/ subdirectory, excluding examples
example_notebooks=('02-Tutorial.ipynb'
   '03-ScatterCharts.ipynb'
   '04-BarCharts.ipynb'
   '05-LineCharts.ipynb'
   '07-LayeredCharts.ipynb'
   '08-CarsDataset.ipynb'
)

for nb in ${example_notebooks[@]}; do
     papermill $nb 'nb_output.ipynb'
done
