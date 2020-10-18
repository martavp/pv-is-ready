# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import numpy as np



plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['axes.titlesize'] = 16
plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
colors={'Solar': 'gold',
        'Wind': 'yellowgreen',
        'Geothermal': 'coral',
        'Hydro':'dodgerblue',
        'Nuclear': 'firebrick',
        'Coal':'black',
        'Oil': 'dimgray',
        'Gas':'gray'}
h_eq={'Hydro':8000,
      'Nuclear':8000,
      'Coal':8000,
      'Oil':8000,
      'Gas':8000}
for tech in ['Gas', 'Coal', 'Nuclear','Hydro', 'Solar', 'Wind', 'Geothermal']: #'Oil',
    if tech in ['Solar', 'Wind', 'Geothermal']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='{} Capacity'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Megawatts'][0:24]
        capacity=0.001*excel.loc['Total World'][0:24] #MW -> GW
    if tech in ['Nuclear', 'Hydro']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='{} Generation - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True)         
        years=excel.loc['Terawatt-hours'][0:55]
        capacity=excel.loc['Total World'][0:55]*1000/h_eq[tech] #TWh -> GW
    if tech in ['Coal', 'Oil', 'Gas']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='Elec Gen from {}'.format(tech),
                              index_col=0, header=0, squeeze=True)          
        years=excel.loc['Terawatt-hours'][0:35]
        capacity=excel.loc['Total World'][0:35]*1000/h_eq[tech] #TWh -> GW
    ax1.semilogy(years, capacity, linewidth=3, linestyle='-',              
                 color=colors[tech], label=tech)

ax1.set_ylabel('Global installed capacity (GW)', fontsize=16)    
ax1.grid(color='lightgrey', linestyle='--', axis='y', which='both')
ax1.set_ylim(10, 1500)
ax1.set_xlim(1968, 2022)
ax1.legend(fancybox=True, fontsize=16, loc=(1.01, 0.), facecolor='white', frameon=True)
plt.savefig('historical_capacity_expansion.png', dpi=300, bbox_inches='tight')  