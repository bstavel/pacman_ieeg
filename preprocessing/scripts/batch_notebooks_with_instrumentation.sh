#!/bin/bash
set -xe  # Enable debugging and exit on error

# Define directories
LOG_DIR="$HOME/pacman/preprocessing/logs"
OUTPUT_FOLDER="$HOME/pacman/preprocessing/htmls"
mkdir -p "$LOG_DIR" "$OUTPUT_FOLDER"

# Trap signals and errors
trap 'echo "Script interrupted by signal"; exit 1' INT TERM
trap 'echo "An error occurred on line $LINENO"; exit 1' ERR

# subjects=( "BJH021" "BJH025" "BJH016" "SLCH002" "BJH026" "BJH027" "BJH029" "BJH039" "BJH041" "LL10" "LL12" "LL13" "LL14" "LL17" "LL19" )
subjects=( "BJH050" "BJH051" "SLCH018" "BJH017" "BJH046" )

for subject in "${subjects[@]}"; do
    cd "$HOME/pacman/preprocessing/$subject/scripts" || {
        echo "Failed to change directory to $HOME/pacman/preprocessing/$subject/scripts"
        continue
    }
	notebooks=(
        	# "${subject}_first_move.ipynb"
        	# "${subject}_first_dot.ipynb"
        	# "${subject}_last_away.ipynb"
        	"${subject}_ghost_attack.ipynb"
        	# "${subject}_trial_end.ipynb"
        	# "${subject}_trial_onset.ipynb"
    	)

    for nb in "${notebooks[@]}"; do
        if [[ ! -f "$nb" ]]; then
            echo "Notebook $nb does not exist for subject $subject"
            continue
        fi

        LOG_FILE="$LOG_DIR/${subject}_$(basename "$nb" .ipynb).log"
        echo "Processing notebook: $nb" | tee -a "$LOG_FILE"

        # Execute the notebook with logging
        if ! jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 "$nb" \
            --ExecutePreprocessor.timeout=-1 --log-level=DEBUG \
            >> "$LOG_FILE" 2>&1; then
            echo "Failed to execute notebook $nb for subject $subject" | tee -a "$LOG_FILE"
            continue
        fi

        # Convert the executed notebook to HTML
        html_output="$OUTPUT_FOLDER/$(basename "$nb" .ipynb).html"
        echo "Converting notebook to HTML: $html_output" | tee -a "$LOG_FILE"
        if ! jupyter nbconvert --to html "$nb" --output "$html_output" \
            >> "$LOG_FILE" 2>&1; then
            echo "Failed to convert notebook $nb to HTML for subject $subject" | tee -a "$LOG_FILE"
            continue
        fi

    done

done

