#!/bin/bash


cd "$HOME/pacman/across_subject_analyses/scripts"

notebooks=( "ghost_attack_allsubs.ipynb" )  # Add your notebooks here

output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

for nb in "${notebooks[@]}"; do
    # Execute the notebook and save the output
    echo $nb
    jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ieeg_analysis2 "$nb"

    # Convert the executed notebook to HTML
    echo "$output_folder/$(basename "$nb" .ipynb).html"
    jupyter nbconvert --to html "$nb" --output "$output_folder/$(basename "$nb" .ipynb).html"

done

