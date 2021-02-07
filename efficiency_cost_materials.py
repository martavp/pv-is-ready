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

plt.figure(figsize=(20, 10))
gs1 = gridspec.GridSpec(2, 4)
gs1.update(wspace=0.4, hspace=0.3)
color_1='firebrick'
color_2='grey'

"""
FIGURE A) SOLAR ELECTRICITY IN 2050
"""
ax0 = plt.subplot(gs1[0,0])
EJ2PWh=0.2778 # EJ -> PWh 
kW2kWh=1370 #kWh->kW

year='2050'
region='World'

data_to_plot=[]
for i,document in enumerate(['IPCC_AR5', 'IPCC_SR1.5']):
    if document=='IPCC_AR5':
        #https://tntcat.iiasa.ac.at/AR5DB/
        fn = "data_IAM/ar5_public_version102_compare_compare_20150629-130000.csv"   

    if document=='IPCC_SR1.5':
        #https://data.ene.iiasa.ac.at/iamc-1.5c-explorer/
        fn="data_IAM/iamc15_scenario_data_world_r2.0.csv"
    
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
    solar_generation=[]
    for scenario in scenarios_clean:    
        scenario_df=df.loc[idx[:,scenario,region,:],year].unstack(['VARIABLE','UNIT'])
        solar_generation = solar_generation + [s for s in scenario_df['Secondary Energy|Electricity|Solar']['EJ/yr'].values]
        
    solar_generation = [EJ2PWh*s for s in solar_generation if str(s) != 'nan']

    data_to_plot.append(solar_generation)

ax0.set_ylabel('Global PV electricity in 2050 (PWh/year)', fontsize=14)    


#Kurtz_Revisiting the Terawatt challenge
ax0.plot([3], 
          [x*kW2kWh/1000 for x in [37]], 
          color=color_1, 
          linewidth=4, 
          marker='*',
          markersize=14)

#Haegel_2019
ax0.plot([4, 4], 
          [x*kW2kWh/1000 for x in [30,70]], 
          color=color_1, 
          linewidth=4, 
          marker='_',
          markersize=14)

#Breyer 
ax0.plot([5, 5], 
          [x*kW2kWh/1000 for x in [22,63.4]],
          color=color_1, 
          linewidth=4, 
          marker='_',
          markersize=14,)


parts=ax0.violinplot(data_to_plot, 
                     showmedians=False, 
                     showextrema=False, 
                     widths=0.7 )

for pc in parts['bodies']:
    pc.set_facecolor('gray')
    pc.set_edgecolor('black')
    pc.set_alpha(1)
    


ax0.text(0.45, 1.01, 'A', transform=ax0.transAxes, fontsize=14)
ax0.set_xticks([1, 2, 3, 4, 5])
ax0.set_xticklabels(['IPCC \n5$^{th}$AR \n[8]', 
                     'IPCC \nSR1.5$^{\circ}$C \n[9]', 
                     'Kurtz \n[125]',
                     'Haegel \n[6]', 
                     'Breyer \n[83,120]',], fontsize=12)

ax0.set_ylim([0, 100])

#%%
"""
FIGURE D) PAST AND FUTURE EFFICIENCY EVOLUTION
"""
# past efficiency: Fraunhofer PV report
# future efficiency: ITPV roadmap
efficiency=pd.read_csv('data/module_efficiency_historical.csv', 
                       index_col=0, sep=',')
cost=pd.read_csv('data/cost_historical.csv', sep=',')
ax1 = plt.subplot(gs1[1,0])

ax1.plot(efficiency.index, 100*efficiency['multi'],
         linewidth=3, color=color_1, label='multi-Si')
ax1.plot(efficiency.index, 100*efficiency['mono'],
         linewidth=3, linestyle='dashed', color=color_1, label='mono-Si')

ax1.plot([2020],[20.3],
         marker='s', 
         markersize=10, 
         markerfacecolor='white',
         markeredgecolor=color_1,
         linewidth=0) 

ax1.plot([2020],[21],
         marker='*', 
         markersize=12, 
         markerfacecolor='white',
         markeredgecolor=color_1,
         linewidth=0) 

ax1.plot([2030],[22.5],
         marker='s', 
         markersize=10, 
         markerfacecolor='white',
         markeredgecolor=color_1,
         linewidth=0, 
         label='PERC') 

ax1.plot([2030],[24],
         marker='*', 
         markersize=12, 
         markerfacecolor='white',
         markeredgecolor=color_1,
         linewidth=0, 
         label='HIT-IBC') 

