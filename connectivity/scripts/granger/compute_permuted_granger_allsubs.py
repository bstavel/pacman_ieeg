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



def process_subject(subject, sig_df, perms, preproc_data_dir="/global/scratch/users/bstavel/pacman/preprocessing/ieeg"):
    """
    Process one subject's data and save the resulting CSV.
    Returns the CSV filename (or you could return the final DataFrame if you prefer).
    """
    
    # Load neural data
    last_away_epochs = mne.read_epochs(f"{preproc_data_dir}/{subject}_bp_filtered_clean_last_away_events.fif")

    # get good epochs
    good_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if not x]
    bad_epochs  = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if x]

    # load behavioral data
    last_away_data = pd.read_csv(f"{preproc_data_dir}/../behave/{subject}_last_away_events.csv")
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
    elif attack == ['escape']:
        last_away_epochs = last_away_epochs['attack == 0'].copy()
    elif attack == ['ghost']:
        last_away_epochs = last_away_epochs['TrialType <= 16'].copy()
    elif attack == ['noghost']:
        last_away_epochs = last_away_epochs['TrialType > 16'].copy()

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

    # We'll accumulate results in a local DataFrame
    granger_df = []

    for _, row in subject_sig_df.iterrows():
        mfg_elec  = row['elec1']
        cing_elec = row['elec2']
        region    = row['roi_pair']

        # pick channels
        elec1_epochs = last_away_epochs.copy().pick_channels([mfg_elec])
        elec2_epochs = last_away_epochs.copy().pick_channels([cing_elec])

        for perm in range(perms):
            # Shuffle the second epoch
            indices = np.arange(len(elec2_epochs))
            np.random.shuffle(indices)
            shuffled_epoch2 = elec2_epochs[indices]

            # Recombine
            last_away_roi = elec1_epochs.copy().add_channels([shuffled_epoch2])

            # Indices for GC
            granger_indices = (
                np.array([[0], [1]]),  # row indices
                np.array([[1], [0]])   # col indices
            )

            # Compute connectivity
            roi_granger = mne_connectivity.spectral_connectivity_epochs(
                data        = last_away_roi,
                names       = last_away_roi.info['ch_names'],
                method      = ['gc', 'gc_tr'],
                indices     = granger_indices,
                mode        = 'cwt_morlet',
                block_size  = 50000,
                cwt_freqs   = theta_freqs,
                cwt_n_cycles= theta_cycles,
                gc_n_lags   = 12,
                n_jobs      = 16
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
            granger_tmp_df['pair']    = f"{mfg_elec}-{cing_elec}"
            granger_tmp_df['region']  = region
            granger_tmp_df['perm']    = perm

            granger_df.append(granger_tmp_df)

        # Concatenate
        granger_csv = pd.concat(granger_df, ignore_index=True)

        # Save
        if attack == ['attack']:
            out_path = f'{preproc_data_dir}/../../granger/results/{subject}_null_granger_attack.csv'
        elif attack == ['escape']:
            out_path = f'{preproc_data_dir}/../../granger/results/{subject}_null_granger_escape.csv'
        elif attack == ['ghost']:
            out_path = f'{preproc_data_dir}/../../granger/results/{subject}_null_granger_by_pair_ghost.csv'
        elif attack == ['noghost']:
            out_path = f'{preproc_data_dir}/../../granger/results/{subject}_null_granger_noghost.csv'
        else:
            out_path = f'{preproc_data_dir}/../../granger/results/{subject}_null_granger_all.csv'

        granger_csv.to_csv(out_path, index=False)
        print(f"Saved {out_path}")

    return out_path  # or return granger_df if you prefer



## Prep paths ##
preproc_data_dir="/global/scratch/users/bstavel/pacman/preprocessing/ieeg"

## Prep lists ##
subject_list = ['BJH046', 'BJH050', 'SLCH018', 'BJH051', 'BJH021', 'BJH025', 'BJH016', 'BJH026', 'BJH027', 'BJH029', 'BJH039', 'BJH041', 'LL10', 'LL12', 'LL13', 'LL14', 'LL17', 'LL19', 'SLCH002', 'BJH017']
pair_list = ['ofc_mfg', 'amyg_ofc', 'amyg_cing', 'hc_cing']

# load sig pairs
sig_df = pd.read_csv(f'{preproc_data_dir}/../../granger/sig_theta_pairs.csv')
sig_df = sig_df[sig_df['metric'] == "Imaginary Coherence"]
sig_df = sig_df[sig_df['roi_pair'].isin(pair_list)]

# split pairs on "_to_" into elec1, elec2
sig_df['elec1'] = [x.split('_to_')[0] for x in sig_df['pairs']]
sig_df['elec2'] = [x.split('_to_')[1] for x in sig_df['pairs']]

perms = 200

# n_jobs: number of parallel processes to use (choose based on CPU cores)
results = Parallel(n_jobs=4)(
    delayed(process_subject)(subject, sig_df, perms)
    for subject in subject_list
)