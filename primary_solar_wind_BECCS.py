# -*- coding: utf-8 -*-

"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
idx = pd.IndexSlice

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 14

plt.figure(figsize=(10, 8))
gs1 = gridspec.GridSpec(1, 1)

ax0 = plt.subplot(gs1[0,0])
EJ2PWh=0.2778 # EJ -> PWh 

year='2050'
region='World'

data_to_plot=[]
for i,document in enumerate(['IPCC_AR5', 'IPCC_SR1.5']):
    if document=='IPCC_AR5':
        #https://tntcat.iiasa.ac.at/AR5DB/
        fn = "data_IAM/ar5_public_version102_compare_compare_20150629-130000.csv"   
        BECCS_name='Primary Energy|Biomass|w/ CCS'
    if document=='IPCC_SR1.5':
        #https://data.ene.iiasa.ac.at/iamc-1.5c-explorer/
        fn="data_IAM/iamc15_scenario_data_world_r2.0.csv"
        #BECCS_name='Primary Energy|Biomass'
        BECCS_name='Secondary Energy|Electricity|Biomass|w/ CCS'
    df = pd.read_csv(fn, encoding="latin-1")
    df = df.set_index(['MODEL', 'SCENARIO', 'REGION', 'VARIABLE', 'UNIT']).sort_index()
    scenarios = df.index.get_level_values('SCENARIO').unique()

    # drop scenarios that do not include Solar Electricity
    scenarios_clean=scenarios
    for scenario in scenarios:
        scenario_df=df.loc[idx[:,scenario,region,:],year].unstack(['VARIABLE','UNIT'])
        try: 
            scenario_df['Secondary Energy|Electricity|Solar']
        except:
            scenarios_clean=[s for s in scenarios_clean if s not in [scenario]] 
        try: 
            scenario_df[BECCS_name]
        except:
            scenarios_clean=[s for s in scenarios_clean if s not in [scenario]]
    solar_generation=[]
    wind_generation=[]
    BECCS_generation=[]
    for scenario in scenarios_clean:    
        scenario_df=df.loc[idx[:,scenario,region,:],year].unstack(['VARIABLE','UNIT'])
        solar_generation = solar_generation + [s for s in scenario_df['Secondary Energy|Electricity|Solar']['EJ/yr'].values]
        wind_generation = wind_generation + [s for s in scenario_df['Secondary Energy|Electricity|Wind']['EJ/yr'].values]
        BECCS_generation = BECCS_generation + [s for s in scenario_df[BECCS_name]['EJ/yr'].values]
        
        
    solar_generation = [s for s in solar_generation if str(s) != 'nan']
    wind_generation = [s for s in wind_generation if str(s) != 'nan']
    BECCS_generation = [s for s in BECCS_generation if str(s) != 'nan']
    data_to_plot.append(solar_generation)
    data_to_plot.append(wind_generation)
    data_to_plot.append(BECCS_generation)

#Electricity produced with biomass is equivalent to (1/0.3) primary energy
data_to_plot[5]=[(1/0.3)*s for s in data_to_plot[5]]
#ax0.set_ylabel('Global electricity in 2050 (PWh/year)', fontsize=14)    
ax0.set_ylabel('Global primary energy in 2050 (EJ/year)', fontsize=14) 
parts=ax0.violinplot(data_to_plot, 
                     showmedians=False, 
                     showextrema=False, 
                     widths=0.7 )


for i, pc in enumerate(parts['bodies']):
    if i==0 or i==3:
        color3='orange'
    if i==1 or i==4:
        color3='dodgerblue'
    if i==2 or i==5:
        color3='black'
    pc.set_facecolor(color3)
    pc.set_edgecolor(color3)
    pc.set_alpha(0.5)
    

ax0.set_xticks([1, 2, 3, 4, 5, 6])
ax0.set_xticklabels(['Solar', 'Wind', 'BECCS', 
                     'Solar', 'Wind', 'BECCS',  ], fontsize=14)

ax0.set_ylim([0, 250])
ax0.annotate('IPCC 5$^{th}$ AR [18]', xy=(0.25, 0.89), xytext=(0.25, 0.94), 
            xycoords='axes fraction', 
            fontsize=14, ha='center', va='bottom',
            #bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=8.0, lengthB=0.5', lw=2.0))
ax0.annotate('IPCC 1.5$^{\circ}$C SR [19]', xy=(0.75, 0.89), xytext=(0.75, 0.94), 
            xycoords='axes fraction', 
            fontsize=14, ha='center', va='bottom',
            #bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=8.0, lengthB=0.5', lw=2.0))
plt.savefig('figures/primary_solar_wind_BECCS.png', 
            dpi=300, 
            bbox_inches='tight')  