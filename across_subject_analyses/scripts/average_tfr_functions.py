import matplotlib
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
import pickle
import statsmodels
from statsmodels import stats
from statsmodels.stats import multitest

## import custom functions
import sys
sys.path.append('/home/brooke/pacman/preprocessing/scripts')
import preproc_functions as pf
from roi import ROIs

# folders
raw_dir = '/home/brooke/pacman/raw_data'
preproc_dir = '/home/brooke/pacman/preprocessing'

def get_roi_elec_lists(ROIs, epochs, roi):

    # prep lists
    roi_list = []
    roi_names = []
    roi_indices = []

    # exclude bad ROI from list
    pairs_long_name = [ch.split('-') for ch in epochs.info['ch_names']]
    bidx = len(epochs.info['bads']) +1
    pairs_name = pairs_long_name[bidx:len(pairs_long_name)]

    # sort ROI into lists
    for ix in range(0, len(pairs_name)):
        if pairs_name[ix][0] in ROIs[roi] or pairs_name[ix][1] in ROIs[roi]:
            roi_list.append(epochs.info['ch_names'][ix + bidx])
            roi_names.append(pairs_name[ix])
            roi_indices.append(ix)

    return roi_list, roi_names, roi_indices

def calculate_trial_onset_average(sub_list, string_filters, tfr_dir, roi,
                                  base=(-1, 5), ROIs=None, subregion=None):
    """
    Calculates the average TFRs for the TRIAL ONSET condition across subjects,
    handling potential differences in sampling rates and optional subregion selection.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        tfr_dir (str): Directory containing TFR files.
        roi (str): The name of the region of interest.
        base (tuple): Baseline window (tmin, tmax) in seconds.
        ROIs (dict, optional): Mapping of subject -> ROI definitions for subregions.
        subregion (str, optional): Name of subregion to select within each ROI.

    Returns:
        list: A list of lists containing average TFRs for each string filter.
    """
    tfrs = []
    used_subs = []

    for subject in sub_list:
        try:
            fname = f"{tfr_dir}/{subject}/ieeg/trial_onset/{roi}-tfr.h5"
            if os.path.exists(fname):
                used_subs.append(subject)
                tmp_TFR = mne.time_frequency.read_tfrs(fname)
                tmp_TFR.crop(tmin=base[0], tmax=base[1], include_tmax=True)

                # optionally select a subregion
                if subregion is not None:
                    if ROIs is None:
                        raise ValueError("ROIs must be provided when subregion is specified")
                    sub_ROIs = ROIs.copy()[subject]
                    sel_chs, _, _ = get_roi_elec_lists(sub_ROIs, tmp_TFR, subregion)
                    tmp_TFR = tmp_TFR.pick_channels(sel_chs)

                # only rebuild metadata if missing
                if tmp_TFR.metadata is None:
                    trial_onset_epochs = mne.read_epochs(
                        f"{preproc_dir}/{subject}/ieeg/{subject}_bp_clean_pres-locked_ieeg.fif"
                    )
                    good_epochs = [i for i, x in enumerate(
                        trial_onset_epochs.get_annotations_per_epoch()
                    ) if not x]

                    trial_data = pd.read_csv(
                        f"{raw_dir}/{subject}/behave/{subject}_raw_behave.csv"
                    )
                    trial_data['Trial'] = trial_data['Trial'] - 1
                    trial_data['TrialType'] = trial_data.groupby('Trial')['TrialType'] \
                        .transform(lambda x: x.mode().iloc[0])
                    trial_data = trial_data[['Trial', 'TrialType']].drop_duplicates()
                    trial_data = trial_data[trial_data['Trial'] >= 0]
                    trial_data = trial_data[trial_data['Trial'].isin(good_epochs)]

                    if subject in ('BJH021', 'LL10', 'LL13', 'LL19', 'BJH039'):
                        tmp_TFR = tmp_TFR[:-1]

                    tmp_TFR.metadata = trial_data
                    tmp_TFR.save(fname, overwrite=True)

                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline=base, logflag=True)

                tfr_cases = []
                for case in string_filters:
                    sel = tmp_TFR[case]
                    tfr_cases.append(sel.data.mean(axis=0).mean(axis=0))

                tfrs.append(tfr_cases)

        except Exception as e:
            print(f"Failed to load {subject}")
            print(e)
            if subject in used_subs:
                used_subs.remove(subject)

        print(f"currently used subs: {used_subs}")

    # save progress
    suffix = subregion if subregion is not None else roi
    with open(f'../ieeg/trial_onset_average_{suffix}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)

    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] 
                  for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:
        if any('LL' in s for s in used_subs):
            first_ll_sub = [s for s in used_subs if 'LL' in s][0]
            ll_begin = used_subs.index(first_ll_sub)

            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis=0)

            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis=0)

            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:3001]))
            all_subs_average = all_subs_tfrs.mean(axis=0)
            all_subs_averages.append(all_subs_average)
        else:
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis=0)
            all_subs_averages.append(washu_tfrs_mean)

    return all_subs_averages

