#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from scipy import signal, stats
import re
import os
import mne
import mne_connectivity
import scipy
from joblib import Parallel, delayed
import h5io
import itertools
import sys



def process_subject(subject, sig_df, perms, preproc_data_dir, granger_dir):
    """
    Process one subject's data and save the resulting CSV.
    Returns the CSV filename (or you could return the final DataFrame if you prefer).
    """
    
    # Load neural data
    last_away_epochs = mne.read_epochs(f"{preproc_data_dir}/ieeg/{subject}_bp_filtered_clean_last_away_events.fif")

    # get good epochs
    good_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if not x]

    # load behavioral data
    last_away_data = pd.read_csv(f"{preproc_data_dir}/behave/{subject}_last_away_events.csv")
    last_away_epochs.metadata = last_away_data
    
    # only keep good epochs
    last_away_epochs = last_away_epochs[good_epochs]

    # choose which condition to filter (attack, ghost, etc.)
    attack = ['ghost']  # <--- CHANGE as needed

    # # load attack events
    # ghost_attack_events = pd.read_csv(f"{preproc_data_dir}/../raw_data/{subject}/behave/{subject}_attack_events.csv")

    # # add attack flag
    # last_away_epochs.metadata['attack'] = [
    #     1 if ghost_attack_events['neural_trial_numeric'].isin([x]).any() else 0
    #     for x in last_away_epochs.metadata['neural_trial_numeric']
    # ]

    # filter to the desired condition
    if attack == ['attack']:
        last_away_epochs = last_away_epochs['attack == 1'].copy()
        out_path = f'{granger_dir}/results/{subject}_null_granger_attack.csv'
    elif attack == ['escape']:
        last_away_epochs = last_away_epochs['attack == 0'].copy()
        out_path = f'{granger_dir}/results/{subject}_null_granger_escape.csv'
    elif attack == ['ghost']:
        last_away_epochs = last_away_epochs['TrialType <= 16'].copy()
        out_path = f'{granger_dir}/results/{subject}_null_granger_by_pair_ghost.csv'
    elif attack == ['noghost']:
        last_away_epochs = last_away_epochs['TrialType > 16'].copy()
        out_path = f'{granger_dir}/results/{subject}_null_granger_all.csv'

    # Define frequencies
    freqs     = np.logspace(start=np.log10(1), stop=np.log10(150), num=80, base=10)
    n_cycles  = np.logspace(np.log10(2), np.log10(30), num=80, base=10)

    # subset frequency bands
    theta_freqs   = freqs[(freqs > 3) & (freqs < 8)]
    theta_cycles  = n_cycles[(freqs > 3) & (freqs < 8)]

    # Resample if sfreq > 1000
    if last_away_epochs.info['sfreq'] > 1000:
        last_away_epochs = last_away_epochs.resample(100)

    # Crop
    last_away_epochs.crop(tmin=-2.5, tmax=2.5)

    # Filter sig_df for this subject
    subject_sig_df = sig_df[sig_df['subject'] == subject]

    if os.path.exists(out_path):
        # load the old results into a single‐element list
        _old = pd.read_csv(out_path)
        finished_pairs = _old['pair'].unique()
        subject_sig_df = subject_sig_df[~subject_sig_df['pairs'].isin(finished_pairs)]
        #  keep granger_df as a list of DataFrames
        granger_df = [_old]
    else:
        # Initialize an empty list to store DataFrames
        granger_df = []

    # prepare GC indices
    granger_indices = (
        np.array([[0], [1]]),  # forward
        np.array([[1], [0]])   # reverse
    )



    for _, row in subject_sig_df.iterrows():
        first_elec  = row['elec1']
        second_elec = row['elec2']
        region    = row['roi_pair']

        # pick channels
        elec1_epochs = last_away_epochs.copy().pick_channels([first_elec])
        elec2_epochs = last_away_epochs.copy().pick_channels([second_elec])

        for perm in range(perms):
            # Shuffle the second epoch
            indices = np.arange(len(elec2_epochs))
            np.random.shuffle(indices)
            shuffled_epoch2 = elec2_epochs[indices]

            # Recombine
            last_away_roi = elec1_epochs.copy().add_channels([shuffled_epoch2])

            # Compute connectivity
            roi_granger = mne_connectivity.spectral_connectivity_epochs(
                data        = last_away_roi,
                names       = last_away_roi.info['ch_names'],
                method      = ['gc', 'gc_tr'],
                indices     = granger_indices,
                mode        = 'cwt_morlet',
                block_size  = 1,
                cwt_freqs   = theta_freqs,
                cwt_n_cycles= theta_cycles,
                gc_n_lags   = 12,
                n_jobs      = 56
            )

            # Extract forward/reverse GC
            gc    = roi_granger.copy()[0].get_data()
            gc_tr = roi_granger.copy()[1].get_data()

            # net granger
            net_gc    = gc[0, :, :]    - gc[1, :, :]
            net_gc_tr = gc_tr[0, :, :] - gc_tr[1, :, :]
            trgc      = net_gc - net_gc_tr
            trgc_favg = trgc.mean(axis=0)

            # Create a temp df
            granger_tmp_df = pd.DataFrame({'times': last_away_epochs.times,
                                           'granger': trgc_favg})
            granger_tmp_df['subject'] = subject
            granger_tmp_df['pair']    = f"{first_elec}-{second_elec}"
            granger_tmp_df['region']  = region
            granger_tmp_df['perm']    = perm

            granger_df.append(granger_tmp_df)

        # Concatenate
        granger_csv = pd.concat(granger_df, ignore_index=True)

        granger_csv.to_csv(out_path, index=False)
        print(f"Saved {out_path}")

    return out_path  # or return granger_df if you prefer



## Prep paths ##
preproc_data_dir="/global/scratch/users/bstavel/pacman_ieeg/preprocessing_hpc"
granger_dir = "/global/scratch/users/bstavel/pacman_ieeg/connectivity/scripts/granger"

## Prep lists ##
subject_list = ['BJH046']
pair_list = ['ofc_mfg', 'amyg_ofc', 'amyg_cing', 'hc_cing']

# load sig pairs
sig_df = pd.read_csv(f'{granger_dir}/sig_theta_pairs.csv')
sig_df = sig_df[sig_df['metric'] == "Imaginary Coherence"]
sig_df = sig_df[sig_df['roi_pair'].isin(pair_list)]

# split pairs on "_to_" into elec1, elec2
sig_df['elec1'] = [x.split('_to_')[0] for x in sig_df['pairs']]
sig_df['elec2'] = [x.split('_to_')[1] for x in sig_df['pairs']]

perms = 1000

# n_jobs: number of parallel processes to use (choose based on CPU cores)
results = Parallel(n_jobs=1)(
    delayed(process_subject)(subject, sig_df, perms, preproc_data_dir, granger_dir)
    for subject in subject_list
)