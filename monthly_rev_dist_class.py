#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import dc_stat_think as dcst


class Spins:
    """class for determining spin revenue"""
    def __init__(self, buyin, number_spins, multipliers, instances, base):
        self.buyin = buyin
        self.number_spins = number_spins
        self.multipliers = multipliers
        self.instances = instances
        self.base = base
        self.probabilities = instances / base
        self.payouts = buyin * multipliers
        self.rake = 3 * buyin - np.dot(self.payouts, self.probabilities)
        self.monthly_theo_rake = self.rake * number_spins

    def generate_revenue(self):
        revenue = np.sum(3 * self.buyin - np.random.choice(self.payouts, size=self.number_spins, p=self.probabilities))
        return revenue

# standard multiplers
multipliers_standard = np.array([12000,240,120,25,10,6,4,2])

# standard base
base_standard = 1000000

# group 1 instances
instances_g1 = np.array([1,30,75,1000,5000,75000,184506,734388])

buyin_1 = 1
number_spins_1 = 5000

buyin_3 = 3
number_spins_3 = 1000

spins_1 = Spins(buyin_1, number_spins_1, multipliers_standard, instances_g1, base_standard)
spins_3 = Spins(buyin_3, number_spins_3, multipliers_standard, instances_g1, base_standard)

total_monthly_theo_rake = np.sum([spins_1.monthly_theo_rake, spins_3.monthly_theo_rake])

monthly_revenues = []

months = 10000

for i in range(months):

    total_revenue = np.sum([spins_1.generate_revenue(),spins_3.generate_revenue()])

    monthly_revenues.append(total_revenue)

mean_monthly_revenue = np.mean(monthly_revenues)
confidence_interval = np.percentile(monthly_revenues,[2.5, 97.5])

print('rake on $1 spin: ',spins_1.rake)
print('rake on $3 spin: ',spins_3.rake)
print('theoretical monthly rake: ',total_monthly_theo_rake)
print('simulated monthly rake: ',mean_monthly_revenue)
print('95% confidence interval: ',confidence_interval)