def calculate_first_move_average(sub_list, string_filters, tfr_dir, roi, ROIs=None, subregion=None):
    """
    Calculates the average TFRs for FIRST MOVE condition across subjects,
    handling potential differences in sampling rates, optional subregion selection,
    and saving progress for efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        tfr_dir (str): Base directory containing TFR files.
        roi (str): The name of the region of interest.
        ROIs (dict, optional): Mapping of subject -> ROI definitions for subregions.
        subregion (str, optional): Name of subregion to select within each ROI.

    Returns:
        list: A list of lists containing average TFRs for each string filter.
    """
    tfrs = []
    used_subs = []

    for subject in sub_list:
        tfr_cases = []
        try:
            # primary location: single file
            fname = f"{tfr_dir}/{subject}/ieeg/first_move/{roi}-tfr.h5"
            if os.path.exists(fname):
                used_subs.append(subject)
                tmp_TFR = mne.time_frequency.read_tfrs(fname)

                # optionally select a subregion
                if subregion is not None:
                    if ROIs is None:
                        raise ValueError("ROIs must be provided when subregion is specified")
                    sub_ROIs = ROIs[subject]
                    sel_chs, _, _ = get_roi_elec_lists(sub_ROIs, tmp_TFR, subregion)
                    tmp_TFR = tmp_TFR.pick_channels(sel_chs)

                # z-score and log-transform
                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline=(-1, 4), logflag=True)

                # apply filters
                for case in string_filters:
                    sel = tmp_TFR[case]
                    tfr_cases.append(sel.data.mean(axis=0).mean(axis=0))
            else:
                # backup location: separate ghost/noghost files
                used_subs.append(subject)
                ghost_fname = f"/home/brooke/pacman/preprocessing/{subject}/ieeg/first_move/ghost-{roi}-tfr.h5"
                noghost_fname = f"/home/brooke/pacman/preprocessing/{subject}/ieeg/first_move/noghost-{roi}-tfr.h5"
                ghost_TFR = mne.time_frequency.read_tfrs(ghost_fname)
                noghost_TFR = mne.time_frequency.read_tfrs(noghost_fname)

                # optionally select subregion
                if subregion is not None:
                    if ROIs is None:
                        raise ValueError("ROIs must be provided when subregion is specified")
                    sub_ROIs = ROIs[subject]
                    sel_chs, _, _ = get_roi_elec_lists(sub_ROIs, ghost_TFR, subregion)
                    ghost_TFR = ghost_TFR.pick_channels(sel_chs)
                    noghost_TFR = noghost_TFR.pick_channels(sel_chs)

                # append pre-computed cases
                tfr_cases.append(ghost_TFR.data.mean(axis=0))
                tfr_cases.append(noghost_TFR.data.mean(axis=0))

            tfrs.append(tfr_cases)

        except Exception as e:
            print(f"Failed to load {subject}")
            print(e)
            if subject in used_subs:
                used_subs.remove(subject)
            continue

        print(f"currently used subs: {used_subs}")

    # save progress
    suffix = subregion if subregion is not None else roi
    with open(f'../ieeg/first_move_average_{suffix}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)

    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))]
                  for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:
        if any('LL' in s for s in used_subs):
            first_ll = [s for s in used_subs if 'LL' in s][0]
            ll_begin = used_subs.index(first_ll)

            # high sampling rate
            washu = np.asarray(tfr_case[:ll_begin]).mean(axis=0)
            ll = np.asarray(tfr_case[ll_begin:]).mean(axis=0)
            combined = np.stack((washu[:, ::2], ll[:, :2501]))
            all_subs_average = combined.mean(axis=0)
            all_subs_averages.append(all_subs_average)
        else:
            all_subs_average = np.asarray(tfr_case).mean(axis=0)
            all_subs_averages.append(all_subs_average)

    return all_subs_averages

    # save progress
    suffix = subregion if subregion is not None else roi
    with open(f'../ieeg/first_move_average_{suffix}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)

    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:
        if any('LL' in s for s in used_subs):
            first_ll = [s for s in used_subs if 'LL' in s][0]
            ll_begin = used_subs.index(first_ll)

            washu = np.asarray(tfr_case[:ll_begin]).mean(axis=0)
            ll = np.asarray(tfr_case[ll_begin:]).mean(axis=0)
            combined = np.stack((washu[:, ::2], ll[:, :2501]))
            all_subs_average = combined.mean(axis=0)
            all_subs_averages.append(all_subs_average)
        else:
            all_subs_average = np.asarray(tfr_case).mean(axis=0)
            all_subs_averages.append(all_subs_average)

    return all_subs_averages


def calculate_first_dot_average(sub_list, string_filters, roi):
    """
    Calculates the average TFRs for the LFIRST DOT condition across subjects,
    handling potential differences in sampling rates and saving progress for
    efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        roi (str): The name of the region of interest.

    Returns:
        list: A list of lists containing average TFRs for each string filter.

    Steps:
        1. Iterates through subjects:
            - Checks for TFR file existence.
            - Loads and preprocesses TFR data (log and zscore).
            - Filters TFR cases based on string_filters.
            - Calculates mean TFRs for each case and appends to a list.
            - Handles exceptions and reports any errors.
        2. Saves intermediate progress to a pickle file.
        3. Invert list structure for easier processing.
        4. Calculates average TFRs for each string filter:
            - Identifies subjects with high or low sampling rates.
            - Calculates separate means for high and low rate TFRs.
            - Combines and averages TFRs from different sampling rates if applicable.
        5. Returns a list of average TFRs for each string filter.
    """    
    tfrs = []
    used_subs = []
    for subject in sub_list:

        try:
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/first_dot/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                
                # load data
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/first_dot/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline = (-1,4), logflag=True)

                tfr_cases = []
                for case in string_filters:            
                    # filter
                    tfr_case = tmp_TFR[case]
                    # append
                    tfr_cases.append(tfr_case.data.mean(axis = 0).mean(axis = 0))

                # get mean and append
                tfrs.append(tfr_cases)

        except Exception as e:
            print(f"Failed to load {subject}")
            print(e)
            used_subs.remove(subject)
            continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/first_dot_average_{roi}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)                
        
    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:

        if any("LL" in subject for subject in sub_list):

            # get indicies of high/low samp rate subs
            first_ll_sub = [subject for subject in used_subs if "LL" in subject][0]
            ll_begin = used_subs.index(first_ll_sub)

            # high sampling rate
            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # Low sampling rate
            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis = 0)

            # combine
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:2501]))
        
            # mean
            all_subs_average = all_subs_tfrs.mean(axis = 0)
            all_subs_averages.append(all_subs_average)
            
        else:
            
            # high sampling rate
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # mean
            all_subs_average = washu_tfrs_mean
            all_subs_averages.append(all_subs_average)    

    return all_subs_averages


