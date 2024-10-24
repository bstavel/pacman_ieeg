# Preprocessing

## Cleaning

Using MNE to handle and document the cleaning process, see cleaning section for specifics


## Bipolar Rereferencing

Pretty self explanatory.

## Extracting Power

I decided to use Morlet wavelets to calculate the time-frequency representation for each time period of interest from 1-150Hz, using the function mne.time_frequency.tfr_morlet. This will be the basis for all of power calcualtions, which means, for example, I will take the 3-8hz frequencies from the TFR and average them to gether to get Theta power, etc. The TFRs on example electrodes have been cleared by Ludo. I am using a log-spaced freqs vector, as well as a log-spaced vector for the number of cycles for each frequency band. Specifically,

```
# Defintion of Frequencies and Number of Cycles
freqs = np.logspace(start = np.log10(1), stop = np.log10(150), num = 80, base = 10, endpoint = True)
n_cycles = np.logspace(np.log10(2), np.log10(30), base = 10, num = 80)

# formulas to check bandwidth and time bin
band_width = (freqs / n_cycles) * 2
time_bin = n_cycles / freqs / np.pi

```

These print out:


*Frequencies*
```
[  1.           1.06548039   1.13524845   1.20958496   1.28878905
   1.37317945   1.46309577   1.55889984   1.6609772    1.76973863
   1.8856218    2.00909304   2.14064922   2.28081976   2.43016872
   2.5892971    2.75884527   2.93949552   3.13197482   3.33705774
   3.55556956   3.78838962   4.03645484   4.30076345   4.5823791
   4.88243505   5.20213877   5.54277682   5.90571998   6.2924288
   6.70445946   7.14347005   7.61122722   8.10961331   8.64063391
   9.20642595   9.80926626  10.45158079  11.13595433  11.8651409
  12.6420749   13.46988283  14.35189595  15.29166362  16.29296764
  17.35983743  18.49656627  19.70772855  20.99819821  22.37316831
  23.83817199  25.39910467  27.06224782  28.83429423  30.72237491
  32.73408785  34.87752853  37.16132253  39.59466023  42.18733383
  44.94977669  47.89310538  51.02916436  54.37057369  57.93077979
  61.72410955  65.76582801  70.07219975  74.66055437  79.54935622
  84.75827869  90.30828341  96.22170458 102.52233885 109.23554107
 116.38832636 124.00947878 132.1296672  140.78156868 150.        ]
 
 ```
 *Number of Cycles (also called width or order)*
 ```
[ 2.          2.06974683  2.14192598  2.21662225  2.29392345  2.37392039
  2.45670711  2.54238088  2.63104239  2.72279582  2.81774902  2.91601355
  3.01770491  3.12294259  3.23185027  3.34455593  3.46119202  3.58189561
  3.70680855  3.83607763  3.96985476  4.10829716  4.25156752  4.3998342
  4.55327146  4.71205959  4.87638521  5.04644142  5.22242807  5.40455198
  5.59302718  5.78807514  5.9899251   6.19881425  6.41498808  6.63870064
  6.87021481  7.10980267  7.35774578  7.61433552  7.87987341  8.15467152
  8.43905278  8.73335138  9.03791318  9.3530961   9.67927051 10.01681975
 10.36614047 10.72764321 11.10175278 11.48890883 11.88956634 12.30419614
 12.73328549 13.17733866 13.63687749 14.112442   14.60459107 15.11390305
 15.64097649 16.18643078 16.75090693 17.33506828 17.93960134 18.56521653
 19.21264906 19.88265978 20.57603606 21.29359274 22.03617307 22.80464971
 23.59992576 24.42293581 25.27464702 26.15606032 27.06821151 28.01217252
 28.98905269 30.        ]
 ```
 
 *Time bin*
 ```
[0.63661977 0.61833225 0.60057005 0.58331808 0.5665617  0.55028666
 0.53447913 0.5191257  0.5042133  0.48972928 0.47566133 0.46199749
 0.44872616 0.43583606 0.42331624 0.41115607 0.39934521 0.38787363
 0.37673158 0.36590959 0.35539848 0.34518931 0.33527341 0.32564235
 0.31628796 0.30720227 0.29837759 0.2898064  0.28148143 0.2733956
 0.26554204 0.25791408 0.25050525 0.24330924 0.23631994 0.22953142
 0.22293791 0.2165338  0.21031365 0.20427219 0.19840427 0.19270491
 0.18716927 0.18179265 0.17657048 0.17149832 0.16657186 0.16178692
 0.15713943 0.15262545 0.14824113 0.14398276 0.13984672 0.13582948
 0.13192765 0.1281379  0.12445701 0.12088186 0.11740941 0.11403671
 0.11076089 0.10757918 0.10448886 0.10148732 0.09857199 0.09574042
 0.09299018 0.09031895 0.08772445 0.08520447 0.08275689 0.08037962
 0.07807064 0.07582798 0.07364975 0.07153409 0.0694792  0.06748334
 0.06554482 0.06366198]
 ```
 *Bandwidth*
 ```
[ 1.          1.02957557  1.06002585  1.09137671  1.1236548   1.15688753
  1.19110313  1.22633068  1.26260011  1.29994222  1.33838875  1.37797236
  1.41872667  1.46068632  1.50388695  1.54836526  1.59415904  1.6413072
  1.68984979  1.73982805  1.79128445  1.84426271  1.89880782  1.95496614
  2.01278538  2.07231465  2.13360453  2.19670709  2.26167595  2.3285663
  2.39743497  2.46834047  2.54134304  2.6165047   2.69388931  2.77356261
  2.8555923   2.94004806  3.02700165  3.11652694  3.2087      3.30359912
  3.40130494  3.50190046  3.60547115  3.71210501  3.82189262  3.93492726
  4.05130497  4.17112461  4.29448799  4.42149991  4.55226828  4.68690419
  4.82552204  4.96823959  5.1151781   5.26646239  5.42222101  5.58258627
  5.74769442  5.91768575  6.09270466  6.27289986  6.45842443  6.649436
  6.84609684  7.04857404  7.25703961  7.47167068  7.69264957  7.92016405
  8.1544074   8.39557862  8.64388262  8.89953035  9.16273901  9.43373222
  9.7127402  10.        ]
```

