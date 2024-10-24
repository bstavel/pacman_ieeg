#!/bin/bash

subjects=(  "BJH021" "BJH025" "BJH016" "SLCH002" "BJH026" "BJH027" "BJH029" "BJH039" "BJH041" "LL10" "LL12" "LL13" "LL14" "LL17" "LL19" )
# subjects=( "BJH050" "BJH051" "SLCH018" "BJH017" "BJH046" )


# Loop over each subject
for subject in "${subjects[@]}"; do

    cd "$HOME/pacman/preprocessing/$subject/scripts" || {
        echo "Failed to change directory to $HOME/pacman/preprocessing/$subject/scripts"
        continue  # Skip to the next subject
    }

    # Add your notebooks here
    notebooks=(
        # "${subject}_first_move.ipynb"
        # "${subject}_first_dot.ipynb"
        # "${subject}_last_away.ipynb"
        # "${subject}_ghost_attack.ipynb"
        # "${subject}_trial_end.ipynb"
        "${subject}_trial_onset.ipynb"
    )
    
    output_folder="$HOME/pacman/preprocessing/htmls"  # Specify your output folder here

    for nb in "${notebooks[@]}"; do
        # Check if the notebook file exists
        if [[ ! -f "$nb" ]]; then
            echo "Notebook $nb does not exist for subject $subject"
            continue  # Skip to the next notebook
        fi

        # Execute the notebook and save the output
        echo "Processing notebook: $nb"
        if ! jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 "$nb"; then
            echo "Failed to execute notebook $nb for subject $subject"
            continue  # Skip to the next notebook
        fi

        # Convert the executed notebook to HTML
        html_output="$output_folder/$(basename "$nb" .ipynb).html"
        echo "Converting notebook to HTML: $html_output"
        if ! jupyter nbconvert --to html "$nb" --output "$html_output"; then
            echo "Failed to convert notebook $nb to HTML for subject $subject"
            continue  # Skip to the next notebook
        fi

    done

done