def calculate_last_away_average(sub_list, string_filters, roi):
    """
    Calculates the average TFRs for the LAST AWAY condition across subjects,
    handling potential differences in sampling rates and saving progress for
    efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        roi (str): The name of the region of interest.

    Returns:
        list: A list of lists containing average TFRs for each string filter.

    Steps:
        1. Iterates through subjects:
            - Checks for TFR file existence.
            - Loads and preprocesses TFR data (log and zscore).
            - Filters TFR cases based on string_filters.
            - Calculates mean TFRs for each case and appends to a list.
            - Handles exceptions and reports any errors.
        2. Saves intermediate progress to a pickle file.
        3. Invert list structure for easier processing.
        4. Calculates average TFRs for each string filter:
            - Identifies subjects with high or low sampling rates.
            - Calculates separate means for high and low rate TFRs.
            - Combines and averages TFRs from different sampling rates if applicable.
        5. Returns a list of average TFRs for each string filter.
    """
    tfrs = []
    used_subs = []
    for subject in sub_list:

        try:
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/last_away/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                
                # load data
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/last_away/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline = (-2,2), logflag=True)

                tfr_cases = []
                for case in string_filters:            
                    # filter
                    tfr_case = tmp_TFR[case]
                    # append
                    tfr_cases.append(tfr_case.data.mean(axis = 0).mean(axis = 0))

                # get mean and append
                tfrs.append(tfr_cases)

        except Exception as e:
            print(f"Failed to load {subject}")
            print(e)
            used_subs.remove(subject)
            continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/last_away_average_{roi}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)                
        
    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:

        if any("LL" in subject for subject in sub_list):

            # get indicies of high/low samp rate subs
            first_ll_sub = [subject for subject in used_subs if "LL" in subject][0]
            ll_begin = used_subs.index(first_ll_sub)

            # high sampling rate
            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # Low sampling rate
            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis = 0)

            # combine
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:2001]))
        
            # mean
            all_subs_average = all_subs_tfrs.mean(axis = 0)
            all_subs_averages.append(all_subs_average)
            
        else:
            
            # high sampling rate
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # mean
            all_subs_average = washu_tfrs_mean
            all_subs_averages.append(all_subs_average)    

    return all_subs_averages

