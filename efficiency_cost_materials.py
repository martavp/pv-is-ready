# -*- coding: utf-8 -*-

"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
"""

2. Consumo de plata histórico
3. Predicción de potencia FV de Haegel
4. Perdicción de potencia FV de IAM
(después mirar qué es repesenta renewable primary energy)
5. Revisar precio futuro de PV de IAM y de NREL ¿incluyen lo mismo?
¿precio de módulo o del sistema?

"""

plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.titlesize'] = 14


efficiency=pd.read_csv('data/module_efficiency_historical.csv', 
                       index_col=0, sep=',')
cost=pd.read_csv('data/cost_historical.csv', sep=',')

future_cost_NREL=pd.read_csv('data/NREL_ATB2020.csv', sep=',')
#%%
plt.figure(figsize=(20, 10))

gs1 = gridspec.GridSpec(2, 4)
gs1.update(wspace=0.4, hspace=0.3)
color_1='firebrick'
color_2='grey'
# A) FIGURE CAPACITY FORECAST

EJ2PWh=0.2778 # EJ -> PWh 
kW2kWh=1370 #kWh->kW 
ax0 = plt.subplot(gs1[0,0])

ax0.set_ylabel('Global supply in 2050 (PWh/year)', fontsize=14)    

#Haegel_2019
ax0.plot([1, 1], 
          [x*kW2kWh/1000 for x in [30,70]], #[23.1,80.9]], 
          color=color_1, 
          linewidth=4, 
          marker='_',
          markersize=14)

#Breyer
ax0.plot([2, 2], 
          [x*kW2kWh/1000 for x in [22,63.4]],
          color=color_1, 
          linewidth=4, 
          marker='_',
          markersize=14,)

#Creutzig
ax0.plot([3, 3], 
          [x*EJ2PWh for x in [8, 35]], 
          color='black', 
          linewidth=4, 
          marker='_',
          markersize=14,

)

ax0.plot([4, 4], 
          [x*EJ2PWh for x in [67, 130]], 
          color='black', 
          linewidth=4, 
          marker='_',
          markersize=14)

#van Vuuren
ax0.plot([5, 5], 
         [x*EJ2PWh for x in [32, 135]], 
          color='black', 
          linewidth=4, 
          marker='_',
          markersize=14)

#Roglej
ax0.plot([6, 6], 
         [x*EJ2PWh for x in [89, 230]], 
          color='black',
          linewidth=4, 
          marker='_',
          markersize=14)
ax0.plot([7, 7], 
         [x*EJ2PWh for x in [20, 300]], 
          color='black', 
          linewidth=4, 
          marker='_',
          markersize=14,
          linestyle='dotted')


ax0.text(0.45, 1.01, 'A', transform=ax0.transAxes, fontsize=14)
ax0.set_xticks([1, 2, 3, 4, 5, 6, 7])
ax0.set_xticklabels(['PV \n[4]', 'PV \n[53, \n63]', 'PV \n[39]', 'PV \n[8]', 'PV+ \nwind \n[7]', 
                     'PV+ \nwind+ \nhydro \n[6]', '     BECCS \n[6]' ], fontsize=12)# , rotation=30, ha="right")
ax0.annotate('IAMs', xy=(0.65, 0.89), xytext=(0.65, 0.94), xycoords='axes fraction', 
            fontsize=12, ha='center', va='bottom',
            #bbox=dict(boxstyle='square', fc='white'),
            arrowprops=dict(arrowstyle='-[, widthB=6.0, lengthB=0.5', lw=2.0))
ax0.set_ylim([0, 100])
#%%

# TWh2EJ=1/277.8 # TWh -> EJ
# ax0.fill_between([2028,2050], 
#                  [x*kW2kWh*TWh2EJ for x in [23.1,80.9]], 
#                  [x*kW2kWh*TWh2EJ for x in [23.1,33.9]],
#                  color=color_1, alpha=0.3, 
#                  label='Solar PV (Haegel 2019)')

# ax0.fill_between([2016, 2030, 2050], 
#                  [x*kW2kWh*TWh2EJ for x in [0.29, 3.2, 8.5]], 
#                  [x*kW2kWh*TWh2EJ for x in [0.29, 2, 4.5]],
#                  color='blue', alpha=0.3, 
#                  label='Solar PV (IRENA)')
# ax0.plot([2050, 2050], 
#          [67, 130], 
#          color='blue', 
#          linewidth=6, 
#          label='Creutzig 2017')
# SSPS=['1', '2']
# for SSP in SSPS:
#     SSPdata=pd.read_csv('data/Rogelj_2018/SSP{}_1.9.csv'.format(SSP), sep=',')
#     ax0.fill_between(SSPdata['year'], 
#                      SSPdata['high'], 
#                      SSPdata['low'],
#                  color='black', alpha=0.3, 
#                  label='non-biomass renewable (Rogelj 2018)')
# ax0.legend(fancybox='true', 
#            fontsize=12, 
#            loc='best', 
#            facecolor='white', 
#            frameon=True)
# ax0.set_xlim([2000, 2050])



