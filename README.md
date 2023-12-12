# Pacman iEEG Analyses


This repo is used to analyze the intracranial EEG data for the Pacman task. This includes data cleaning, rereferencing, visualization of the signals, and prep for joining with the task behavior. Mostly written in python utilizing MNE.

### Folder Notes

* `raw_data` has scripts for data cleaning as well as notes about the sub-specific cleaning
* `preprocessing` has the subject-specific scripts for iEEG analysis
* `issues_decisions` have markdown files with reminders of issues and decision-points


## Current To-Do

Written post SFN 2023. As the story is coming together for the pacman data, I am documenting here the next big steps to get this finished, both in terms of what it will take to understand this system (or as much of it as I can in a single phd project) as well as get it ready for publication. I am setting a goal of getting this written and on bioarxiv by end of May 2024.

1. **Rerun Visualizations for Linear Mixed Effects Models**
    * Final versions of these plots  for SFN looked really nice and clear-- would like to run these for the other regions, especially at turnaround. The significance for some of the turnaround plots looked suspicious to me and it might be easier to interpret with the new versions.
    * If the differences hold it would be good to find another way to validate those findings. Might be helpful to visualize trial by trial theta when I lock to turnaround-- why is it so much messier looking that onset? Could visualize the regressors right before turnaround too
    * Extend the interaction model to all regions/time points
    * Timelock to the first dot and rerun
2. **Recalculate HFA**
    * I was given advice once that it is better not to notch filter before running the morlet wavelet computation. I think I must have misunderstood, but that has been nagging at me for awhile. I need to change this to get an accurate measure of HFA.
    * After this, the priority is figuring out what lPFC HFA is tracking in the task. This might mean having to re timelock to ghost chase initiation. I could also maybe include that in my code refactor (see 4).
3. **Add SFG??**
    * Super torn about this, because adding more heterogeneity seems to be going in the opposite direction... Might hold off on this for the next year?
4. **Code Refactor**
    * Before running the next 18 subjects, I want to create a function sheet with my main functions for morlets and especially ROIs. It is bad practice to have those functions the same but repeating themselves across the subject-specific notebooks.
    * Also, I am gonna have to ask for soooo much more space on the cluster, but am gonna try not to feel bad about that. Will try to talk to Bob about it beforehand this time. 😬
5. **Clean the other 18 (!!!!) datasets**
    * Clean WashU datasets
        - Figure out what is up with BJH024
    * Write scripts to read in Irvine data
    * Get final region counts and make sure that we are actually for real for real good to stop recording
    * See if we have enough electrode counts to split sgACC from dACC, lOFC and mOFC, and antHC with postHC.
6. **Directed Connectivity - Limbic**
    * *OFC/HC Connectivity* We have pretty strong evidence that OFC/HC are communicating via theta at trial onset, so I think we should start here. Using the electrode pairs identified in the earlier connectivity analysis, I want to get at the following
        - Phase-informed connectivity. I am going to be asked for multiple measures of connectivity, so I might as well get a basic understanding now of the phase information.
        - Directed connectivity. I still don't understand which is the best measure to use. Phase-locking values feel like the ones I have seen the most. But this will take more thought. I probably need like a week "retreat" to get these off the ground and running.
7. **Directed Connectivity - lPFC**
    * This is more tricky. I hypothesize that the lPFC is interacting with the limbic theta network, but I don't know by what frequency band or by what region. Bob thinks (and I agree) that this is the step that could take this project to the next level.
    * Is the first step to really figure out what lPFC HFA is encoding? It seems like it has to do with threat, because we just do not see those signals in the no ghost trials. 
    * We can look for theta connectivity
    * Ask Bob/lab for help with this.
8. **Look at posterior/anterior hippocampal differences**
9. **Phase/amplitude coupling**
    * Truly no way we get to this until early next year. Could really help piece together the connectivity and local results though. Will need to think about this way more. TODO.