def calculate_ghost_attack_average(sub_list, tfr_dir, string_filters, roi):
    """
    Calculates the average TFRs for the GHOST ATTACK condition across subjects,
    handling potential differences in sampling rates and saving progress for
    efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        roi (str): The name of the region of interest.

    Returns:
        list: A list of lists containing average TFRs for each string filter.

    Steps:
        1. Iterates through subjects:
            - Checks for TFR file existence.
            - Loads and preprocesses TFR data (log and zscore).
            - Filters TFR cases based on string_filters.
            - Calculates mean TFRs for each case and appends to a list.
            - Handles exceptions and reports any errors.
        2. Saves intermediate progress to a pickle file.
        3. Invert list structure for easier processing.
        4. Calculates average TFRs for each string filter:
            - Identifies subjects with high or low sampling rates.
            - Calculates separate means for high and low rate TFRs.
            - Combines and averages TFRs from different sampling rates if applicable.
        5. Returns a list of average TFRs for each string filter.
    """    
    tfrs = []
    used_subs = []
    for subject in sub_list:

        try:
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5") or os.path.exists(f"{preproc_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                
                # load data
                try:
                    tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5")
                except:
                    tmp_TFR = mne.time_frequency.read_tfrs(f"{preproc_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline = (-1,3), logflag=True)

                tfr_cases = []
                for case in string_filters:            
                    # filter
                    tfr_case = tmp_TFR[case]
                    # append
                    tfr_cases.append(tfr_case.data.mean(axis = 0).mean(axis = 0))

                # get mean and append
                tfrs.append(tfr_cases)

        except Exception as e:
            print(f"Failed to load {subject}")
            print(e)
            used_subs.remove(subject)
            continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/ghost_attack_average_{roi}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)                
        
    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:

        if any("LL" in subject for subject in used_subs):

            # get indicies of high/low samp rate subs
            first_ll_sub = [subject for subject in used_subs if "LL" in subject][0]
            ll_begin = used_subs.index(first_ll_sub)

            # high sampling rate
            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # Low sampling rate
            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis = 0)

            # combine
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:2001]))
        
            # mean
            all_subs_average = all_subs_tfrs.mean(axis = 0)
            all_subs_averages.append(all_subs_average)
            
        else:
            
            # high sampling rate
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # mean
            all_subs_average = washu_tfrs_mean
            all_subs_averages.append(all_subs_average)    

    return all_subs_averages