# ax0 = plt.subplot(gs1[0,0])
# ax0.set_ylabel('Global energy (EJ/year)', fontsize=14)    
# kW2kWh=1370 #kWh->kW 
# TWh2EJ=1/277.8 # TWh -> EJ
# ax0.fill_between([2028,2050], 
#                  [x*kW2kWh*TWh2EJ for x in [23.1,80.9]], 
#                  [x*kW2kWh*TWh2EJ for x in [23.1,33.9]],
#                  color=color_1, alpha=0.3, 
#                  label='Solar PV (Haegel 2019)')

# ax0.fill_between([2016, 2030, 2050], 
#                  [x*kW2kWh*TWh2EJ for x in [0.29, 3.2, 8.5]], 
#                  [x*kW2kWh*TWh2EJ for x in [0.29, 2, 4.5]],
#                  color='blue', alpha=0.3, 
#                  label='Solar PV (IRENA)')
# ax0.plot([2050, 2050], 
#          [67, 130], 
#          color='blue', 
#          linewidth=6, 
#          label='Creutzig 2017')
# SSPS=['1', '2']
# for SSP in SSPS:
#     SSPdata=pd.read_csv('data/Rogelj_2018/SSP{}_1.9.csv'.format(SSP), sep=',')
#     ax0.fill_between(SSPdata['year'], 
#                      SSPdata['high'], 
#                      SSPdata['low'],
#                  color='black', alpha=0.3, 
#                  label='non-biomass renewable (Rogelj 2018)')
# ax0.legend(fancybox='true', 
#            fontsize=12, 
#            loc='best', 
#            facecolor='white', 
#            frameon=True)
# ax0.set_xlim([2000, 2050])
# ax0.text(0.9, 0.9, 'A)', transform=ax0.transAxes, fontsize=14)

# past efficiency: Fraunhofer PV report
# future efficiency: ITPV roadmap

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
ax1.text(2032, 26.5, '?', 
         fontsize=60,
         color='silver')
ax1.text(2027, 27, 'multijunction \n   perovskite', 
         fontsize=14,
             color=color_1)
# ax1.text(2021, 22, 'bifacial', 
#          fontsize=14,
#              color=color_1)
ax1.set_xlim([2005, 2040])
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
# ax2.set_xticks([0.01, 1, 100, 10000, 1000000])
# ax2.set_xticklabels(['0.01', '10', '100', '10000', '1000000'])
ax2.plot([0.2, 1200000],[150, 0.18], linewidth=1, color='black')
ax2.plot([8000, 1200000],[6, 0.16], linewidth=1, color='dimgray')
ax2.text(0.45, 1.01, 'B', transform=ax2.transAxes, fontsize=14)
ax2.text(500, 1.1, '23%', fontsize=14)
ax2.text(200000, 1.1, '40%', fontsize=14, color='dimgray')
#ax2.set_xlim([0.01, 2000000])
#%%
# C) COST FORECAST
# IAM cost assumption:
# NREL cost assumption:
# IRENA: average cost 995€/kW, cost in USA 1221 €/kW

ax3 = plt.subplot(gs1[0,2])

# ax3.plot(future_cost_NREL['year'], 
#          future_cost_NREL['Conservative']/1000,
#          linewidth=3, color=color_1, linestyle='dashed')
# ax3.plot(future_cost_NREL['year'], 
#          future_cost_NREL['Moderate']/1000,
#          linewidth=3, color=color_1, linestyle='dotted')
# ax3.plot(future_cost_NREL['year'], 
#          future_cost_NREL['Advanced']/1000,
#          linewidth=3, color=color_1, linestyle='dashdot')


IAMS=['DIW', 'AIM_E_INDIA', 'DNE21+V.12A', 'EIA', 'GCAM4.2_ADVANCE', 'IEA', 'IMAGE3.0', 
      'MESSAGE ix-GLOBIOM_1.0', 'REMIND1.6', 'IPAC-AIM_technology_V1.0', 'GEM_E3', ]
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
    
#A clean planet for all
ax3.plot([2020, 2030, 2040, 2050], 
          [x/1000 for x in [690, 627, 455, 407]],
          linewidth=3, color=color_2, linestyle='solid', label=None)
