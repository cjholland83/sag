#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:08:35 2019

@author: chrisholland
"""
import numpy as np
import pandas as pd

########### USER INPUT ########################################################

buy_in = 5 # payout and ev will be in same units (dollars or cents)
rake_pct = 8.5 # use pct rather than decimal
base = 10000000 # used to divide the set probabilities and prevent user error for high multipliers
set_probabilities = np.array([300, 6000, 10000, 50000, 900000]) # chance out of base do not include level 1 and 2
set_multipliers = np.array([200, 100, 25, 10, 6, 4, 2]) # include all multipliers including level 1 and 2
for_effective_rake = 1/1000 # set probability for an experince very few player will have

###############################################################################

########### CALCULATIONS ######################################################

# get the level 1 and 2 payouts needed for the calculation
level_1 = set_multipliers[-1] * buy_in
level_2 = set_multipliers[-2] * buy_in

# calculate the total ev of the game in units of the base: (1-rake)*buy_in * players
total_ev = 3 * buy_in * (100 - rake_pct)/100 * base

# calculate the ev of each level in units of the base excluding level 1 and 2 which still need to be solved
set_ev_array = set_probabilities * set_multipliers[:-2] * buy_in

# calculate the ev remaining to be distributed amongst levels 1 and 2
remaining_ev = total_ev - np.sum(set_ev_array)

# calculate the probability remaining to be distributed amongst levels 1 and 2
remaining_prob = base - np.sum(set_probabilities)

# calculate the level 2 probability (solving simultaneous equations)
level_2_prob = (remaining_ev - level_1 * remaining_prob) / (level_2 - level_1)

# the level 1 probability is 1 - all other probability
level_1_prob = base - level_2_prob - np.sum(set_probabilities)

# append the calculated probabilities to the set probability array
calculated_probs = np.append(level_2_prob,level_1_prob)
all_probabilities = np.append(set_probabilities, calculated_probs)

# construct a dictionary with the payout in units specified in the input and fractional probabilities
d = {'payout':set_multipliers*buy_in, 'probability':all_probabilities/base}

# create a DataFrame from the dict
df = pd.DataFrame(data=d)

# calculate the ev and ev percentage for each level
df['ev']= df.payout * df.probability
df['ev_pct'] = df.ev / sum(df.ev)

# calculate the percentage of ev going to the jackpot as defined by the user in order to give the effective rake
jackpot_pct = np.sum(df.ev_pct[df.probability <= for_effective_rake])
effective_rake = rake_pct + jackpot_pct*100

# output the paytable and the effective rake
print(df)
print('\nThe buy-in is {0:.0f}, the total EV is {1:.2f}'.format(buy_in, total_ev/base))
print('The rake is {0:.2f}% with the effective rake at {1:.2f}%'.format(rake_pct, effective_rake))

###############################################################################