ax1.grid(color='grey', linestyle='--', axis='y', which='both')
ax1.set_ylabel('Efficiency (%)', fontsize=14)    
ax1.set_ylim(12,30)
ax1.set_xlim(2005, 2045)
ax1.text(2027, 26.5, '?', 
         fontsize=60,
         color='silver')
ax1.text(2023, 27, 'multijunction \n   perovskite', 
         fontsize=14,
             color=color_1)
ax1.set_xlim([2005, 2035])
ax1.legend(fancybox='true', 
           fontsize=12, 
           loc='upper left', 
           facecolor='white', 
           frameon=True,
           edgecolor='black')
ax1.text(0.45, 1.01, 'D', transform=ax1.transAxes, fontsize=14)

# B) LEARNING CURVE

ax2 = plt.subplot(gs1[0,1])
ax2.loglog(cost['volume'], cost['cost'],
           marker='o', markerfacecolor=color_1,
         linewidth=0, color=color_1)

ax2.set_ylabel('Module price (USD2019/W$_p$)', fontsize=14)    
ax2.set_xlabel('Cumulative PV capacity (MW)', fontsize=14)  
ax2.grid(color='grey', linestyle='--', axis='both', which='both')
ax2.set_ylim(0.1,200)
ax2.set_xlim(0.01, 10000000)
ax2.set_yticks([0.1, 1, 10, 100])
ax2.set_yticklabels(['0.1', '1', '10', '100'])
ax2.plot([0.2, 1200000],[150, 0.18], linewidth=1, color='black')
ax2.plot([8000, 1200000],[6, 0.16], linewidth=1, color='dimgray')
ax2.text(0.45, 1.01, 'B', transform=ax2.transAxes, fontsize=14)
ax2.text(500, 1.1, '23%', fontsize=14)
ax2.text(200000, 1.1, '40%', fontsize=14, color='dimgray')

#%%
"""
FIGURE C) COST FORECAST
"""

# IAM cost assumption: Krey 2019
# IRENA: average cost 995€/kW, cost in USA 1221 €/kW

ax3 = plt.subplot(gs1[0,2])

IAMS=['DIW', 'AIM_E_INDIA', 'DNE21+V.12A', 'EIA', 'GCAM4.2_ADVANCE', 'IEA', 
      'IMAGE3.0', 'MESSAGE ix-GLOBIOM_1.0', 'REMIND1.6', 
      'IPAC-AIM_technology_V1.0', 'GEM_E3', ]
marker_IAM={'DIW':'|',
            'AIM_E_INDIA': 's', 
            'DNE21+V.12A': '*', 
            'EIA': 'v', 
            'GCAM4.2_ADVANCE': '^', 
            'IEA': 'p', 
            'IMAGE3.0':'+', 
            'MESSAGE ix-GLOBIOM_1.0':'d', 
            'REMIND1.6':'o', 
            'IPAC-AIM_technology_V1.0':'_', 
            'GEM_E3':'.' }
USD2010_to_USD2019=1.17 
for IAM in IAMS:
    IAM_cost=pd.read_csv('data/Krey_2019/cost_{}.csv'.format(IAM), 
                       header=None, index_col=0, sep=',')
    label='IAMs' if IAM=='DNE21+V.12A' else None
    ax3.plot(IAM_cost.index, IAM_cost[1]*USD2010_to_USD2019/1000,
           linewidth=1, color='black', marker=marker_IAM[IAM], label=label)
    
#PRIMES (A clean planet for all)
ax3.plot([2020, 2030, 2040, 2050], 
          [x/1000 for x in [690, 627, 455, 407]],
          linewidth=3, color=color_2, linestyle='solid', label=None)
ax3.plot([2020, 2030, 2040, 2050], 
          [x/1000 for x in [721, 690, 567, 495]],
          linewidth=3, color=color_2, linestyle='dashed', label='PRIMES')

#ETIP-PV 2017
# ax3.plot([2020,2030, 2040, 2050], 
#           [x/1000 for x in [573, 391, 302, 246]],
#           linewidth=3, color=color_1, label='ETIP-PV2017')


#ITRPV 2020
Dollar2Euro=0.82
ax3.plot([2020, 2024, 2027, 2030], 
           [Dollar2Euro*x/1000 for x in [685, 602, 502, 418]],
           linewidth=3, color=color_1, label='ITRPV')

# #Vartiainen
ax3.plot([2020, 2025, 2030, 2035, 2040, 2045, 2050], 
          [x/1000 for x in [431, 333, 275, 235, 204, 181, 164]],
          linewidth=3, color=color_1,label='Vartiainen 2019')

