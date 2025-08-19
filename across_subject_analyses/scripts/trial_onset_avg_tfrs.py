import matplotlib
# matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import signal, stats
import re
import os
import mne
import IPython
import seaborn as sns
import scipy
import joblib
import dask.array as da 
import pickle
import statsmodels
from statsmodels import stats
from statsmodels.stats import multitest

## import custom functions
import sys
sys.path.append('/home/brooke/pacman/preprocessing/scripts')
import preproc_functions as pf
import average_tfr_functions as avg_tfr
from roi import ROIs

# folders
raw_dir = '/home/brooke/pacman/raw_data'
preproc_dir = '/home/brooke/pacman/preprocessing'
tfr_dir = '/home/brooke/pacman/preprocessing' # used to be on the server
fig_dir = '../figures'

# subjects
sub_list = [
    'BJH021','BJH017','BJH046','BJH050','SLCH018','BJH051','BJH025','BJH016',
    'SLCH002','BJH026','BJH027','BJH029','BJH039','BJH041','LL10','LL12',
    'LL13','LL14','LL17','LL19'
]

# conditions
conditions = ['TrialType <= 16', 'TrialType > 16']

## Hippocampus
hcs = avg_tfr.calculate_trial_onset_average(sub_list, conditions, tfr_dir, 'hc')
hc_conflict, hc_noconflict = hcs
avg_tfr.plot_allsub_averages(
    hc_conflict,
    "Average Hippocampal TFR in Conflict Trials",
    os.path.join(fig_dir, 'average_hc_onset_conflict_all_subs.png'),
    -1, 5
)
avg_tfr.plot_allsub_averages(
    hc_noconflict,
    "Average Hippocampal TFR in No Conflict Trials",
    os.path.join(fig_dir, 'average_hc_onset_noconflict_all_subs.png'),
    -1, 5
)

## OFC
ofcs = avg_tfr.calculate_trial_onset_average(sub_list, conditions, tfr_dir, 'ofc')
ofc_conflict, ofc_noconflict = ofcs
avg_tfr.plot_allsub_averages(
    ofc_conflict,
    "Average OFC TFR in Conflict Trials",
    os.path.join(fig_dir, 'average_ofc_onset_conflict_all_subs.png'),
    -1, 5
)
avg_tfr.plot_allsub_averages(
    ofc_noconflict,
    "Average OFC TFR in No Conflict Trials",
    os.path.join(fig_dir, 'average_ofc_onset_noconflict_all_subs.png'),
    -1, 5
)

## Amygdala
amygs = avg_tfr.calculate_trial_onset_average(sub_list, conditions, tfr_dir, 'amyg')
amyg_conflict, amyg_noconflict = amygs
avg_tfr.plot_allsub_averages(
    amyg_conflict,
    "Average Amygdala TFR in Conflict Trials",
    os.path.join(fig_dir, 'average_amyg_onset_conflict_all_subs.png'),
    -1, 5
)
avg_tfr.plot_allsub_averages(
    amyg_noconflict,
    "Average Amygdala TFR in No Conflict Trials",
    os.path.join(fig_dir, 'average_amyg_onset_noconflict_all_subs.png'),
    -1, 5
)

## Anterior Cingulate
cings = avg_tfr.calculate_trial_onset_average(sub_list, conditions, tfr_dir, 'cing')
cing_conflict, cing_noconflict = cings
avg_tfr.plot_allsub_averages(
    cing_conflict,
    "Average Ant. Cingulate TFR in Conflict Trials",
    os.path.join(fig_dir, 'average_cing_onset_conflict_all_subs.png'),
    -1, 5
)
avg_tfr.plot_allsub_averages(
    cing_noconflict,
    "Average Ant. Cingulate TFR in No Conflict Trials",
    os.path.join(fig_dir, 'average_cing_onset_noconflict_all_subs.png'),
    -1, 5
)

## Middle Frontal Gryrus
mfgs = avg_tfr.calculate_trial_onset_average(sub_list, conditions, tfr_dir, 'dlpfc', ROIs = ROIs, subregion = 'mfg')
mfg_conflict, mfg_noconflict = mfgs
avg_tfr.plot_allsub_averages(
    mfg_conflict,
    "Average Middle Frontal Gyrus TFR in Conflict Trials",
    os.path.join(fig_dir, 'average_mfg_onset_conflict_all_subs.png'),
    -1, 5
)
avg_tfr.plot_allsub_averages(
    mfg_noconflict,
    "Average Middle Frontal Gyrus TFR in No Conflict Trials",
    os.path.join(fig_dir, 'average_mfg_onset_noconflict_all_subs.png'),
    -1, 5
)
