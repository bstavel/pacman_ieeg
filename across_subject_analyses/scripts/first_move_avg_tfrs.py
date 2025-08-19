import matplotlib
# matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import mne
import seaborn as sns
import joblib
import dask.array as da
import pickle
from statsmodels import stats
from statsmodels.stats import multitest

## import custom functions
import sys
sys.path.append('/home/brooke/pacman/preprocessing/scripts')
import preproc_functions as pf
import average_tfr_functions as avg_tfr
from roi import ROIs

# folders
raw_dir    = '/home/brooke/pacman/raw_data'
preproc_dir= '/home/brooke/pacman/preprocessing'
tfr_dir    = '/home/brooke/knight_server/remote/bstavel/pacman/preprocessing'
fig_dir    = '../figures'

# subjects
sub_list = [
    'BJH021','BJH017','BJH046','BJH050','SLCH018','BJH051','BJH025','BJH016',
    'SLCH002','BJH026','BJH027','BJH029','BJH039','BJH041','LL10','LL12',
    'LL13','LL14','LL17','LL19'
]


# conditions (string filters)
conditions = ['TrialType <= 16', 'TrialType > 16']

# ## Hippocampus — First Move
# hcs_fm = avg_tfr.calculate_first_move_average(
#     sub_list, conditions, tfr_dir, 'hc'
# )
# hc_fm_conflict, hc_fm_noconflict = hcs_fm
# avg_tfr.plot_allsub_averages(
#     hc_fm_conflict,
#     "Average Hippocampal TFR in Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_hc_first_move_conflict_all_subs.png'),
#     -1, 4
# )
# avg_tfr.plot_allsub_averages(
#     hc_fm_noconflict,
#     "Average Hippocampal TFR in No Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_hc_first_move_noconflict_all_subs.png'),
#     -1, 4
# )

# ## OFC — First Move
# ofcs_fm = avg_tfr.calculate_first_move_average(
#     sub_list, conditions, tfr_dir, 'ofc'
# )
# ofc_fm_conflict, ofc_fm_noconflict = ofcs_fm
# avg_tfr.plot_allsub_averages(
#     ofc_fm_conflict,
#     "Average OFC TFR in Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_ofc_first_move_conflict_all_subs.png'),
#     -1, 4
# )
# avg_tfr.plot_allsub_averages(
#     ofc_fm_noconflict,
#     "Average OFC TFR in No Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_ofc_first_move_noconflict_all_subs.png'),
#     -1, 4
# )

# ## Amygdala — First Move
# amygs_fm = avg_tfr.calculate_first_move_average(
#     sub_list, conditions, tfr_dir, 'amyg'
# )
# amyg_fm_conflict, amyg_fm_noconflict = amygs_fm
# avg_tfr.plot_allsub_averages(
#     amyg_fm_conflict,
#     "Average Amygdala TFR in Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_amyg_first_move_conflict_all_subs.png'),
#     -1, 4
# )
# avg_tfr.plot_allsub_averages(
#     amyg_fm_noconflict,
#     "Average Amygdala TFR in No Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_amyg_first_move_noconflict_all_subs.png'),
#     -1, 4
# )

# ## Anterior Cingulate — First Move
# cings_fm = avg_tfr.calculate_first_move_average(
#     sub_list, conditions, tfr_dir, 'cing'
# )
# cing_fm_conflict, cing_fm_noconflict = cings_fm
# avg_tfr.plot_allsub_averages(
#     cing_fm_conflict,
#     "Average Ant. Cingulate TFR in Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_cing_first_move_conflict_all_subs.png'),
#     -1, 4
# )
# avg_tfr.plot_allsub_averages(
#     cing_fm_noconflict,
#     "Average Ant. Cingulate TFR in No Conflict Trials (First Move)",
#     os.path.join(fig_dir, 'average_cing_first_move_noconflict_all_subs.png'),
#     -1, 4
# )

## Middle Frontal Gyrus — First Move (subregion)
mfgs_fm = avg_tfr.calculate_first_move_average(
    sub_list, conditions, tfr_dir, 'dlpfc',
    ROIs=ROIs, subregion='mfg'
)
mfg_fm_conflict, mfg_fm_noconflict = mfgs_fm
avg_tfr.plot_allsub_averages(
    mfg_fm_conflict,
    "Average Middle Frontal Gyrus TFR in Conflict Trials (First Move)",
    os.path.join(fig_dir, 'average_mfg_first_move_conflict_all_subs.png'),
    -1, 4
)
avg_tfr.plot_allsub_averages(
    mfg_fm_noconflict,
    "Average Middle Frontal Gyrus TFR in No Conflict Trials (First Move)",
    os.path.join(fig_dir, 'average_mfg_first_move_noconflict_all_subs.png'),
    -1, 4
)
