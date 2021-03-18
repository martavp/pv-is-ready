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
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.family'] = 'avenir'
plt.rcParams['axes.titlesize'] = 14
plt.figure(figsize=(8, 8))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)

ax1 = plt.subplot(gs1[0,0])
colors={'Solar': 'orange',
        'Wind': 'yellowgreen',
        'Geo Biomass Other': 'coral',
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
for tech in ['Coal', 'Gas', 'Hydro', 'Nuclear', 
              'Wind', 'Solar']: # 'Geo Biomass Other', 'Oil',    
    if tech in ['Wind']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='{} Capacity'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Megawatts'][0:24]
        global_generation_2019 = 1429.6 #TWh
        global_capacity_2019 = 622704 # MW
        energy=excel.loc['Total World'][0:24]*global_generation_2019/global_capacity_2019  #MW -> TWh

    
    if tech in ['Geo Biomass Other']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='{} - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True) 
        years=excel.loc['Terawatt-hours'][0:55]
        energy=excel.loc['Total World'][0:55] #TWh
    if tech in ['Nuclear', 'Hydro', 'Solar']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='{} Generation - TWh'.format(tech),
                              index_col=0, header=0, squeeze=True)         
        years=excel.loc['Terawatt-hours'][0:55]
        energy=excel.loc['Total World'][0:55] #TWh 
    if tech in ['Coal', 'Oil', 'Gas']:
        excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='Elec Gen from {}'.format(tech),
                              index_col=0, header=0, squeeze=True)          
        years=excel.loc['Terawatt-hours'][0:35]
        energy=excel.loc['Total World'][0:35] #TWh
    label='Solar PV' if tech=='Solar' else tech    
    ax1.semilogy(years, energy, linewidth=3, linestyle='-',              
                  color=colors[tech], label=label)

ax1.set_ylabel('Global electricity generation (TWh)', fontsize=18)    
ax1.grid(color='grey', linestyle='--', axis='y', which='both')
ax1.set_ylim(10, 11000)
ax1.set_xlim(1968, 2022)
ax1.text(2009, 15, 'Solar PV', color=colors['Solar'], fontsize=14)
ax1.text(1992, 15, 'Wind', color=colors['Wind'], fontsize=14)
ax1.text(1975, 220, 'Nuclear', color=colors['Nuclear'], fontsize=14)
ax1.text(1990, 5000, 'Coal', color=colors['Coal'], fontsize=14)
ax1.text(1970, 1500, 'Hydro', color=colors['Hydro'], fontsize=14)
ax1.text(1990, 1400, 'Gas', color=colors['Gas'], fontsize=14)

plt.savefig('figures/historical_energy_generation_expansion.tiff', dpi=300, bbox_inches='tight')  