ax3.plot([2020, 2030, 2040, 2050], 
          [x/1000 for x in [721, 690, 567, 495]],
          linewidth=3, color=color_2, linestyle='dashed', label='PRIMES')

#ITPV 2017
ax3.plot([2020,2030, 2040, 2050], 
          [x/1000 for x in [573, 391, 302, 246]],
          linewidth=3, color=color_1, label='ITPV2017')
#Breyer
ax3.plot([2020, 2025, 2030, 2035, 2040, 2045, 2050], 
          [x/1000 for x in [431, 333, 275, 235, 204, 181, 164]],
          linewidth=3, color=color_1,label='Vartiainen 2019')
#irena
# ax3.plot([2019, 2019, 2019], 
#           #[995/1000],
#           #[618/1000, 2117/1000],
#          [618/1000, 995/1000, 1404/1000],
#           linewidth=2, 
#           marker='_',
#           color=color_1,label='IRENA 2019')
# ax3.plot([2019], 
#           [2117/1000],
#           linewidth=0, 
#           marker='s',
#           color=color_1,label=None)
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
#ax3.set_xlim([2020, 2050])
# ax3.legend(fancybox='true', 
#            fontsize=14, 
#            loc=(1.05,.01), 
#            facecolor='white', 
#            frameon=True)
# ax3.annotate('IAMs', xy=(2030, 2), xytext=(2040, 2.5), fontsize=12,
#             arrowprops=dict(color='black', headwidth=0.1, width=0.1),)   
# ax3.annotate('', xy=(2040, 1.5), xytext=(2040, 2.5), fontsize=12,
#             arrowprops=dict(color='black', headwidth=0.1,width=0.1))
# ax3.annotate('', xy=(2035, 1.6), xytext=(2040, 2.5), fontsize=12,
#             arrowprops=dict(color='black', headwidth=0.1,width=0.1))
ax3.text(2040, 2.2, 'IAMs', fontsize=12)
ax3.annotate('PRIMES', xy=(2038, 0.6), xytext=(2042, 0.75), color=color_2,
            arrowprops=dict(color=color_2, headwidth=0.1, width=0.1),)

ax3.annotate('ITPV', xy=(2030, 0.25), xytext=(2020, 0.1), color=color_1,
             arrowprops=dict(color=color_1, headwidth=0.1, width=0.1))


# E) USE OF SILVER
# PV Capacity: BP
# Silver consumption:

excel = pd.read_excel('data/bp-stats-review-2020-all-data.xlsx', 
                              sheet_name='Solar Capacity',
                              index_col=0, header=0, squeeze=True) 
 
capacity=0.001*excel.loc['Total World'][0:24] #MW -> GW
capacity.index=[int(x) for x in excel.loc['Megawatts'][0:24]]
capacity.loc[2019]=600 #update 2016 capacity
annual_capacity=capacity.diff()

silver=pd.read_csv('data/silver_demand.csv', 
                       header=None, index_col=0, sep=',')
ax4 = plt.subplot(gs1[1,2])

# ax4.plot(years[9:], capacity[9:]/capacity[14],
#            linewidth=3, color=color_1)
# ax4.set_ylabel('Global PV capacity (relative to 2010)', color=color_1, fontsize=14)    
# ax5 = ax4.twinx() 
# ax5.plot(silver.index, silver[1]/silver[1][2010],
#            linewidth=3, color='black')
# ax5.set_ylabel('Silver consumption for PV (relative to 2010)', fontsize=14) 
# ax4.spines['left'].set_color(color_1)
# ax5.spines['left'].set_color(color_1)
# ax4.tick_params(axis='y', colors=color_1)
# ax4.text(0.9, 0.9, 'E)', transform=ax4.transAxes, fontsize=14)
# ax4.set_ylim([0,15])
# ax5.set_ylim([0,15])
ounce2kg=0.028349523125 # million ounce -> kilo-metric ton (ounce -> kg)
ax4.plot(silver.index[1:], [ounce2kg*1000*silver.loc[year][1]/annual_capacity[year] for year in silver.index[1:]],
            linewidth=3, color=color_1)
ax4.set_xlim([2005,2020])
#million ounces / Gw -> ounces/kW
ax4.set_ylabel('Silver consumption / PV capacity \n (kg/MW)',  fontsize=14)   
ax4.grid(color='grey', linestyle='--', axis='y', which='both')
ax4.text(0.45, 1.01, 'F', transform=ax4.transAxes, fontsize=14)

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
            dpi=300, 
            bbox_inches='tight')  