def calculate_trial_end_average(sub_list, string_filters, roi):
    """
    Calculates the average TFRs for the TRIAL END condition across subjects,
    handling potential differences in sampling rates and saving progress for
    efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        roi (str): The name of the region of interest.

    Returns:
        list: A list of lists containing average TFRs for each string filter.

    Steps:
        1. Iterates through subjects:
            - Checks for TFR file existence.
            - Loads and preprocesses TFR data (log and zscore).
            - Filters TFR cases based on string_filters.
            - Calculates mean TFRs for each case and appends to a list.
            - Handles exceptions and reports any errors.
        2. Saves intermediate progress to a pickle file.
        3. Invert list structure for easier processing.
        4. Calculates average TFRs for each string filter:
            - Identifies subjects with high or low sampling rates.
            - Calculates separate means for high and low rate TFRs.
            - Combines and averages TFRs from different sampling rates if applicable.
        5. Returns a list of average TFRs for each string filter.
    """      
    tfrs = []
    used_subs = []
    for subject in sub_list:

        try:
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/trial_end/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                
                # load data
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/trial_end/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline = (-2.5,2.5), logflag=True)

                tfr_cases = []
                for case in string_filters:            
                    # filter
                    tfr_case = tmp_TFR[case]
                    # append
                    tfr_cases.append(tfr_case.data.mean(axis = 0).mean(axis = 0))

                # get mean and append
                tfrs.append(tfr_cases)

        except Exception as e:
            print(f"Failed to load {subject}")
            print(e)
            used_subs.remove(subject)
            continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/trial_end_average_{roi}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)                
        
    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:

        if any("LL" in subject for subject in sub_list):

            # get indicies of high/low samp rate subs
            first_ll_sub = [subject for subject in used_subs if "LL" in subject][0]
            ll_begin = used_subs.index(first_ll_sub)

            # high sampling rate
            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # Low sampling rate
            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis = 0)

            # combine
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:2501]))
        
            # mean
            all_subs_average = all_subs_tfrs.mean(axis = 0)
            all_subs_averages.append(all_subs_average)
            
        else:
            
            # high sampling rate
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # mean
            all_subs_average = washu_tfrs_mean
            all_subs_averages.append(all_subs_average)    

    return all_subs_averages



