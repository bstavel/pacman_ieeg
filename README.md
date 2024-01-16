# Pacman iEEG Analyses


This repo is used to analyze the intracranial EEG data for the Pacman task. This includes data cleaning, rereferencing, visualization of the signals, and prep for joining with the task behavior. Mostly written in python utilizing MNE.

### Folder Notes

* `raw_data` has scripts for data cleaning as well as notes about the sub-specific cleaning
* `preprocessing` has the subject-specific scripts for iEEG analysis
* `issues_decisions` have markdown files with reminders of issues and decision-points


## Current To-Do

Updated 1/12/2024. As the story is coming together for the pacman data, I am documenting here the next big steps to get this finished, both in terms of what it will take to understand this system (or as much of it as I can in a single phd project) as well as get it ready for publication. I am setting a goal of getting this written and on bioarxiv by end of May 2024.

1. **Rerun Visualizations for Linear Mixed Effects Models**
    * Final versions of these plots  for SFN looked really nice and clear-- would like to run these for the other regions, especially at turnaround. The significance for some of the turnaround plots looked suspicious to me and it might be easier to interpret with the new versions.
    * If the differences hold it would be good to find another way to validate those findings. Might be helpful to visualize trial by trial theta when I lock to turnaround-- why is it so much messier looking that onset? Could visualize the regressors right before turnaround too
    * Extend the interaction model to all regions/time points
    * Timelock to the first dot and rerun
<s>
   <b>2. Recalculate HFA</b>
    <ul>
        <li>I was given advice once that it is better not to notch filter before running the morlet wavelet computation. I think I must have misunderstood, but that has been nagging at me for awhile. I need to change this to get an accurate measure of HFA.</li>
        <li>After this, the priority is figuring out what lPFC HFA is tracking in the task. This might mean having to re timelock to ghost chase initiation. I could also maybe include that in my code refactor (see 4).</li>
    </ul>
    <b>3. Add SFG</b>
    <ul>
        <li>split SFG/MFG and dACC/sgACC</li>
    </ul>
    <b>4. Code Refactor</b>
    <ul>
        <li>Before running the next 18 subjects, I want to create a function sheet with my main functions for morlets and especially ROIs. It is bad practice to have those functions the same but repeating themselves across the subject-specific notebooks.</li>
        <li>Also, I am gonna have to ask for soooo much more space on the cluster, but am gonna try not to feel bad about that. Will try to talk to Bob about it beforehand this time. 😬</li>
    </ul>
    <b>5. Clean the other 18 (!!!!) datasets</b>
    <ul>
        <li>Clean WashU datasets
            <ul>
                <li>Figure out what is up with BJH024</li>
            </ul>
        </li>
        <li>Write scripts to read in Irvine data</li>
        <li>Get final region counts and make sure that we are actually for real for real good to stop recording</li>
        <li>See if we have enough electrode counts to split sgACC from dACC, lOFC and mOFC, and antHC with postHC.</li>
    </ul>
</s>

6. **Directed Connectivity - Limbic**
    * *Limbic Connectivity* We have pretty strong evidence that OFC/HC are communicating via theta at trial onset, so I think we should start here. Using the electrode pairs identified in the earlier connectivity analysis, I want to get at the following
        - Going to use coherence to match the rodent literature. Start with limbic regions, particularly during approach, see if it breaks down at turn around.
7. **Directed Connectivity - lPFC**
    * It seems like when lPFC HFA turns on, the limbic theta drops. Need to try to capture this either just by showing that HFA increases predict theta descreases or that HFA increases predicts when coherence in the limbic circuit shuts down.
8. **Look at posterior/anterior hippocampal differences**
9. **Phase/amplitude coupling**
    * Hypothesize that hippocampal theta will have sig PAC with OFC/Cingulate HFA.
10. **Integrate with Survival Models**
    * See if the OFC-HC coherence or lPFC HFA predicts turnaround in the survival models
