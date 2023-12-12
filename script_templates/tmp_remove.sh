# Define the list of subjects
subjects=( "BJH026" "LL19" "IR102" "IR103" "IR104" "BJH030" "BJH039" "BJH041" )

# Loop over each subject
for subject in "${subjects[@]}"; do
    echo "Processing $subject..."

    # # Create directories
    rm -rf "$HOME/pacman/preprocessing/$subject/ieeg"

    ## create kngiht server folders
    mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/trial_onset"
    mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/first_move"
    mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/first_dot"
    mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/last_away"
    mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/trial_end"
    mkdir -p "$HOME/pacman/preprocessing/$subject/ieeg/ghost_attack"


    # ## create kngiht server folders
    # mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_onset"
    # mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/first_move"
    # mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/first_dot"
    # mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/last_away"
    # mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_end"
    # mkdir -p "$HOME/knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/ghost_attack"

done
