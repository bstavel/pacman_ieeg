#!/usr/bin/env python
# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal, stats
import re
import os
import mne
import mne_connectivity
import IPython
import seaborn as sns
import scipy
import joblib
import h5io
import dask.array as da 
import itertools
import sys
import statsmodels
from statsmodels import stats
from statsmodels.stats import multitest

# custom scripts
sys.path.append('/home/brooke/pacman/connectivity/scripts/granger')

## Prep paths ##
subject_list = ['BJH046', 'BJH050', 'SLCH018', 'BJH051', 'BJH021', 'BJH025', 'BJH016', 'BJH026', 'BJH027', 'BJH029', 'BJH039', 'BJH041', 'LL10', 'LL12', 'LL13', 'LL14', 'LL17', 'LL19', 'SLCH002', 'BJH017']
pair_list = ['ofc_cing', 'ofc_mfg', 'amyg_ofc', 'amyg_cing', 'amyg_mfg', 'hc_amyg', 'hc_ofc', 'hc_mfg', 'hc_cing']

# load sig pairs
sig_df = pd.read_csv('/home/brooke/pacman/connectivity/sig_theta_pairs.csv')
sig_df = sig_df[sig_df['metric'] == "Imaginary Coherence"]
sig_df = sig_df[sig_df['roi_pair'].isin(pair_list)]

# split pairs on "_to_" into elec1, elec2
sig_df['elec1'] = [x.split('_to_')[0] for x in sig_df['pairs']]
sig_df['elec2'] = [x.split('_to_')[1] for x in sig_df['pairs']]

perms = 200

for subject in subject_list:
    preproc_data_dir = f"/home/brooke/pacman/preprocessing/"

    ## Load Neural Data

    # load
    last_away_epochs = mne.read_epochs(f"{preproc_data_dir}/{subject}/ieeg/{subject}_bp_filtered_clean_last_away_events.fif")

    # get good epochs (for behavioral data only)
    good_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if not x]
    bad_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if  x]

    # load behavioral data
    last_away_data = pd.read_csv(f"{preproc_data_dir}/../raw_data/{subject}/behave/{subject}_last_away_events.csv")

    # set info as metadata
    last_away_epochs.metadata = last_away_data

    # onlt good epochs
    last_away_epochs = last_away_epochs[good_epochs]

    # set attack FLAG
    attack = ['ghost']

    # load attack events
    ghost_attack_events = pd.read_csv(f"{preproc_data_dir}/../raw_data/{subject}/behave/{subject}_attack_events.csv")

    # add attack to metadata 
    last_away_epochs.metadata['attack'] = [1 if ghost_attack_events['neural_trial_numeric'].isin([x]).any() else 0 for x in last_away_epochs.metadata['neural_trial_numeric']]

    # filter to attack, escape, all
    if attack == ['attack']:
        last_away_epochs = last_away_epochs['attack == 1'].copy()
    elif attack == ['escape']:
        last_away_epochs = last_away_epochs['attack == 0'].copy()
    elif attack == ['ghost']:
        last_away_epochs = last_away_epochs['TrialType <= 16'].copy()
    elif attack == ['noghost']:
        last_away_epochs = last_away_epochs['TrialType > 16'].copy()

    ## Set frequencies ##
    freqs = np.logspace(start = np.log10(1), stop = np.log10(150), num = 80, base = 10, endpoint = True)
    n_cycles = np.logspace(np.log10(2), np.log10(30), base = 10, num = 80)

    # delta, theta, hfa
    delta_freqs = freqs[np.where((freqs <= 3))]
    delta_cycles = n_cycles[np.where((freqs <= 3))]

    theta_freqs = freqs[np.where((freqs > 3) & (freqs < 8))]
    theta_cycles = n_cycles[np.where((freqs > 3) & (freqs < 8))]

    hfa_freqs = freqs[np.where((freqs > 70))]
    hfa_cycles = n_cycles[np.where((freqs > 70))]

    # resample 
    if last_away_epochs.info['sfreq'] > 1000:
        last_away_epochs= last_away_epochs.resample(100)

    # Crop #
    last_away_epochs.crop(tmin = -2.5, tmax = 2.5) 

    # create subject specific sig df
    subject_sig_df = sig_df[sig_df['subject'] == subject]

    # loop over rows
    for row in subject_sig_df.iterrows():
        mfg_elec = row[1]['elec1']
        cing_elec = row[1]['elec2']
        region = row[1]['roi_pair']

        # pull out data
        elec1_epochs = last_away_epochs.copy().pick_channels([mfg_elec])
        elec2_epochs = last_away_epochs.copy().pick_channels([cing_elec])

        for perm in range(perms):

            # Shuffle the first epoch
            indices = np.arange(len(elec2_epochs))
            np.random.shuffle(indices)
            shuffled_epoch2 = elec2_epochs[indices]

            # recombine channels
            last_away_roi = elec1_epochs.copy().add_channels([shuffled_epoch2])

            # Convert to numpy arrays of dtype=object (as MNE expects)
            granger_indices = (np.array([[0], [1]]),  # row indices
                                np.array([[1], [0]])) # col indices

            ## compute connectivity ##
            roi_granger = mne_connectivity.spectral_connectivity_epochs(data = last_away_roi,
                                                                    names = last_away_roi.info['ch_names'],
                                                                    method = ['gc', 'gc_tr'],
                                                                    indices = granger_indices,
                                                                    mode = 'cwt_morlet',
                                                                    block_size=50000,
                                                                    cwt_freqs = theta_freqs,
                                                                    cwt_n_cycles = theta_cycles,
                                                                    gc_n_lags = 12,
                                                                    n_jobs = 16)

            # pull out forward/reverse granger #
            gc = roi_granger.copy()[0].get_data()
            gc_tr = roi_granger.copy()[1].get_data()

            # compute net granger
            net_gc = gc[0, :, :] - gc[1, :, :] 
            net_gc_tr = gc_tr[0, :, :] - gc_tr[1, :, :] 
            trgc = net_gc - net_gc_tr
            trgc_favg = trgc.mean(axis = 0)

            # create tmp pandas frame with granger data
            granger_tmp_df = pd.DataFrame(data = last_away_epochs.times, columns = ['times'])
            granger_tmp_df['granger'] = trgc_favg
            granger_tmp_df['subject'] = subject
            granger_tmp_df['pair'] = f"{mfg_elec}-{cing_elec}"
            granger_tmp_df['region'] = region
            granger_tmp_df['perm'] = perm

            if 'granger_df' in locals():
                granger_df = pd.concat([granger_df, granger_tmp_df], ignore_index=True)
            else:
                granger_df = granger_tmp_df.copy()


    if attack == ['attack']:
        # final save
        granger_df.to_csv(f'/home/brooke/pacman/connectivity/ieeg/granger/{subject}_granger_attack.csv')
    elif attack == ['escape']:
        # final save
        granger_df.to_csv(f'/home/brooke/pacman/connectivity/ieeg/granger/{subject}_granger_escape.csv')
    elif attack == ['ghost']:
        # final save
        granger_df.to_csv(f'/home/brooke/pacman/connectivity/ieeg/granger/null_granger_by_pair_ghost.csv')
    elif attack == ['noghost']:
        # final save
        granger_df.to_csv(f'/home/brooke/pacman/connectivity/ieeg/granger/{subject}_granger_noghost.csv')       
    else:
        # final save
        granger_df.to_csv(f'/home/brooke/pacman/connectivity/ieeg/granger/{subject}_granger_all.csv')

