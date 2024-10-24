import pandas as pd
import numpy as np
from scipy import signal, stats
import re
import sys
import os
import mne
import mne_connectivity
import scipy
import joblib
import itertools
import pickle
import tensorpac as tp


## Prep paths ##
preproc_data_dir = f"/global/scratch/users/bstavel/pacman/preprocessing/"
t7_folder = '/global/scratch/users/bstavel/pacman/connectivity/ieeg/pac/avoid/'

## Load in the electrodes with sig theta coherence
# Load sig pairs data
sg_full_df = pd.read_csv('/global/scratch/users/bstavel/pacman/connectivity/scripts/pac/sig_theta_pairs.csv')

# Filter the DataFrame
sg_df = sg_full_df[
    (sg_full_df['roi_pair'].isin(['ofc_insula', 'ofc_amyg', 'ofc_hc', 'ofc_dlpfc', 'ofc_cing'])) &
    (sg_full_df['metric'] == 'Imaginary Coherence')
]

# Add elec1 and elec2 columns
sg_df['elec1'] = sg_df['pairs'].str.replace('_to_.*', '', regex=True)
sg_df['elec2'] = sg_df['pairs'].str.replace('.*_to_', '', regex=True)

def find_largest_cluster_mask(matrix):

    if not matrix.any():
        return matrix
    
    # Label the connected components in the inverted matrix
    labeled_array, num_features = label(matrix)
    
    # Find the size of each connected component
    component_sizes = np.bincount(labeled_array.ravel())
    
    # Exclude the background component (label 0)
    largest_component_label = component_sizes[1:].argmax() + 1
    
    # Create a mask for the largest component
    largest_cluster_mask = (labeled_array == largest_component_label).astype(int)
    
    return largest_cluster_mask

def find_pair_pac_pvalue(p):

    # create average pac and average perm pac by averaging over trials
    average_perm_pac = p.surrogates.mean(-1)
    average_pac = p.pac.mean(-1)

    # find the uncorrected p values
    tmp = average_pac <= average_perm_pac
    uncorrected_p = np.sum(tmp, axis = 0)/200

    # create a mask of largest sig cluster
    mask = uncorrected_p.copy()
    mask[uncorrected_p > .01] = 0
    mask[uncorrected_p <= .01] = 1
    large_cluster = find_largest_cluster_mask(mask)

    if np.sum(large_cluster) >= 5:

        # sum pac values in the largest cluster for each surrogate
        perm_test_stat = np.zeros((200, 1))
        for i in range(200):
            tmp = average_perm_pac[i, :, :]
            tmp[large_cluster == 0] = 0
            perm_test_stat[i] = np.sum(tmp)  

        # get summed pac value of the real data
        real_pac = average_pac.copy()
        real_pac[large_cluster == 0] = 0
        test_stat = np.sum(real_pac) 

        # get the p value
        pval = np.sum(test_stat <= perm_test_stat)/200
    else:
        # get summed pac value of the real data
        real_pac = average_pac.copy()
        real_pac[large_cluster == 0] = 0
        test_stat = np.sum(real_pac) 
        pval = 1        


    return test_stat, pval, large_cluster

## From OFC

# intialize results pd
results = pd.DataFrame(columns = ['subject', 'elec1', 'elec2', 'test_stat', 'pval'])

# get all the files
all_files = os.listdir(f'{t7_folder}/from_ofc')
pac_files= list(filter(lambda s: '_to_' in s, all_files))

# loop through all the files
for file in pac_files:
    with open(f'{t7_folder}/from_ofc/{file}', 'rb') as f:
        p = pickle.load(f)

    # calculate p value
    test_stat, pval, cluster= find_pair_pac_pvalue(p)

    # get subject and electrode info
    sub, elec1, _, elec2, _ = file.split("_")

    # add to results
    results = pd.concat([results, pd.DataFrame({'subject': [sub], 'elec1': [elec1], 'elec2': [elec2], 'test_stat': [test_stat], 'pval': [pval]})])

# left join with sg_df
compiled_results = results.merge(sg_df, left_on = ['subject', 'elec1', 'elec2'], right_on = ['subject', 'elec1', 'elec2'], how = 'left')

# save results
compiled_results.to_csv(f'{t7_folder}/compiled_avoid_from_ofc_results.csv', index = False)


## To OFC

# intialize results pd
results = pd.DataFrame(columns = ['subject', 'elec1', 'elec2', 'test_stat', 'pval'])

# get all the files
all_files = os.listdir(f'{t7_folder}/to_ofc')
pac_files= list(filter(lambda s: '_to_' in s, all_files))

# loop through all the files
for file in pac_files:
    with open(f'{t7_folder}/to_ofc/{file}', 'rb') as f:
        p = pickle.load(f)

    # calculate p value
    test_stat, pval, cluster= find_pair_pac_pvalue(p)

    # get subject and electrode info
    sub, elec1, _, elec2, _ = file.split("_")

    # add to results
    results = pd.concat([results, pd.DataFrame({'subject': [sub], 'elec1': [elec1], 'elec2': [elec2], 'test_stat': [test_stat], 'pval': [pval]})])

# left join with sg_df
compiled_results = results.merge(sg_df, left_on = ['subject', 'elec1', 'elec2'], right_on = ['subject', 'elec1', 'elec2'], how = 'left')

# save results
compiled_results.to_csv(f'{t7_folder}/compiled_avoid_to_ofc_results.csv', index = False)