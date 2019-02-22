#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:59:07 2019

@author: chrisholland
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import dc_stat_think as dcst

standard_multipliers = np.array([12000,240,120,25,10,6,4,2])

# buy in $0.25 to $3 stats
group_1_probabilities = np.array([1,30,75,1000,5000,75000,184506,734388])

buyin_025 = 0.25
spins_025 = 100000

buyin_1 = 1.0
spins_1 = 10

buyin_3 = 3.0
spins_3 = 80000

# buy in $7
group_2_probabilities = np.array([1,30,75,1000,5000,75000,199506,719388])

buyin_7 = 7
spins_7 = 70000

# buy in $15 and $30
group_3_probabilities = np.array([1,30,75,1000,5000,75000,214506,704388])

buyin_15 = 15
spins_15 = 60000

buyin_30 = 30
spins_30 = 50000

# buy in $60 and $100
group_4_probabilities = np.array([1,30,75,1000,5000,75000,229506,689388])

buyin_60 = 60
spins_60 = 40000

buyin_100 = 100
spins_100 = 30000

# buy in $500
group_5_probabilities = np.array([1,30,75,1000,5000,75000,234306,684588])

buyin_500 = 500
spins_500 = 20000

# buy in $1000
group_6_probabilities = np.array([1,30,75,1000,5000,75000,234906,683988])

buyin_1000 = 1000
spins_1000 = 10000

base = 1000000.0
months = 100


calculated_probs_g1 = group_1_probabilities / base
calculated_probs_g2 = group_2_probabilities / base
calculated_probs_g3 = group_3_probabilities / base
calculated_probs_g4 = group_4_probabilities / base
calculated_probs_g5 = group_5_probabilities / base
calculated_probs_g6 = group_6_probabilities / base

def calc_monthly_theo_rake(buyin, multipliers, calculated_probs, spins):
    payouts = buyin * multipliers
    rake = 3 * buyin - np.dot(payouts, calculated_probs)
    monthly_theo_rake = rake * spins
    return payouts, monthly_theo_rake

payouts_025, monthly_theo_rake_025 = calc_monthly_theo_rake(buyin_025,standard_multipliers,calculated_probs_g1,spins_025)
payouts_1, monthly_theo_rake_1 = calc_monthly_theo_rake(buyin_1,standard_multipliers,calculated_probs_g1,spins_1)
payouts_3, monthly_theo_rake_3 = calc_monthly_theo_rake(buyin_3,standard_multipliers,calculated_probs_g1,spins_3)
payouts_7, monthly_theo_rake_7 = calc_monthly_theo_rake(buyin_7,standard_multipliers,calculated_probs_g2,spins_7)
payouts_15, monthly_theo_rake_15 = calc_monthly_theo_rake(buyin_15,standard_multipliers,calculated_probs_g3,spins_15)
payouts_30, monthly_theo_rake_30 = calc_monthly_theo_rake(buyin_30,standard_multipliers,calculated_probs_g3,spins_30)
payouts_60, monthly_theo_rake_60 = calc_monthly_theo_rake(buyin_60,standard_multipliers,calculated_probs_g4,spins_60)
payouts_100, monthly_theo_rake_100 = calc_monthly_theo_rake(buyin_100,standard_multipliers,calculated_probs_g4,spins_100)
payouts_500, monthly_theo_rake_500 = calc_monthly_theo_rake(buyin_500,standard_multipliers,calculated_probs_g5,spins_500)
payouts_1000, monthly_theo_rake_1000 = calc_monthly_theo_rake(buyin_1000,standard_multipliers,calculated_probs_g6,spins_1000)

monthly_theoretical_revenue = np.sum([monthly_theo_rake_025, monthly_theo_rake_1, monthly_theo_rake_3,
                                      monthly_theo_rake_7, monthly_theo_rake_15, monthly_theo_rake_30,
                                      monthly_theo_rake_60, monthly_theo_rake_100, monthly_theo_rake_500,
                                      monthly_theo_rake_1000]) / 1000

monthly_revenue = []

for i in range(months):
    generated_payouts_025 = np.random.choice(payouts_025, size=spins_025, p=calculated_probs_g1)
    generate_revenue_025 = 3 * buyin_025 - generated_payouts_025

    generated_payouts_1 = np.random.choice(payouts_1, size=spins_1, p=calculated_probs_g1)
    generate_revenue_1 = 3 * buyin_1 - generated_payouts_1

    generated_payouts_3 = np.random.choice(payouts_3, size=spins_3, p=calculated_probs_g1)
    generate_revenue_3 = 3 * buyin_3 - generated_payouts_3

    generated_payouts_7 = np.random.choice(payouts_7, size=spins_7, p=calculated_probs_g2)
    generate_revenue_7 = 3 * buyin_7 - generated_payouts_7

    generated_payouts_15 = np.random.choice(payouts_15, size=spins_15, p=calculated_probs_g3)
    generate_revenue_15 = 3 * buyin_15 - generated_payouts_15

    generated_payouts_30 = np.random.choice(payouts_30, size=spins_30, p=calculated_probs_g3)
    generate_revenue_30 = 3 * buyin_30 - generated_payouts_30

    concat_array = np.concatenate((generate_revenue_025, generate_revenue_1, generate_revenue_3,
                                   generate_revenue_7, generate_revenue_15, generate_revenue_30))
    total_revenue = np.sum(concat_array)
    monthly_revenue.append(total_revenue)
    print('{} month completed'.format(i+1))

monthly_revenue_thousands = np.array(monthly_revenue) / 1000
mean_monthly_revenue = np.mean(monthly_revenue_thousands)
confidence_interval = np.percentile(monthly_revenue_thousands,[2.5, 97.5])

fmt = '${x:,.0f}k'
tick = mtick.StrMethodFormatter(fmt)
fig, ax = plt.subplots(1,1)
plt.plot(*dcst.ecdf(monthly_revenue_thousands), linestyle='none', marker='.')
ax.xaxis.set_major_formatter(tick)
plt.xticks(rotation=25)
plt.axvline(x=monthly_theoretical_revenue,color='k')
plt.axvline(x=confidence_interval[0],color='r')
plt.axvline(x=confidence_interval[1],color='g')
plt.xlabel('Revenue ($)')
plt.ylabel('ECDF')
plt.title('Expected Monthly Revenue Distribution')
plt.tight_layout()
plt.show()

print('Monthly theoretical revenue: ${0:,.0f}k'.format(monthly_theoretical_revenue))
print('Mean monthly simulated revenue: ${0:,.0f}k'.format(mean_monthly_revenue))
print('95% confidence interval simulated: ${0:,.0f}k to ${1:,.0f}k'
      .format(confidence_interval[0], confidence_interval[1]))