## Baselining

For baselining, I am currently log-transforming the TFR, and then z-scoring within each trial, channel, and frequnecy band.

## Individual Subject Time-locking Analyses

I then calculate the TFRs based on 4 different events: `last_away`, `first_dot`, `trial_onset`, `trial_end`. These scripts generally follow the same format, but I seperate some of the TFRs based on different conditions as is relevant to the specific event. 

### Freq Power Csvs

Along with calculating the TFR I also average frequency power within the given frequency bands and save out to cvs. Here is the information relevant frequency-specific information.


|  Freq | Lower  | Upper  | Step  |  Subband |  Subband Info |
|-------|--------|--------|-------|----------|---------------|
|  Delta | 1     |  3     |  np.floor(sfreq/(2*4)) |    No     |  ~ |
|  Theta |  3    |  8     |  np.floor(sfreq/(5*4)) |    No     |  ~ |
|  Alpha  | 8    | 13     |  np.floor(sfreq/(11*4)) |    No     |  ~ |
|  Beta | 13     | 30     |  np.floor(sfreq/(22*4)) |    No     |  ~ |
| Gamma  | 30    | 70     |  np.floor(sfreq/(50*4)) |    yes     |  (30, 40), (35, 45), (40, 50), (45, 55), (50, 60), (55, 65), (60, 70) |
| HFA  |  70     | 150    |  np.floor(sfreq/(110*4)) |    yes     | (70, 90), (80, 100), (90, 110), (100, 120), (110, 130), (120, 140), (130, 150) |


The step is with what frequency I save out the power information to a csv. Higher frequency for higher bands. I chose 4 samples per oscillation, and picked a middle frequency within the band to determine the frequency. I did this because it seemed reasonable, I wasn't copying from any example.

### Event tables

I use R to create tables of events that I use to create the MNE epoch objects. The scripts live here: https://github.com/bstavel/pacman_behavior/blob/main/R/create_timelock_event_tables.R
Here are some small but tricky points

* When merging the tables as metadata in the timelocking scripts, merge the metadata in before you remove bad epochs. This means that I do not filter out bad trials in the R scripts, as I was doing originally. 
* Also, in the R scripts we will save the events with the `neural_trial_numeric` variable so it already aligns with python 0 indexing, cuz it is confusing to change it other same variable/know if I already changed it before.

