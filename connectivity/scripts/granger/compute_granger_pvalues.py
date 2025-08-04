#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

from plotnine import (
    ggplot,
    aes,
    geom_line,
    facet_wrap,
    labs,
    geom_hline,
    element_text,
    scale_alpha_manual,
    scale_color_manual,
    theme,
    ggtitle
)

# custom scripts
sys.path.append('/home/brooke/pacman/connectivity/scripts/turnaround_coherence')
from connectivity_functions import *


def compute_pvals_for_group(group):
    """
    group: subset of 'granger' for a specific (pair, time)
    We look up the sorted null distribution for that (pair, time)
    and compute the p-values in bulk.
    """
    # group.name is now a tuple (pair, time)
    pair, time = group.name
    dist_sorted = null_distributions[(pair, time)]
    # Compute the absolute granger values
    vals = np.abs(group['granger'].to_numpy())
    # Use searchsorted to determine the number of null values greater than each true value
    idx = np.searchsorted(dist_sorted, vals, side='right')
    count_greater = len(dist_sorted) - idx
    # Use .loc to avoid potential SettingWithCopyWarning
    group.loc[:, 'pval'] = count_greater / len(dist_sorted)
    return group



# load in true data
granger_path = f'/home/brooke/pacman/connectivity/ieeg/granger/all_subs_all_roi_true_granger.csv'

#read in csv
granger = pd.read_csv(granger_path)

# limit time
granger = granger[(granger['times'] >= -1.5) & (granger['times'] <= 1.5)]


## Prep paths ##
subject_list = ['BJH046', 'BJH050', 'SLCH018', 'BJH051', 'BJH021', 'BJH025', 'BJH016', 'BJH026', 'BJH027', 'BJH029', 'BJH039', 'BJH041', 'LL10', 'LL12', 'LL13', 'LL14', 'LL17', 'LL19', 'SLCH002', 'BJH017']
pair_list = ['ofc_cing', 'ofc_mfg', 'amyg_ofc', 'amyg_cing', 'amyg_mfg', 'hc_amyg', 'hc_ofc', 'hc_mfg', 'hc_cing', 'mfg_cing']

for subject in granger['subject'].unique():

    # filter to subject
    sub_true_granger = granger[granger['subject'] == subject]
    # load in null data
    null_path = f'/home/brooke/pacman/connectivity/ieeg/granger/{subject}_null_granger_all_ghost.csv'
    null = pd.read_csv(null_path)

    # Build a dictionary of sorted null distributions for each pair_id
    null_distributions = (
        null
        .groupby(['pair', 'times'])['granger']
        .apply(lambda x: np.sort(np.abs(x).to_numpy()))
        .to_dict()
    )

    # Compute p-values for each group and assign back
    sub_true_granger = sub_true_granger.groupby(['pair', 'times'], group_keys=False).apply(compute_pvals_for_group)

    # bind to new df
    if subject == granger['subject'].unique()[0]:
        all_sub_true_granger = sub_true_granger
    else:
        all_sub_true_granger = pd.concat([all_sub_true_granger, sub_true_granger])


## save out
all_sub_true_granger.to_csv('/home/brooke/pacman/connectivity/ieeg/granger/all_subs_all_roi_true_granger_dir.csv', index=False)


