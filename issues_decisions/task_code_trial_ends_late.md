## Task code issue with trial ends lagging

When analyzing the first bci2000 patient, I noticed that there were a handful of trials (n=5, trials = [101, 90, 80, 65, 15]) that were no ghost trials where the trial ended on the opposite side of the cooridor from the exit. The game was designed to not allow this behavior and it looks like the pacman does get stuck there for some amount of time (2-5s) before the trial ends. 

I intended for that not be an exit under any circumstance, but maybe it is is better that the game will eventually them through rather than the player thinking the game froze? As for the mechanism, I believe it is from the slight rounding in location that happens with every frame flip, so eventually they are able to skip ahead past 178 to the exit or something like that (back from when the code allowed you to circle around to the side, rather than end the trial). It is rare, so I am not sure I should change it at this point? Current plan is to look out for this behavior on the next two subjects and determine if I need to reach out about it.

Here are some examples of trials with this behavior:

![Example](/home/brooke/Pictures/Screenshots/Screenshot_from_2022-05-06_17-00-42.png)