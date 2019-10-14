# EliminatorChallenge
The NFL eliminator challenge is a contest in which you choose a team each week to win their game. You can't choose the same team more than once. If the team that you chose for a given week loses, then you are eliminated. The last person standing wins!

### Elo Scores and Win Probabilities

This program first takes the current elo scores of NFL teams (https://projects.fivethirtyeight.com/2019-nfl-predictions/) and given the schedule of the entire season, calculates the win probability of each game for each team using the elo win probability formula:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/51346e1c65f857c0025647173ae48ddac904adcb)

### Integer Programming Solver

Next, it feeds this into an integer programming solver with the following constrains:

Maximize - total win probability

Subject to - must choose one team each week, any team can only be picked once per season

### Week Weights

I played around with adding weights to certain weeks. You don't need to be correct every single week, you just need to outlast everyone else (i.e. a correct pick week 1 is worth much more than a correct pick week 16). 

#### Exponential Weighting

I first added exponential weights to the weeks given the following formula: .9^(Week-1)

I then used the metric of 'points' to now optimize, where points are just win probability multiplied by the weight for that week.

#### Equal Weights for first 8-10 Weeks

Past contests with a similar number of entrants showed that you need about 8-10 weeks correct to win, so for the final output I considered only the first 10 weeks of the season and weighted each week equally. 

### Output

Here is what the output looks like!

![alt text](https://github.com/kweithers/EliminatorChallenge/blob/master/Output.png)