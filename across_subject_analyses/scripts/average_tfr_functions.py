def calculate_trial_onset_average(sub_list, string_filters, roi, base = (-1,5)):
    """
    Calculates the average TFRs for the TRIAL ONSET condition across subjects,
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
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/trial_onset/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/trial_onset/{roi}-tfr.h5")
                tmp_TFR = tmp_TFR[0]
                # check if metadata exists
                if tmp_TFR.metadata is None:

                    # load old pres data to help add metadata
                    trial_onset_epochs = mne.read_epochs(f"{preproc_dir}/{subject}/ieeg/{subject}_bp_clean_pres-locked_ieeg.fif")

                    # get good epochs (for behavioral data only)
                    good_epochs = [i for i,x in enumerate(trial_onset_epochs.get_annotations_per_epoch()) if not x]

                    # Create trial metadata 
                    trial_data = pd.read_csv(f"{raw_dir}/{subject}/behave/{subject}_raw_behave.csv")
                    trial_data['Trial'] = trial_data['Trial'] - 1
                    trial_data['TrialType'] = trial_data.groupby('Trial')['TrialType'].transform(lambda x: x.mode().iloc[0])
                    trial_data = trial_data[['Trial', 'TrialType']].drop_duplicates()
                    trial_data = trial_data[trial_data['Trial'] >=0]
                    trial_data = trial_data[trial_data['Trial'].isin(good_epochs)]

                    # last trial is fake for BJH021
                    if subject == 'BJH021' or subject == 'LL10' or subject == "LL13" or subject == "LL19" or subject == "BJH039":
                        tmp_TFR = tmp_TFR[0:-1]

                    # set metadata to TFR
                    tmp_TFR.metadata = trial_data
                    
                    # save
                    tmp_TFR.save(f"{tfr_dir}/{subject}/ieeg/trial_onset/{roi}-tfr.h5", overwrite = True)
                
                # log and zscore
                tmp_TFR = log_and_zscore_TFR(tmp_TFR, baseline = base, logflag=True)
                    
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
            # continue

        print(f"currently used subs: {used_subs}")

    # save progress cuz it is so long to load these dang things       
    with open(f'../ieeg/trial_onset_average_{roi}.pkl', 'wb') as f:
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
            all_subs_tfrs = np.stack((washu_tfrs_mean[:, ::2], ll_tfrs_mean[:, 0:3001]))
        
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

def calculate_first_move_average(sub_list, string_filters, roi):
    """
    Calculates the average TFRs for FIRST MOVE condition across subjects,
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
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/first_move/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                
                # load data
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/first_move/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = log_and_zscore_TFR(tmp_TFR[0], baseline = (-1,4), logflag=True)

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
    with open(f'../ieeg/first_move_average_{roi}.pkl', 'wb') as f:
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
                tmp_TFR = log_and_zscore_TFR(tmp_TFR[0], baseline = (-1,4), logflag=True)

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
                tmp_TFR = log_and_zscore_TFR(tmp_TFR[0], baseline = (-2,2), logflag=True)

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

def calculate_ghost_attack_average(sub_list, string_filters, roi):
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
            if os.path.exists(f"{tfr_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5"):
                # load data
                used_subs.append(subject)
                
                # load data
                tmp_TFR = mne.time_frequency.read_tfrs(f"{tfr_dir}/{subject}/ieeg/ghost_attack/{roi}-tfr.h5")

                # zscore and log
                tmp_TFR = log_and_zscore_TFR(tmp_TFR[0], baseline = (-1,3), logflag=True)

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
                tmp_TFR = log_and_zscore_TFR(tmp_TFR[0], baseline = (-2.5,2.5), logflag=True)

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

    plt.rcParams['figure.figsize'] = [45, 35]
    plt.rcParams.update({'font.size': 60})
    matplotlib.rcParams['font.serif'] = 'Times New Roman'
    matplotlib.rcParams['font.family'] = 'serif'

    freqs = np.logspace(start = np.log10(1), stop = np.log10(150), num = 80, base = 10, endpoint = True)
    yticks = np.linspace(np.min(freqs),np.max(freqs),len(freqs))
    yticks_labels = np.round(freqs, 1)
    
    # decimate y for viz
    yticks = yticks[::2]
    yticks_labels = yticks_labels[::2]

    fig, ax = plt.subplots()
    i = ax.imshow(array_average, cmap = 'RdBu_r', interpolation="none", origin="lower", aspect = 'auto', extent=[min_time, max_time, freqs[0], freqs[-1]], vmin = -1, vmax = 1)
    i2 = plt.axvline(x=0, color='black', linestyle='--')
    ax.set_yticks(yticks[::2])
    ax.set_yticklabels(yticks_labels[::2])
    bar = plt.colorbar(i)
    ax.set_title(title, fontsize=65, fontweight = "bold", pad=40)
    fig.savefig(fname, dpi=400)