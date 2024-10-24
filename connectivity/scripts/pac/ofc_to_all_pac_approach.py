import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal, stats
import re
import sys
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
from plotnine import *
import pickle
import statsmodels
from statsmodels import stats
from statsmodels.stats import multitest
import tensorpac as tp


## Prep paths ##
raw_data_dir = f"/home/brooke/pacman/raw_data/"
preproc_data_dir = f"/home/brooke/pacman/preprocessing/"
t7_folder = '/media/brooke/T7/pacman/connectivity/pac/approach/from_ofc'

## Load in the electrodes with sig theta coherence
# Load sig pairs data
sg_full_df = pd.read_csv('/home/brooke/pacman/connectivity/scripts/pac/sig_theta_pairs.csv')

# Filter the DataFrame
sg_df = sg_full_df[
    (sg_full_df['roi_pair'].isin(['ofc_insula', 'ofc_amyg', 'ofc_hc', 'ofc_dlpfc', 'ofc_cing'])) &
    (sg_full_df['metric'] == 'Imaginary Coherence')
]

# Add elec1 and elec2 columns
sg_df['elec1'] = sg_df['pairs'].str.replace('_to_.*', '', regex=True)
sg_df['elec2'] = sg_df['pairs'].str.replace('.*_to_', '', regex=True)

# load compelted pac analyses
from_ofc_done = pd.read_csv('/home/brooke/pacman/connectivity/scripts/pac/compiled_approach_from_ofc_results.csv')

# Perform the anti-join
merged_df = sg_df.merge(from_ofc_done, on=['subject', 'elec1', 'elec2'], how='left', indicator=True)

# Filter the rows that are only in sg_df
remaining_df = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

# fix and drop columns
remaining_df.drop(['test_stat', 'pval', 'pairs_y', 'roi_pair_y', 'metric_y'], axis=1, inplace=True)
rename_mapping = dict(zip(remaining_df.columns, sg_df.columns))
remaining_df.rename(columns=rename_mapping, inplace=True)

# replace sg_df with the updated version
sg_df = remaining_df

## prep pac objects
# Get the freqs for the phase, amplitude
p_freqs = tp.Pac(idpac=(2, 0, 0), f_pha='hres', f_amp='hres')
theta_phases = [x for x in p_freqs.f_pha if x[0] >= 2 and x[1] <= 9]
hfa_amps = [x for x in p_freqs.f_amp if x[0] >= 70]
# main pac object
p = tp.Pac(idpac=(2, 0, 0), f_pha=theta_phases, f_amp=hfa_amps)

# Get Sub list
subject_list = sg_df['subject'].unique()

# Loop over subject
for sub in subject_list:

    # filter to current subject
    sub_df = sg_df[sg_df['subject'] == sub]

    ## Load Neural Data
    # load
    last_away_epochs = mne.read_epochs(f"{preproc_data_dir}/{sub}/ieeg/{sub}_bp_filtered_clean_last_away_events.fif")

    if sub == 'LL14':
        # get good epochs (for behavioral data only) & Manually add more bad trials because of a bipolar referencing issue that created NANs
        good_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if not x and i not in [432, 433, 484, 628, 634, 635]]
        bad_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if  x or i in [432, 433, 484, 628, 634, 635]]
    else:
        # get good epochs (for behavioral data only)
        good_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if not x]
        bad_epochs = [i for i,x in enumerate(last_away_epochs.get_annotations_per_epoch()) if  x]

    # load behavioral data
    last_away_data = pd.read_csv(f"{raw_data_dir}/{sub}/behave/{sub}_last_away_events.csv")

    # set info as metadata
    last_away_epochs.metadata = last_away_data

    # onlt good epochs
    last_away_epochs = last_away_epochs[good_epochs]

    # only approach
    last_away_epochs = last_away_epochs.crop(tmin=-2, tmax=0)

    # downsample to 512 Hz since LL is maxed out at 512
    last_away_epochs = last_away_epochs.resample(512)

    # Get the ofc elec list
    ofc_list = sub_df['elec1'].unique()

    # Loop over ofc elecs
    for ofc_elec in ofc_list:

        # filter to current ofc elec
        ofc_elec_df = sub_df[sub_df['elec1'] == ofc_elec]

        # prep ofc elec
        ofc_data = last_away_epochs.copy().pick([ofc_elec])
        ofc_array = np.squeeze(ofc_data.get_data())

        # get the amplitudes
        phases = p.filter(last_away_epochs.info['sfreq'], ofc_array, ftype='phase', n_jobs = 16)

        # get ofc elec pairs
        ofc_pairs_list = ofc_elec_df['elec2'].unique()

        # loop over the other elecs
        for roi_pair in ofc_pairs_list:

            # prep roi pair
            roi_data = last_away_epochs.copy().pick([roi_pair])
            roi_array = np.squeeze(roi_data.get_data())

            # get the phases
            amplitudes = p.filter(last_away_epochs.info['sfreq'], roi_array, ftype='amplitude', n_jobs = 16)

            # get the pac
            p.idpac = (2, 3, 4)
            xpac = p.fit(phases, amplitudes, n_perm=200, n_jobs = 16, mcp = 'fdr')

            # Save the object to a file
            with open(f'{t7_folder}/{sub}_{ofc_elec}_to_{roi_pair}_pac.pkl', 'wb') as file:
                pickle.dump(p, file)