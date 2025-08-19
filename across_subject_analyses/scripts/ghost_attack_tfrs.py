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
tfr_dir = '/home/brooke/knight_server/remote/bstavel/pacman/preprocessing'

# subjects
sub_list = ['BJH021', 'BJH025', 'BJH016', 'SLCH002', 'BJH026', 'BJH027', 'BJH029', 'BJH039', 'BJH041', 'BJH017', 'BJH046', 'BJH050', 'BJH51', 'SLCH018', 'LL10', 'LL12', 'LL13', 'LL14', 'LL17', 'LL19']
mfg_sub_list = ['BJH021', 'BJH025','BJH016', 'SLCH002', 'BJH026', 'BJH027', 'BJH039', 'BJH046', 'BJH050', 'BJH51', 'LL12', 'LL13','LL14', 'LL17', 'LL19']

# conditions
conditions = ['TrialType <= 16']

## HC
all_subs_average_hcs = avg_tfr.calculate_ghost_attack_average(sub_list, tfr_dir, conditions, 'hc')
all_subs_average_hc_conflict = all_subs_average_hcs[0]
avg_tfr.plot_allsub_averages(all_subs_average_hc_conflict, "Average Hippocampal TFR During Ghost Attack", 'average_hc_ghost_attack_all_subs.png', -1, 3)

## OFC
all_subs_average_ofcs = avg_tfr.calculate_ghost_attack_average(sub_list, tfr_dir, conditions, 'ofc')
all_subs_average_ofc_conflict = all_subs_average_ofcs[0]
avg_tfr.plot_allsub_averages(all_subs_average_ofc_conflict, "Average OFC TFR During Ghost Attack", 'average_ofc_ghost_attack_all_subs.png', -1, 3)

## Anterior Cingulate
all_subs_average_cings = avg_tfr.calculate_ghost_attack_average(sub_list, tfr_dir, conditions, 'cing')
all_subs_average_cing_conflict = all_subs_average_cings[0]
avg_tfr.plot_allsub_averages(all_subs_average_cing_conflict, "Average Ant. Cingulate TFR During Ghost Attack", 'average_cing_ghost_attack_all_subs.png', -1, 3)

## Amygdala
all_subs_average_amygs = avg_tfr.calculate_ghost_attack_average(sub_list, tfr_dir, conditions, 'amyg')
all_subs_average_amyg_conflict = all_subs_average_amygs[0]
avg_tfr.plot_allsub_averages(all_subs_average_amyg_conflict, "Average Amygdala TFR During Ghost Attack", 'average_amyg_ghost_attack_all_subs.png', -1, 3)

## MFG
all_subs_average_dlpfcs = avg_tfr.calculate_subregion_ghost_attack_average(mfg_sub_list, conditions, 'dlpfc', 'mfg', ROIs)
all_subs_average_dlpfc_conflict = all_subs_average_dlpfcs[0]
avg_tfr.plot_allsub_averages(all_subs_average_dlpfc_conflict, "Average MFG TFR During Ghost Attack", 'average_mfg_ghost_attack_all_subs.png', -1, 3)