## funcions to compute power via morlet wavelts and save out to csvs

# Load libraries
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal, stats
import mat73
import re
from neurodsp.timefrequency import compute_wavelet_transform
import os
import mne
import IPython
import seaborn as sns
import scipy
import joblib
import h5io
import dask.array as da 


# Set frequencies
freqs = np.logspace(start = np.log10(1), stop = np.log10(150), num = 80, base = 10, endpoint = True)
n_cycles = np.logspace(np.log10(2), np.log10(30), base = 10, num = 80)

# formulas to check bandwidth and time bin
band_width = (freqs / n_cycles) * 2
time_bin = n_cycles / freqs / np.pi

def compute_TFR(epochs, freqs, n_cycles, workers = 8):
    """
    epochs:                     MNE epoch object with channels of interest
    freqs:                      list of frequencies, should be log spaced
    n_cycles:                   number of cycles, adjust with freqs to balance temporal and frequency resolution
    workers:                    number of threads to use while calculating TFR
    """
    print('computing TFR')
    TFR = mne.time_frequency.tfr_morlet(epochs,freqs,n_cycles,return_itc=False,
                                            average=False,  n_jobs = workers)
    return TFR

def log_and_zscore_TFR(TFR, baseline, logflag = True):
    """
    TFR:                        Transformed and log transformed data from compute_TFR
    logflag:                    Log transform or not, defaults to True
    baseline:                   tuple that specifies the time in seconds that baseline should be calculated on 
                                (should be 1-2s smaller than epoch TFR was calculated on to exclude artifacts on morlet waves
    """
    if logflag:
        print('log transforming')
        TFR.data = da.from_array(TFR.data, chunks="auto")  # Convert the data to a Dask array
        TFR.data = da.log(TFR.data)  # Compute the element-wise log
    
    print('z-scoring to baseline')
    bix = [a and b for a, b in zip(TFR.times >= baseline[0], TFR.times <= baseline[1])]
    bmean = TFR.data[:, :, :, bix].mean(axis=3, keepdims=True).mean(axis=0, keepdims=True)
    bstd = TFR.data[:, :, :, bix].std(axis=3, keepdims=True).std(axis=0, keepdims=True)
    TFR.data = (TFR.data - bmean) / bstd

    TFR.data = TFR.data.compute()  # Convert the Dask array back to a NumPy array
    return TFR

def extract_freqs(lower_freq, higher_freq, freq_band, subdir, ROI, label, TFR, trials):
    """ function to extract and average the across the freqs within a given band and save out to csvs
    step is calculated based on getting ~4 samples per frequency cycle
    
    lower_freq, higher_freq:    non inclusive lower and upper bounds of the band
    freq_band:                  band name, as a string
    subdir:                     dir in sub/ieeg/ that specifies the time locking
    ROI:                        region name, as a string
    label:                      label, eg itibase, no itibase, choice locked etc, as a string
    TFR:                        MNE TFR object
    """  
    # calculate step, every 50ms to match the behavioral data
    step = int(np.floor(TFR.info['sfreq']/20))
    
    # check if it needs to be calculated with subbands
    if freq_band == 'gamma' or freq_band == 'hfa':
        
        subband_dict = {
            'gamma'    : [(30, 40), (35, 45), (40, 50), (45, 55), (50, 60), (55, 65), (60, 70)],
            'hfa'      : [(70, 90), (80, 100), (90, 110), (100, 120), (110, 130), (120, 140), (130, 150)]
        }
        
        for chix in range(len(TFR.ch_names)):
            subb_trial_power = []
            for subb in subband_dict[freq_band]:
                fidx = np.where((freqs > subb[0]) & (freqs < subb[1]))[0]
                subb_trial_power.append(TFR.data[:, chix, fidx, :].mean(axis=1))
            trial_power = np.mean(subb_trial_power, axis = 0)
            channel_df = pd.DataFrame(rolling_avg_2d(trial_power, step))
            channel_df["trial"] = trials
            channel_df.to_csv(f"/home/brooke/pacman/preprocessing/{sub}/ieeg/{subdir}/{TFR.ch_names[chix]}_{ROI}_trial_{freq_band}_{label}.csv")
    
    else:
        fidx = np.where((freqs > lower_freq) & (freqs < higher_freq))[0]
        for chix in range(len(TFR.ch_names)):
            trial_power = TFR.data[:, chix, fidx, :].mean(axis=1)
            channel_df = pd.DataFrame(rolling_avg_2d(trial_power, step))
            channel_df["trial"] = trials
            channel_df.to_csv(f"/home/brooke/pacman/preprocessing/{sub}/ieeg/{subdir}/{TFR.ch_names[chix]}_{ROI}_trial_{freq_band}_{label}.csv")

def rolling_avg_2d(matrix, n, axis=1):
    if axis != 1:
        raise ValueError("Only axis=1 is supported for this function.")
    
    half_n = int(np.floor(n // 2))
    results = []
    
    for row in matrix:
        avg_row = []
        i = 0
        while i < len(row):
            start = max(0, i - half_n)
            end = min(len(row), i + half_n)
            avg = np.mean(row[start:end])
            avg_row.append(avg)
            i += n
        results.append(avg_row)
    
    return np.array(results)


def plot_average_tfr(tfr, title_str, subject, fig_name):
    """ function to plot TFRs
    tfr:                        MNE TFR object
    title_str:                  title of plot, as a string
    subject:                    subject ID, as a string
    fig_name:                   name of figure to save, as a string
    """
    plt.rcParams['figure.figsize'] = [22, 20]
    plt.rcParams.update({'font.size': 18})


    fig, ax = plt.subplots(figsize = (22, 20))
    i = ax.imshow(tfr.data.mean(axis = 0).mean(axis = 0), cmap = 'RdBu_r', interpolation="none", origin="lower", aspect = 'auto', extent=[tfr.tmin, tfr.tmax, freqs[0], freqs[-1]], vmin = -1, vmax = 1)
    ax.set_yticks(np.linspace(np.min(tfr.freqs),np.max(tfr.freqs),len(tfr.freqs))[::2])
    ax.set_yticklabels(np.round(tfr.freqs)[::2]) 
    i2 = plt.axvline(x=0, color='black', linestyle='--', linewidth = 5)
    bar = plt.colorbar(i)
    ax.set_title(title_str, fontsize=22, fontweight = 'bold')
    fig.savefig(f'figures/{subject}_average_{fig_name}.png', dpi=600)
    fig.show()

def plot_channel_tfr(tfr, chix, ch, title_str):
    """ function to plot TFRs
    tfr:                        MNE TFR object
    chix:                       channel index, as an int
    ch:                         channel name, as a string
    title_str:                  title of plot, as a string
    """
    plt.rcParams['figure.figsize'] = [22, 20]
    plt.rcParams.update({'font.size': 18})


    fig, ax = plt.subplots(figsize = (22, 20))
    i = ax.imshow(tfr.data[:, chix, :, :].mean(axis = 0), cmap = 'RdBu_r', interpolation="none", origin="lower", aspect = 'auto', extent=[tfr.tmin, tfr.tmax, freqs[0], freqs[-1]], vmin = -2.5, vmax = 2.5)
    ax.set_yticks(np.linspace(np.min(tfr.freqs),np.max(tfr.freqs),len(tfr.freqs))[::2])
    ax.set_yticklabels(np.round(tfr.freqs)[::2]) 
    bar = plt.colorbar(i)
    i2 = plt.axvline(x=0, color='black', linestyle='--', linewidth = 5)
    ax.set_title(f"{ch}:  {title_str}")
    fig.show()