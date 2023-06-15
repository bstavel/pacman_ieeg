#!/bin/bash

# Read the list of common folders from folders.txt
folders_list=("BJH016" "SLCH002" "LL10" "LL12" "LL13" "BJH021" "BJH025")


# Loop over each folder listed in folders.txt
for subject in $folders_list; do
    # move files 
    mv pacman/preprocessing/$subject/ieeg/last_away/*.h5 knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/last_away/
    mv pacman/preprocessing/$subject/ieeg/first_dot/*.h5 knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/first_dot/
    mv pacman/preprocessing/$subject/ieeg/trial_onset/*.h5 knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_onset/
    mv pacman/preprocessing/$subject/ieeg/trial_end/*.h5 knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_end/

    # Find all files in the current subfolder of /source/directory
    find knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/last_away/ -type f -exec sh -c 'ln -s "{}" "pacman/preprocessing/'"$subject"'/ieeg/last_away/$(basename "{}")"' \;
    find knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/first_dot/ -type f -exec sh -c 'ln -s "{}" "pacman/preprocessing/'"$subject"'/ieeg/first_dot/$(basename "{}")"' \;
    find knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_onset/ -type f -exec sh -c 'ln -s "{}" "pacman/preprocessing/'"$subject"'/ieeg/trial_onset/$(basename "{}")"' \;
    find knight_server/remote/bstavel/pacman/preprocessing/$subject/ieeg/trial_end/ -type f -exec sh -c 'ln -s "{}" "pacman/preprocessing/'"$subject"'/ieeg/trial_end/$(basename "{}")"' \;
    
done