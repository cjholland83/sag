#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:59:07 2019

@author: chrisholland
"""

import numpy as np
import matplotlib.pyplot as plt
import dc_stat_think as dcst

# buy in $0.25 to $3 stats
group_1_probabilities = np.array([1,30,75,1000,5000,75000,184506,734388])
group_1_multipliers = np.array([12000,240,120,25,10,6,4,2])

buyin_025 = 0.25
spins_025 = 100000

buyin_1 = 1.0
spins_1 = 100000

buyin_3 = 3.0
spins_3 = 100000

# buy in $7
group_2_probabilities = np.array([1,30,75,1000,5000,75000,214506,704388])
group_2_multipliers = np.array([12000,240,120,25,10,6,4,2])

buyin_7 = 7
spins_7 = 100000

base = 1000000.0
months = 1000

calculated_probs_g1 = group_1_probabilities / base
calculated_probs_g2 = group_2_probabilities / base

payouts_025 = buyin_025 * group_1_multipliers
rake_025 = 3 * buyin_025 - np.dot(payouts_025, calculated_probs_g1)
monthly_theo_rake_025 = rake_025 * spins_025

payouts_1 = buyin_1 * group_1_multipliers
rake_1 = 3 * buyin_1 - np.dot(payouts_1, calculated_probs_g1)
monthly_theo_rake_1 = rake_1 * spins_1

payouts_3 = buyin_3 * group_1_multipliers
rake_3 = 3 * buyin_3 - np.dot(payouts_3, calculated_probs_g1)
monthly_theo_rake_3 = rake_3 * spins_3

payouts_7 = buyin_7 * group_2_multipliers
rake_7 = 3 * buyin_7 - np.dot(payouts_7, calculated_probs_g2)
monthly_theo_rake_7 = rake_7 * spins_7

monthly_theoretical_revenue = np.sum([monthly_theo_rake_025, monthly_theo_rake_1, monthly_theo_rake_3,
                                      monthly_theo_rake_7])

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

    total_revenue = np.sum([generate_revenue_025, generate_revenue_1, generate_revenue_3,
                            generate_revenue_7])
    monthly_revenue.append(total_revenue)
    print('{} month completed'.format(i+1))

mean_monthly_revenue = np.mean(monthly_revenue)
confidence_interval = np.percentile(monthly_revenue,[2.5, 97.5])

_ = plt.plot(*dcst.ecdf(monthly_revenue), linestyle='none', marker='.')
_ = plt.axvline(x=monthly_theoretical_revenue,color='k')
_ = plt.axvline(x=confidence_interval[0],color='r')
_ = plt.axvline(x=confidence_interval[1],color='g')
_ = plt.xlabel('Revenue ($)')
_ = plt.ylabel('ECDF')
_ = plt.title('Expected Monthly Revenue Distribution')
plt.show()

print('Monthly theoretical revenue: ${0:,.0f}'.format(monthly_theoretical_revenue))
print('Mean monthly simulated revenue: ${0:,.0f}'.format(mean_monthly_revenue))
print('95% confidence interval simulated: ${0:,.0f} to ${1:,.0f}'
      .format(confidence_interval[0], confidence_interval[1]))
