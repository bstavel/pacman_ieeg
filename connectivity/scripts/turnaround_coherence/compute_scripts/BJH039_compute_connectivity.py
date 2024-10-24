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
sys.path.append('/global/scratch/users/bstavel/pacman/connectivity/scripts')
from connectivity_functions import *

## No Amygdala, No Insula

## Prep paths ##
subject_list = ['BJH039']

for subject in subject_list:
    preproc_data_dir = f"/global/scratch/users/bstavel/pacman/preprocessing/"

    ## Load Neural Data

    # load
    last_away_epochs = mne.read_epochs(f"{preproc_data_dir}/ieeg/{subject}_bp_filtered_clean_last_away_events.fif")

    # get good epochs (for behavioral data only)
    good_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if not x]
    bad_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if  x]

    # load behavioral data
    last_away_data = pd.read_csv(f"{preproc_data_dir}/behave/{subject}_last_away_events.csv")

    # set info as metadata
    last_away_epochs.metadata = last_away_data

    # onlt good epochs
    last_away_epochs = last_away_epochs[good_epochs]


    ## Dictionary of electrode locations ##

    # Dictionary mapping ROI to elecs
    # Pull mapping ROI to elecs
    with open('/global/scratch/users/bstavel/pacman/scripts/roi.py') as file:
        exec(file.read())
    ROIs = ROIs[subject]

    ## prep lists

    # primary ROI
    hc_list = []
    hc_indices = []
    hc_names = []
    ofc_list = []
    ofc_indices = []
    ofc_names = []
    amyg_list = []
    amyg_names = [] 
    amyg_indices = []
    cing_list = []
    cing_names = [] 
    cing_indices = []

    # control ROI
    insula_list = []
    insula_names = []  
    insula_indices = []
    dlpfc_list = []
    dlpfc_names = []  
    dlpfc_indices = []
    ec_list = []
    ec_names = []  
    ec_indices = []

    # exclude bad ROI from list
    pairs_long_name = [ch.split('-') for ch in last_away_epochs.info['ch_names']]
    bidx = len(last_away_epochs.info['bads']) +1
    pairs_name = pairs_long_name[bidx:len(pairs_long_name)]

    # sort ROI into lists
    for ix in range(0, len(pairs_name)):
        if pairs_name[ix][0] in ROIs['hc'] or pairs_name[ix][1] in ROIs['hc']:
            hc_list.append(last_away_epochs.info['ch_names'][ix + bidx])
            hc_names.append(pairs_name[ix])
            hc_indices.append(ix)
        if pairs_name[ix][0] in ROIs['ofc'] or pairs_name[ix][1] in ROIs['ofc']:
            ofc_list.append(last_away_epochs.info['ch_names'][ix + bidx])
            ofc_names.append(pairs_name[ix])
            ofc_indices.append(ix)
        if pairs_name[ix][0] in ROIs['amyg'] or pairs_name[ix][1] in ROIs['amyg']:
            amyg_list.append(last_away_epochs.info['ch_names'][ix + bidx])       
            amyg_names.append(pairs_name[ix])
            amyg_indices.append(ix)
        if pairs_name[ix][0] in ROIs['cing'] or pairs_name[ix][1] in ROIs['cing']:
            cing_list.append(last_away_epochs.info['ch_names'][ix + bidx])       
            cing_names.append(pairs_name[ix])
            cing_indices.append(ix)
            
        # control roi
        if pairs_name[ix][0] in ROIs['insula'] or pairs_name[ix][1] in ROIs['insula']:
            insula_list.append(last_away_epochs.info['ch_names'][ix + bidx])       
            insula_names.append(pairs_name[ix])
            insula_indices.append(ix)
        if pairs_name[ix][0] in ROIs['dlpfc'] or pairs_name[ix][1] in ROIs['dlpfc']:
            dlpfc_list.append(last_away_epochs.info['ch_names'][ix + bidx])       
            dlpfc_names.append(pairs_name[ix])
            dlpfc_indices.append(ix)
        if pairs_name[ix][0] in ROIs['ec'] or pairs_name[ix][1] in ROIs['ec']:
            ec_list.append(last_away_epochs.info['ch_names'][ix + bidx])       
            ec_names.append(pairs_name[ix])
            ec_indices.append(ix)        
            

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

    # permutations #
    permutations = 1000

    # resample 
    if last_away_epochs.info['sfreq'] > 1000:
        last_away_epochs= last_away_epochs.resample(100)

    # Crop #
    last_away_epochs.crop(tmin = -2.5, tmax = 2.5) 

    ## remove any electrodes that are duplicated across regions... ugh so much code for such a simple thing ##
    # Combine all ROI lists into a single Series
    elec_list = pd.Series(hc_list + ofc_list + cing_list + dlpfc_list)

    # Identify duplicated elements
    duplicated_list = elec_list[elec_list.duplicated()].tolist()

    # ROI lists
    roi_lists = [hc_list, ofc_list, cing_list, dlpfc_list]

    # Find indices of last occurrences of duplicated elements
    items_to_remove = [(sub_roi, idx_list) for idx_list, sub_list in enumerate(roi_lists) 
                    for idx, sub_roi in enumerate(sub_list) 
                    if sub_roi in duplicated_list and 
                        idx == len(sub_list) - sub_list[::-1].index(sub_roi) - 1]

    # Convert to list of tuples with unique first elements
    items_to_remove = list({t[0]: t for t in items_to_remove}.values())

    # remove elements
    for item in items_to_remove:
        roi_lists[item[1]].remove(item[0])

    # reset roi lists
    hc_list = roi_lists[0]
    ofc_list = roi_lists[1]
    cing_list = roi_lists[2]
    dlpfc_list = roi_lists[3]
    roi_lists = [hc_list, ofc_list, cing_list, dlpfc_list]

    for perm in range(0, permutations):

        # Prep for new permutation
        roi_coherence = []
        last_away_hc = last_away_epochs.copy().pick_channels(hc_list)
        last_away_ofc = last_away_epochs.copy().pick_channels(ofc_list)
        last_away_cing = last_away_epochs.copy().pick_channels(cing_list)
        last_away_dlpfc = last_away_epochs.copy().pick_channels(dlpfc_list)

        ## shuffle trials ##
        last_away_hc = shuffle_epochs(last_away_hc)
        last_away_ofc = shuffle_epochs(last_away_ofc)
        last_away_cing = shuffle_epochs(last_away_cing)
        last_away_dlpfc = shuffle_epochs(last_away_dlpfc)

        ## combine ##
        last_away_roi = last_away_hc.add_channels([last_away_ofc, last_away_cing, last_away_dlpfc])

        ## get indicies for all the noon-symmetric pairs ##
        first_pair_indices, second_pair_indices = get_indices_of_connectivity_pairs(roi_lists, last_away_roi.info['ch_names'])

        ## compute connectivity ##
        roi_coherence = compute_coherence(last_away_roi, last_away_roi.info.ch_names, (first_pair_indices, second_pair_indices), theta_freqs, theta_cycles, workers = 28)

        # pull out different measures #
        imcoh = roi_coherence[0].get_data().mean(axis = 1)
        ppc = roi_coherence[1].get_data().mean(axis = 1)
        pli = roi_coherence[2].get_data().mean(axis = 1)

        if perm == 0:
            imcoh_permutations = imcoh.copy()
            ppc_permutations = ppc.copy()
            pli_permutations = pli.copy()
        else:
            imcoh_permutations = np.vstack([imcoh_permutations, imcoh])
            ppc_permutations = np.vstack([ppc_permutations, ppc])
            pli_permutations = np.vstack([pli_permutations, pli])
            

        if perm % 10 == 0:
            np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_imcoh_perm.npy', imcoh_permutations)
            np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_ppc_perm.npy', ppc_permutations)
            np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_pli_perm.npy', pli_permutations)

    # final save
    np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_imcoh_perm.npy', imcoh_permutations)
    np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_ppc_perm.npy', ppc_permutations)
    np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_pli_perm.npy', pli_permutations)
    np.save(f'/global/scratch/users/bstavel/pacman/across_subject_analyses/ieeg/connectivity/perms/{subject}_pairs.npy', (first_pair_indices, second_pair_indices))

