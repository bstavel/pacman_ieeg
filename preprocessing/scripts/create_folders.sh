#!/bin/bash

# Define the list of subjects
# subjects=( "BJH026" "LL19" "LL10" "LL12" "LL13" "IR102" "IR103" "IR104" "BJH016" "BJH021" "BJH025" "BJH030" "SLCH002" "BJH039" "BJH041" )
# subjects=( "BJH026" "BJH027" "BJH029" "BJH030" "BJH039" "BJH041" "LL14" "LL16" "LL17" "LL19" )
subjects=( "LL17" "LL14" )

# Loop over each subject
for subject in "${subjects[@]}"; do
    echo "Processing $subject..."

    ## Create rivendell directories
    # # raw dirs
    # mkdir -p "$HOME/pacman/raw_data/$subject/behave"
    # mkdir -p "$HOME/pacman/raw_data/$subject/ieeg"
    # mkdir -p "$HOME/pacman/raw_data/$subject/scripts"

    # # preprocessed dirs
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/scripts"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/scripts/figures"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/trial_onset"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/first_move"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/first_dot"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/last_away"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/trial_end"
    # mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/ghost_attack"

    # # # # Copy files
    # cp ~/pacman/script_templates/trial_onset.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_trial_onset.ipynb
    # cp ~/pacman/script_templates/first_move.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_first_move.ipynb
    # cp ~/pacman/script_templates/first_dot.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_first_dot.ipynb
    # cp ~/pacman/script_templates/last_away.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_last_away.ipynb
    # cp ~/pacman/script_templates/ghost_attack.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_ghost_attack.ipynb
    # cp ~/pacman/script_templates/trial_end.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_trial_end.ipynb
    # cp ~/pacman/script_templates/preprocessing.ipynb $HOME/pacman/preprocessing/$subject/scripts/${subject}_preprocessing.ipynb

    ## create kngiht server folders
    mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_onset"
    mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/first_move"
    mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/first_dot"
    mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/last_away"
    mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_end"
    mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/ghost_attack"
done

echo "All subjects processed."