def calculate_last_away_average_subregion(sub_list, string_filters, roi, ROIs, subregion_name):
    """
    Calculates the average TFRs for the LAST AWAY condition across subjects,
    handling potential differences in sampling rates and saving progress for
    efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        roi (str): The name of the region of interest.

    Returns:
        list: A list of lists containing average TFRs for each string filter.

    Steps:
        1. Iterates through subjects:
            - Checks for TFR file existence.
            - Loads and preprocesses TFR data (log and zscore).
            - Filters TFR cases based on string_filters.
            - Calculates mean TFRs for each case and appends to a list.
            - Handles exceptions and reports any errors.
        2. Saves intermediate progress to a pickle file.
        3. Invert list structure for easier processing.
        4. Calculates average TFRs for each string filter:
            - Identifies subjects with high or low sampling rates.
            - Calculates separate means for high and low rate TFRs.
            - Combines and averages TFRs from different sampling rates if applicable.
        5. Returns a list of average TFRs for each string filter.
    """
    tfrs = []
    used_subs = []
    for subject in sub_list:

        try:
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/last_away/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                    
                # load data
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/last_away/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline = (-2,2), logflag=True)
                        
                sub_ROIs = ROIs.copy()[subject]
                        
                subroi_list, subroi_names, subroi_indices = get_roi_elec_lists(sub_ROIs, tmp_TFR, subregion_name)
                        
                # create a new tfr with only the mfg channels
                subroi_tfr = tmp_TFR.copy().pick_channels(subroi_list)

                tfr_cases = []
                for case in string_filters:            
                    # filter
                    tfr_case = subroi_tfr[case]
                    # append
                    tfr_cases.append(tfr_case.data.mean(axis = 0).mean(axis = 0))

                # get mean and append
                tfrs.append(tfr_cases)

        except Exception as e:
           print(f"Failed to load {subject}")
           print(e)
           used_subs.remove(subject)
           continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/last_away_average_{subregion_name}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)                
        
    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:

        if any("LL" in subject for subject in sub_list):

            # get indicies of high/low samp rate subs
            first_ll_sub = [subject for subject in used_subs if "LL" in subject][0]
            ll_begin = used_subs.index(first_ll_sub)

            # high sampling rate
            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # Low sampling rate
            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis = 0)

            # combine
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:2001]))

            # mean
            all_subs_average = all_subs_tfrs.mean(axis = 0)
            all_subs_averages.append(all_subs_average)
            
        else:
            
            # high sampling rate
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # mean
            all_subs_average = washu_tfrs_mean
            all_subs_averages.append(all_subs_average)    

    return all_subs_averages

def calculate_subregion_ghost_attack_average(sub_list, string_filters, roi, subregion_name, ROIs = ROIs):
    """
    Calculates the average TFRs for the GHOST ATTACK condition across subjects,
    handling potential differences in sampling rates and saving progress for
    efficiency.

    Args:
        sub_list (list): A list of subject IDs to process.
        string_filters (list): A list of strings to filter TFR cases by.
        roi (str): The name of the region of interest.

    Returns:
        list: A list of lists containing average TFRs for each string filter.

    Steps:
        1. Iterates through subjects:
            - Checks for TFR file existence.
            - Loads and preprocesses TFR data (log and zscore).
            - Filters TFR cases based on string_filters.
            - Calculates mean TFRs for each case and appends to a list.
            - Handles exceptions and reports any errors.
        2. Saves intermediate progress to a pickle file.
        3. Invert list structure for easier processing.
        4. Calculates average TFRs for each string filter:
            - Identifies subjects with high or low sampling rates.
            - Calculates separate means for high and low rate TFRs.
            - Combines and averages TFRs from different sampling rates if applicable.
        5. Returns a list of average TFRs for each string filter.
    """    
    tfrs = []
    used_subs = []
    for subject in sub_list:

        # try:
        if os.path.exists(f"{tfr_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5") or os.path.exists(f"{preproc_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5"):
            # load data
            used_subs.append(subject)
            
            # load data
            try:
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5")
            except:
                tmp_TFR = mne.time_frequency.read_tfrs(f"{preproc_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5")

            # zscore and log
            tmp_TFR = pf.log_and_zscore_TFR(tmp_TFR, baseline = (-1,3), logflag=True)

            ## MONICA TODO
            # need to calculate mfg_tfr and replace tmp_TFR with mfg_tfr
            sub_ROIs = ROIs.copy()[subject]

            subroi_list, subroi_names, subroi_indices = get_roi_elec_lists(sub_ROIs, tmp_TFR, subregion_name)
            
            # create a new tfr with only the mfg channels
            subroi_tfr = tmp_TFR.copy().pick_channels(subroi_list)
            
            tfr_cases = []
            for case in string_filters:            
                # filter
                tfr_case = subroi_tfr[case]
                # append
                tfr_cases.append(tfr_case.data.mean(axis = 0).mean(axis = 0))

            # get mean and append
            tfrs.append(tfr_cases)

        # except Exception as e:
        #     print(f"Failed to load {subject}")
        #     print(e)
        #     used_subs.remove(subject)
        #     continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/ghost_attack_average_{subregion_name}.pkl', 'wb') as f:
        pickle.dump(tfrs, f)                
        
    # invert list so the outer list is the string filter
    tfrs_cases = [[tfrs[j][i] for j in range(len(tfrs))] for i in range(len(tfrs[0]))]

    all_subs_averages = []
    for tfr_case in tfrs_cases:

        if any("LL" in subject for subject in used_subs):

            # get indicies of high/low samp rate subs
            first_ll_sub = [subject for subject in used_subs if "LL" in subject][0]
            ll_begin = used_subs.index(first_ll_sub)

            # high sampling rate
            washu_tfrs = np.asarray(tfr_case[0:ll_begin])
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # Low sampling rate
            ll_tfrs = np.asarray(tfr_case[ll_begin:])
            ll_tfrs_mean = ll_tfrs.mean(axis = 0)

            # combine
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:2001]))
        
            # mean
            all_subs_average = all_subs_tfrs.mean(axis = 0)
            all_subs_averages.append(all_subs_average)
            
        else:
            
            # high sampling rate
            washu_tfrs = np.asarray(tfr_case)
            washu_tfrs_mean = washu_tfrs.mean(axis = 0)

            # mean
            all_subs_average = washu_tfrs_mean
            all_subs_averages.append(all_subs_average)    

    return all_subs_averages




