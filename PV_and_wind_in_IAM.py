# -*- coding: utf-8 -*-
"""
@author: Marta

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
idx = pd.IndexSlice

document='IPCC_AR5'
option='primary energy'
year='2050'
region='World'
# temp threshold, only plots scenario with lower tempt
# (currently not in use)
T_threshold=10 


if document=='IPCC_AR5':
    #https://tntcat.iiasa.ac.at/AR5DB/
    fn = "data_IAM/ar5_public_version102_compare_compare_20150629-130000.csv"   
    Temperature_parameter = 'Temperature|Global Mean|MAGICC6|MED'

if document=='IPCC_SR1.5':
    #https://data.ene.iiasa.ac.at/iamc-1.5c-explorer/
    fn="data_IAM/iamc15_scenario_data_world_r2.0.csv"
    Temperature_parameter = 'AR5 climate diagnostics|Temperature|Global Mean|MAGICC6|MED'
    
df = pd.read_csv(fn, encoding="latin-1")
df = df.set_index(['MODEL', 'SCENARIO', 'REGION', 'VARIABLE', 'UNIT']).sort_index()
scenarios = df.index.get_level_values('SCENARIO').unique()

#%%
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
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

color_0='orange'
color_1='firebrick'
color_2='dodgerblue'
ax1.plot([0,100],[100,0], color=color_0, linewidth=3)
ax1.set_ylim([0,100])
ax1.set_xlim([0,100])
ax1.set_xlabel('Solar penetration (%)')
ax1.set_ylabel('Wind penetration (%)')
ax1.text(35.5, 35.5, '100% wind & solar ' + option, rotation=-45, 
         color=color_0, fontsize=16)


#%%
# drop scenarios that do not include any of the variables needed
scenarios_clean=scenarios
for scenario in scenarios:
    scenario_df=df.loc[idx[:,scenario,region,:],year].unstack(['VARIABLE','UNIT'])
    try: 
        scenario_df['Secondary Energy|Electricity|Solar']
    except:
        scenarios_clean=[s for s in scenarios_clean if s not in [scenario]]   
    try: 
        scenario_df[Temperature_parameter]
    except:
        scenarios_clean=[s for s in scenarios_clean if s not in [scenario]]         
    try: 
        scenario_df['Primary Energy|Solar']
    except:
        scenarios_clean=[s for s in scenarios_clean if s not in [scenario]]
 
# to read only scenarios included in EMF27 analysis       
#scenarios_clean=[s for s in scenarios_clean if 'EMF27' in s]        
#%%         

solar_ratio=[]
wind_ratio=[]
solar_generation=[]
for scenario in scenarios_clean:
    #print(scenario)
    scenario_df=df.loc[idx[:,scenario,region,:],year].unstack(['VARIABLE','UNIT'])
    if option=='electricity':        
        # Calculate the solar and wind share in electricity, only if temperature  
        # is included in the scenario and it is below T_threshold
        ratio = [[100*(solar/total).item(), 100*(wind/total).item()] for solar,wind,total,temperature in 
                      zip(scenario_df['Secondary Energy|Electricity|Solar'].values,
                          scenario_df['Secondary Energy|Electricity|Wind'].values,
                          scenario_df['Secondary Energy|Electricity'].values,
                          scenario_df[Temperature_parameter].values)
                      ]#if ( np.isnan(temperature)==False and temperature<T_threshold)]
        solar_generation = solar_generation + [s for s in scenario_df['Secondary Energy|Electricity|Solar']['EJ/yr'].values]
    
        ax1.plot([r[0] for r in ratio], [r[1] for r in ratio], marker='s', markersize=10, 
                 markerfacecolor=(1,1,1,0),  linewidth=0,
                 markeredgecolor='gray')
        
        #save solar and wind ratios
        solar_ratio=solar_ratio + [r[0] for r in ratio]
        wind_ratio=wind_ratio + [r[1] for r in ratio]
    
    if option=='primary energy':
        ratio = [[100*(solar/total).item(), 100*(wind/total).item()] for solar,wind,total,temperature in 
                 # I don't use 'Primary Energy|Solar' to avoid including solar thermal energy
                  zip(scenario_df['Secondary Energy|Electricity|Solar'].values,
                      scenario_df['Secondary Energy|Electricity|Wind'].values,
                      scenario_df['Primary Energy'].values,
                      scenario_df[Temperature_parameter].values)
                  ]#if ( np.isnan(temperature)==False and temperature<T_threshold)]
        
        ax1.plot([r[0] for r in ratio], [r[1] for r in ratio], marker='s', markersize=10, 
                 markerfacecolor=(1,1,1,0),  linewidth=0,
                 markeredgecolor='gray')
                #save solar and wind ratios
        solar_ratio=solar_ratio + [r[0] for r in ratio]
        wind_ratio=wind_ratio + [r[1] for r in ratio]

          
print('average solar penetration = ' + str(np.array(solar_ratio).mean())+ ' %')
print('average wind penetration = ' + str(np.array(wind_ratio).mean())+ ' %')
print('number of scenarios included = '+ str(len([s for s in solar_ratio if str(s) != 'nan'])))
# ax1.text(55,79,document + ' ' + option, fontsize=16)
# ax1.text(55,75,'average solar = ' + str(np.array(solar_ratio).mean().round(1))+ ' %', fontsize=16)
# ax1.text(55,71,'average wind = ' + str(np.array(wind_ratio).mean().round(1))+ ' %', fontsize=16)

#%%
if option=='electricity':
    solar_generation = [s for s in solar_generation if str(s) != 'nan']
    print('average solar generation = ' + str(np.array(solar_generation).mean()) + 'EJ/yr')
    print('max solar generation = ' + str(np.array(solar_generation).max()) + 'EJ/yr')
    print('min solar generation = ' + str(np.array(solar_generation).min()) + 'EJ/yr') 

penetration=pd.read_csv('data/solar_wind_electricity_penetration.csv', 
                       index_col=0, sep=',')
if option=='electricity':
    if document=='IPCC_AR5':
        ax1.text(18, 8, 'IPCC 5$^{th}$AR', color='dimgray', fontsize=12)
    
    if document=='IPCC_SR1.5':
        ax1.text(18, 8, 'IPCC SR 1.5$^{\circ}$C', color='dimgray', fontsize=12)
    #PRIMES (Clean energy for all Europeans)
    for EUscenario in ['Baseline','EE', 'CIRC', 'ELEC', 'H2', 'P2X', 'COMBO', '1.5TECH', '1.5LIFE', ]:
        ax1.plot(penetration.loc[EUscenario,'solar'], penetration.loc[EUscenario,'wind'], 
                 marker='o', markersize=10, markerfacecolor=(1,1,1,0), markeredgecolor='black')
    ax1.text(10, 55, 'PRIMES [ref]', color='black', fontsize=12)

    #PRIMES (Stepping-up)
    for EUscenario in ['BSL','REG', 'MIX', 'CPRICE', 'ALLBNK' ]:
        ax1.plot(penetration.loc[EUscenario,'solar'], penetration.loc[EUscenario,'wind'], 
                 marker='o', markersize=10, color='black')
    ax1.text(15, 38, 'PRIMES [ref]', color='black', fontsize=12)


    #ENTSOE
    ax1.plot(penetration.loc['ENTSOE','solar'], penetration.loc['ENTSOE','wind'], 
                  marker='o', markersize=10, color=color_2)
    ax1.text(2, 28, 'ENTSOE', color=color_2, fontsize=12)

    #BNEF 2020
    ax1.plot(penetration.loc['BNEF','solar'], penetration.loc['BNEF','wind'], 
                  marker='s', markersize=10, 
                  markeredgecolor=color_2,
                  markerfacecolor=color_2)     
    ax1.text(25.5, 31.5, 'BNEF', color=color_2, fontsize=12)

    #Shell Sky
    ax1.plot(penetration.loc['Sky','solar'], penetration.loc['Sky','wind'], 
                  marker='s', markersize=10, 
                  markeredgecolor=color_2,
                  markerfacecolor=color_2)     
    ax1.text(38.5, 24.5, 'Shell Sky', color=color_2, fontsize=12)

    #Victoria
    ax1.plot(penetration.loc['Victoria','solar'], penetration.loc['Victoria','wind'], 
                  marker='o', markersize=10, color=color_1) 
    ax1.text(40, 42, 'Victoria [ref]', color=color_1, fontsize=12)

    #Child
    ax1.plot(penetration.loc['Child','solar'], penetration.loc['Child','wind'], 
              marker='o', markersize=10,  markeredgecolor=color_1,
                  markerfacecolor=color_1) 
    ax1.text(41, 31, 'Child [ref]', color=color_1, fontsize=11)

    #Bogdanov
    ax1.plot(penetration.loc['Bogdanov','solar'], penetration.loc['Bogdanov','wind'], 
                  marker='s', markersize=10, 
                  markeredgecolor=color_1,
                  markerfacecolor='white') 
    ax1.text(62, 16, 'Bogdanov [ref]', color=color_1, fontsize=12)
   
    #Solar Power Europe
    ax1.plot(penetration.loc['SolarPower','solar'], penetration.loc['SolarPower','wind'], 
                  marker='o', markersize=10, 
                  markeredgecolor=color_1,
                  markerfacecolor=color_1) 
    ax1.text(57.5, 29, 'SPE [ref]', color=color_1, fontsize=12)
    
    
    #Pursiheimo
    ax1.plot(penetration.loc['Pursiheimo','solar'], penetration.loc['Pursiheimo','wind'], 
                  marker='s', markersize=10, 
                  markeredgecolor='black',
                  markerfacecolor='white') 
    ax1.text(69, 8, 'Pursiheimo [ref]', color='black', fontsize=12)
    
    #Jacobson
    ax1.plot(penetration.loc['Jacobson','solar'], penetration.loc['Jacobson','wind'], 
                  marker='s', markersize=10, 
                  markeredgecolor='black',
                  markerfacecolor='white') 
    ax1.text(42, 33.5, 'Jacobson [ref]', color='black', fontsize=11)
    
    #Creutzig
    ax1.annotate("", xy=(30, 4), xytext=(50,4),
                 arrowprops=dict(arrowstyle="<->", color='black'))
    ax1.text(32, 1.5, 'Creutzig [ref]', color='black', fontsize=12)


plt.savefig('figures/pv_and_wind_in_IAM_' + option + '_' + document + '.png', dpi=300, bbox_inches='tight')