#IRENA
ax3.plot([2019], 
          [995/1000],
          linewidth=0, 
          marker='*',
          markersize=12, 
          markerfacecolor='white',
          markeredgecolor=color_1,
          color=color_1,label=None) 
ax3.plot([2019], 
          [618/1000],
          linewidth=0, 
          marker='o',
          markersize=10, 
          markerfacecolor='white',
          markeredgecolor=color_1,
          color=color_1,label=None)  

ax3.set_ylabel('PV system price (USD2019/W$_p$)', fontsize=14)    
ax3.text(0.45, 1.01, 'C', transform=ax3.transAxes, fontsize=14)
ax3.set_ylim([0, 3.3 ])
ax3.set_yticks([0, 1, 2 ,3])
ax3.set_yticklabels(['0','1','2','3'])

ax3.text(2040, 2.2, 'IAMs', fontsize=12)
ax3.annotate('PRIMES [24]', xy=(2045, 0.55), xytext=(2038, 0.7), color=color_2,
            arrowprops=dict(color=color_2, headwidth=0.1, width=0.1),)

ax3.annotate('Vartiainen [36]', xy=(2030, 0.25), xytext=(2020, 0.1), color=color_1,
              arrowprops=dict(color=color_1, headwidth=0.1, width=0.1))

ax3.annotate('ITRPV', xy=(2022, 0.54), xytext=(2012, 0.35), color=color_1,
             arrowprops=dict(color=color_1, headwidth=0.1, width=0.1))

# color_10='blue'
# ILR=1.34 #Inverter Loading Ratio
# ax3.plot([2019, 2030, 2040, 2050], 
#           [Dollar2Euro*x/(1000*ILR) for x in [1375, 673, 590, 507]],
#           linewidth=3, color=color_10, #linestyle='dashed',
#           label='NREL Advanced')
# ax3.plot([2019, 2030, 2040, 2050], 
#           [Dollar2Euro*x/(1000*ILR) for x in [1375, 819, 746, 673]],
#           linewidth=3, color=color_10, linestyle='dotted',
#           label='NREL Moderate')
# ax3.plot([2019, 2030, 2040, 2050], 
#           [Dollar2Euro*x/(1000*ILR) for x in [1375, 1197, 1008, 819]],
#           linewidth=3, color=color_10, linestyle='dashed',
#           label='NREL Conservative')


"""
FIGURE F) USE OF SILVER
"""

# PV Capacity: BP
# Silver consumption: Silver Institute report 2020
excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='Solar Capacity',
                              index_col=0, header=0, squeeze=True) 
 
capacity=0.001*excel.loc['Total World'][0:24] #MW -> GW
capacity.index=[int(x) for x in excel.loc['Megawatts'][0:24]]
capacity.loc[2019]=600 #update 2019 capacity
annual_capacity=capacity.diff()

silver=pd.read_csv('data/silver_demand.csv', 
                       header=None, index_col=0, sep=',')
ax4 = plt.subplot(gs1[1,2])

ounce2kg=0.028349523125 # million ounce -> kilo-metric ton (ounce -> kg)
ax4.plot(silver.index[1:], [ounce2kg*1000*silver.loc[year][1]/annual_capacity[year] for year in silver.index[1:]],
            linewidth=3, color=color_1)
ax4.set_xlim([2005,2020])
#million ounces / Gw -> ounces/kW
ax4.set_ylabel('Silver consumption / PV capacity \n (mg/W)',  fontsize=14)   
ax4.grid(color='grey', linestyle='--', axis='y', which='both')
ax4.text(0.45, 1.01, 'F', transform=ax4.transAxes, fontsize=14)

"""
FIGURE E) AGE OF INSTALLED PV POWER PLANTS
"""

ax5 = plt.subplot(gs1[1,1])
ax5.bar(range(len(annual_capacity)), 
              annual_capacity, 
              width=0.8,
              color='black')
ax5.plot([-6, -6],[0,110], 
         linewidth=65, 
         color=color_1, alpha=0.3)
ax5.text(-1.5, 45, 'expected \n lifetime', fontsize=14, color=color_1)
ax5.set_xlabel('Years from installation')
ax5.set_ylabel('Capacity (GW)')
ax5.set_xticks([-11, -6, -1, 4, 9, 14, 19])
ax5.set_xticklabels(['35', '30','25', '20', '15', '10', '5'])
ax5.set_xlim(24,-11)
ax5.set_ylim(0,105)
#ax5.set_yscale('log')
ax5.text(0.45, 1.01, 'E', transform=ax5.transAxes, fontsize=14)
plt.savefig('figures/cost_efficiency.png', 
            dpi=600, 
            bbox_inches='tight')  