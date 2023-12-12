#!/bin/bash

subjects=( "BJH027" "BJH029" "BJH039" "BJH041" "LL14" "LL17" "LL19" )


# Loop over each subject
for subject in "${subjects[@]}"; do

    cd "$HOME/pacman/preprocessing/$subject/scripts"

    # notebooks=( "${subject}_first_move.ipynb" "${subject}_first_dot.ipynb" "${subject}_last_away.ipynb" "${subject}_ghost_attack.ipynb" "${subject}_trial_end.ipynb" "${subject}_trial_onset.ipynb" )  # Add your notebooks here
    notebooks=( "${subject}_ghost_attack.ipynb" )  # Add your notebooks here
    
    output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

    for nb in "${notebooks[@]}"; do
        # Execute the notebook and save the output
        echo $nb
        jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ieeg_analysis2 "$nb"

        # Convert the executed notebook to HTML
        echo "$output_folder/$(basename "$nb" .ipynb).html"
        jupyter nbconvert --to html "$nb" --output "$output_folder/$(basename "$nb" .ipynb).html"

    done

done

subjects=( "LL14" "LL17" )


# Loop over each subject
for subject in "${subjects[@]}"; do

    cd "$HOME/pacman/preprocessing/$subject/scripts"

    notebooks=( "${subject}_first_move.ipynb" "${subject}_first_dot.ipynb" "${subject}_last_away.ipynb" "${subject}_trial_end.ipynb" "${subject}_trial_onset.ipynb" )  # Add your notebooks here
    
    output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

    for nb in "${notebooks[@]}"; do
        # Execute the notebook and save the output
        echo $nb
        jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ieeg_analysis2 "$nb"

        # Convert the executed notebook to HTML
        echo "$output_folder/$(basename "$nb" .ipynb).html"
        jupyter nbconvert --to html "$nb" --output "$output_folder/$(basename "$nb" .ipynb).html"

    done

done

subjects=( "BJH027" "BJH029" )

# Loop over each subject
for subject in "${subjects[@]}"; do

    cd "$HOME/pacman/preprocessing/$subject/scripts"

    notebooks=( "${subject}_trial_onset.ipynb" )  # Add your notebooks here
    
    output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

    for nb in "${notebooks[@]}"; do
        # Execute the notebook and save the output
        echo $nb
        jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ieeg_analysis2 "$nb"

        # Convert the executed notebook to HTML
        echo "$output_folder/$(basename "$nb" .ipynb).html"
        jupyter nbconvert --to html "$nb" --output "$output_folder/$(basename "$nb" .ipynb).html"

    done

done

subjects=( "BJH027" "LL19" )

# Loop over each subject
for subject in "${subjects[@]}"; do

    cd "$HOME/pacman/preprocessing/$subject/scripts"

    notebooks=( "${subject}_last_away.ipynb" )  # Add your notebooks here
    
    output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

    for nb in "${notebooks[@]}"; do
        # Execute the notebook and save the output
        echo $nb
        jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ieeg_analysis2 "$nb"

        # Convert the executed notebook to HTML
        echo "$output_folder/$(basename "$nb" .ipynb).html"
        jupyter nbconvert --to html "$nb" --output "$output_folder/$(basename "$nb" .ipynb).html"

    done

done

subjects=( "BJH029" )

# Loop over each subject
for subject in "${subjects[@]}"; do

    cd "$HOME/pacman/preprocessing/$subject/scripts"

    notebooks=( "${subject}_first_move.ipynb" )  # Add your notebooks here
    
    output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

    for nb in "${notebooks[@]}"; do
        # Execute the notebook and save the output
        echo $nb
        jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ieeg_analysis2 "$nb"

        # Convert the executed notebook to HTML
        echo "$output_folder/$(basename "$nb" .ipynb).html"
        jupyter nbconvert --to html "$nb" --output "$output_folder/$(basename "$nb" .ipynb).html"

    done

done
