# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec




plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['axes.titlesize'] = 14
plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)


ax1 = plt.subplot(gs1[0,0])

penetration=pd.read_csv('data/solar_wind_penetration.csv', 
                       index_col=0, sep=',')


ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

color_0='dodgerblue'
color_1='firebrick'
color_2='darkblue'
ax1.plot([0,100],[100,0], color=color_0, linewidth=3)
ax1.set_ylim([0,100])
ax1.set_xlim([0,100])
ax1.set_xlabel('Solar penetration (%)')
ax1.set_ylabel('Wind penetration (%)')
ax1.text(35, 35, '100% wind & solar electricity', rotation=-45, 
         color=color_0, fontsize=16)
#PRIMES
for EUscenario in ['Baseline','EE', 'CIRC', 'ELEC', 'H2', 'P2X', 'COMBO', '1.5TECH', '1.5LIFE', ]:
    ax1.plot(penetration.loc[EUscenario,'solar'], penetration.loc[EUscenario,'wind'], 
             marker='o', markersize=10, color='silver')
ax1.text(10, 55, 'PRIMES [15]', color='dimgray', fontsize=12)

#PRIMES (Stepping-up)

for EUscenario in ['BSL','REG', 'MIX', 'CPRICE', 'ALLBNK' ]:
    ax1.plot(penetration.loc[EUscenario,'solar'], penetration.loc[EUscenario,'wind'], 
             marker='o', markersize=10, color='dimgray')
ax1.text(15, 38, 'PRIMES [16]', color='dimgray', fontsize=12)


#ENTSOE
ax1.plot(penetration.loc['ENTSOE','solar'], penetration.loc['ENTSOE','wind'], 
             marker='o', markersize=10, color=color_2)
ax1.text(8, 25, 'ENTSOE', color=color_2, fontsize=12)

#BNEF
ax1.plot(penetration.loc['BNEF','solar'], penetration.loc['BNEF','wind'], 
             marker='s', markersize=10, 
             markeredgecolor=color_2,
             markerfacecolor='white')     
ax1.text(20, 20, 'BNEF', color=color_2, fontsize=12)

#Victoria
ax1.plot(penetration.loc['Victoria','solar'], penetration.loc['Victoria','wind'], 
             marker='o', markersize=10, color=color_1) 
ax1.text(40, 42, 'Victoria', color=color_1, fontsize=12)

#Child
ax1.plot(penetration.loc['Child','solar'], penetration.loc['Child','wind'], 
             marker='o', markersize=10, color=color_1) 
ax1.text(40, 32, 'Child', color=color_1, fontsize=12)

#Bogdanov
ax1.plot(penetration.loc['Bogdanov','solar'], penetration.loc['Bogdanov','wind'], 
             marker='s', markersize=10, 
             markeredgecolor=color_1,
             markerfacecolor='white') 
ax1.text(62, 16, 'Bogdanov', color=color_1, fontsize=12)

   
#Creutzig
ax1.annotate("", xy=(30, 4), xytext=(50,4),
             arrowprops=dict(arrowstyle="<->", color='black'))
ax1.text(34.5, 5, 'Creutzig', color='black', fontsize=12)

# #van Vuuren
# ax1.annotate("", xy=(0, 36), xytext=(36,0),
#              arrowprops=dict(arrowstyle="<->", color='black'))
# ax1.text(13.5, 13.5, 'van Vuuren', rotation=-45, 
#          color='black', fontsize=12)

# #Rogelj
# ax1.annotate("", xy=(0, 80), xytext=(80,0),
#              arrowprops=dict(arrowstyle="<->", color='black'))
# ax1.text(37.5, 37.5, 'Rogelj', rotation=-45, 
#          color='black', fontsize=12)

plt.savefig('figures/pv_plus_wind_penetration.png', dpi=300, bbox_inches='tight')  