def plot_allsub_averages(array_average, title, fname, min_time, max_time):
    """
    Generates and saves a time-frequency plot of the average TFR across all subjects
    with customizable visual properties.

    Args:
        array_average (np.ndarray): The 2D array containing average TFR values.
        title (str): The title to display on the plot.
        fname (str): The filename to save the plot as.
        min_time (float): The minimum time value to display on the x-axis.
        max_time (float): The maximum time value to display on the x-axis.

    Returns:
        None

    Creates a time-frequency plot using matplotlib with the following customizations:
        - Large figure size and font size for clarity.
        - Times New Roman font for a serif appearance.
        - Logarithmic frequency axis and custom tick labels.
        - Decimated y-axis ticks for improved readability.
        - 'RdBu_r' colormap for diverging color representation.
        - Black dashed vertical line at time zero.
        - Colorbar for displaying value ranges.
        - High-resolution image saving (dpi=400).
    """

    plt.rcParams['figure.figsize'] = [6, 4.8]
    plt.rcParams.update({'font.size': 14})
    matplotlib.rcParams['font.serif'] = 'Gill Sans'
    matplotlib.rcParams['font.family'] = 'serif'

    freqs = np.logspace(start = np.log10(1), stop = np.log10(150), num = 80, base = 10, endpoint = True)
    yticks = np.linspace(np.min(freqs),np.max(freqs),len(freqs))
    yticks_labels = np.round(freqs, 1)
    
    # decimate y for viz
    yticks = yticks[::2]
    yticks_labels = yticks_labels[::2]

    fig, ax = plt.subplots()
    i = ax.imshow(array_average, cmap = 'RdBu_r', interpolation="none", origin="lower", aspect = 'auto', extent=[min_time, max_time, freqs[0], freqs[-1]], vmin = -.8, vmax = .8)
    i2 = plt.axvline(x=0, color='#2D2327', linestyle='-')
    ax.set_yticks(yticks[::2])
    ax.set_yticklabels(yticks_labels[::2])
    ax.tick_params(axis='x', which='major', width = 1, length = 2, pad=2)  # Increase padding between x-ticks and x-axis
    ax.tick_params(axis='y', which='major', width = 1, length = 2, pad=2)  # Increase padding between y-ticks and y-axis

    bar = plt.colorbar(i)
    ax.set_title(title, fontsize=10, fontweight = "bold", pad=7)
    fig.savefig(fname, dpi=400)