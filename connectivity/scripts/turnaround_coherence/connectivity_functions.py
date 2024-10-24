## connectivity functions

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


def compute_coherence(epochs, ch_names, roi_indices, freqs, n_cycles,  workers = 8):
    """ function to compute TFR via Morlet wavelets
    
    epochs:                     MNE epoch object with channels of interest
    freqs:                      list of frequencies, should be log spaced
    n_cycles:                   number of cycles, adjust with freqs to balance temporal and frequency resolution
    workers:                    number of threads to use while calculating TFR
    """
    print('computing TFR')
    connect = mne_connectivity.spectral_connectivity_epochs(data = epochs,
                                                            names = ch_names,
                                                            method = ['imcoh', 'ppc', 'wpli2_debiased'],
                                                            indices = roi_indices,
                                                            mode = 'cwt_morlet',
                                                            block_size=50000,
                                                            cwt_freqs = freqs,
                                                            cwt_n_cycles = n_cycles,
                                                            n_jobs = workers)

    return connect


def compute_epoch_coherence(epochs, ch_names, roi_indices, freqs, n_cycles,  workers = 8):
    """ function to compute TFR via Morlet wavelets
    
    epochs:                     MNE epoch object with channels of interest
    freqs:                      list of frequencies, should be log spaced
    n_cycles:                   number of cycles, adjust with freqs to balance temporal and frequency resolution
    workers:                    number of threads to use while calculating TFR
    """
    print('computing TFR')
    connect = mne_connectivity.spectral_connectivity_time(data = epochs,
                                                            method = ['coh', 'ciplv', 'wpli'],
                                                            indices = roi_indices,
                                                            mode = 'cwt_morlet',
                                                            freqs = freqs,
                                                            padding = 1,
                                                            n_cycles = n_cycles,
                                                            n_jobs = workers)

    return connect



def shuffle_epochs(epoch1):
    """
    Shuffles trials in the first epoch object and then combines it with the second epoch object.

    Parameters:
    epoch1 (mne.Epochs): The first epoch object to be shuffled.

    Returns:
    mne.Epochs: The shuffled epoch.
    """

    # Shuffle the first epoch
    indices = np.arange(len(epoch1))
    np.random.shuffle(indices)
    shuffled_epoch1 = epoch1[indices]


    return shuffled_epoch1


def get_indices_of_connectivity_pairs(roi_lists, ch_names):
    """
    Generates indices of channel names corresponding to unique, non-symmetric pairs 
    formed from a list of Regions of Interest (ROIs).

    Parameters:
    roi_lists (list of lists): A list where each element is a list of ROIs (Region of Interest).
                            Each sublist represents a different ROI category.
    ch_names (list): A list of channel names.

    Returns:
    tuple of lists: Two lists containing the indices. The first list contains indices from ch_names 
                    that match the first element of each pair. The second list contains indices from 
                    ch_names that match the second element of each pair.

    Example:
    roi_lists = [roi_list1, roi_list2, ...]
    ch_names = ["ch1", "ch2", "ch3", ...]
    first_pair_indices, second_pair_indices = get_indices_of_connectivity_pairs(roi_lists, ch_names)
    """

    # Generate all unique, non-symmetric pairs from the ROI lists
    pairs = [(item1, item2) for i, list1 in enumerate(roi_lists) 
                            for j, list2 in enumerate(roi_lists) 
                            if i < j 
                            for item1, item2 in itertools.product(list1, list2)]

    # Find indices in ch_names matching the first element of each pair
    first_pair_indices = [idx for pair in pairs 
                                    for idx, roi in enumerate(ch_names) 
                                    if roi == pair[0]]

    # Find indices in ch_names matching the second element of each pair
    second_pair_indices = [idx for pair in pairs 
                                    for idx, roi in enumerate(ch_names) 
                                    if roi == pair[1]]
    
    return first_pair_indices, second_pair_indices