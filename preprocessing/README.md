# Preprocessing

## Cleaning

Using MNE to handle and document the cleaning process, see cleaning section for specifics

## Filtering

I still need to separate out filtering for data cleaning and filtering for the rest of the analysis.

I have decided to use welches method for filtering for my analysis of theta in the hippocampus, since I am using FOOF and it seems to be what the Voyteck lab uses. Need to read up on why that may be a bad choice for any reason, but it seems reasonable.

## Bipolar Rereferencing

## Baselining

* Theta 

I have ~1 second ITI, so I need to decide how much of that I will use to baseline and if it makes sense to baseline using the ITI. Will decide this by looking at the raw signal and visualizing electrodes to see if there are peaks in theta before the trial onset.
