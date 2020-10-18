# -*- coding: utf-8 -*-
"""
@author: Marta
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


from matplotlib.legend_handler import HandlerPatch
from matplotlib.patches import Circle, Ellipse

def make_handler_map_to_scale_circles_as_in(ax, dont_resize_actively=False):
    fig = ax.get_figure()

    def axes2pt():
        return np.diff(ax.transData.transform([(0, 0), (1, 1)]), axis=0)[
            0] * (72. / fig.dpi)

    ellipses = []
    if not dont_resize_actively:
        def update_width_height(event):
            dist = axes2pt()
            for e, radius in ellipses:
                e.width, e.height = 2. * radius * dist
        fig.canvas.mpl_connect('resize_event', update_width_height)
        ax.callbacks.connect('xlim_changed', update_width_height)
        ax.callbacks.connect('ylim_changed', update_width_height)

    def legend_circle_handler(legend, orig_handle, xdescent, ydescent,
                              width, height, fontsize):
        w, h = 2. * orig_handle.get_radius() * axes2pt()
        e = Ellipse(xy=(0.5 * width - 0.5 * xdescent, 0.5 *
                        height - 0.5 * ydescent), width=w, height=w)
        ellipses.append((e, orig_handle.get_radius()))
        return e
    return {Circle: HandlerPatch(patch_func=legend_circle_handler)}


def make_legend_circles_for(sizes, scale=1.0, **kw):
    return [Circle((0, 0), radius=(s / scale)**0.5, **kw) for s in sizes]


plt.style.use('seaborn-ticks')
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
#params = {'legend.fontsize': 20,
#          'legend.handlelength': 2}
#plot.rcParams.update(params)

plt.rcParams['axes.titlesize'] = 14
plt.figure(figsize=(10,10))
gs1 = gridspec.GridSpec(1, 1)
gs1.update(wspace=0.2, hspace=0.2)



df=pd.read_csv('data/pv_penetration.csv', index_col=0, header=0)

ax1 = plt.subplot(gs1[0,0])

years=['2010', '2019', '2030']

colors={'Spain': 'firebrick',        
        'Germany': 'dodgerblue',       
        'California': 'gold',
        'UK':'darkblue',
        'Honduras':'black',
        'China':'lightblue', #'aliceblue',
        'India':'gray',
        'Japan':'darkorange',
        'Italy':'yellowgreen',
        'Australia':'green',
        'Hawaii':'brown',
        'Chile':'violet'}
xpos={  
        'Spain': 0,
        'Germany': 0,       
        'California': 0,
        'UK':0,
        'Honduras':0,
        'China':0.3,
        'India':0.02,
        'Japan':0,
        'Italy':0,
        'Australia':0,
        'Hawaii':0,
        'Chile':0}

ypos={  
        'Spain': 0,
        'Germany': 0.4,       
        'California': 0,
        'UK':0.7,
        'Honduras':0.1,
        'China':0,
        'India':-0.7,
        'Japan':0,
        'Italy':0,
        'Australia':-0.1,
        'Hawaii':-0.3,
        'Chile':-0.4}

countries=[
           'China',
           'India',
           'Japan',
           'Germany',
           'California',
           'UK',
           'Honduras',          
           'Australia',
           'Italy',
           'Spain',
           'Hawaii',
           'Chile']
face_colors={}
markeredgewidth={}
scale=4
for country in countries:#df.index:
    face_colors[country]=colors[country] if country not in ['*China'] else 'None'
    markeredgewidth[country]=0 if country not in ['*China'] else 3
    ax1.scatter(years[0:3], 
             df.loc[country,years][0:3], 
             scale*df.loc[country,'Annual electricity demand (TWh)'],
             #linewidth=0, 
             #linestyle='--', 
             alpha=0.8, 
             #marker='o', 
             color=colors[country],
             #markerfacecolor=face_colors[country],
             #markeredgecolor=colors[country],
             #markeredgewidth=markeredgewidth[country],
             #markersize=scale*df.loc[country,'Annual electricity demand (TWh)'],
             label=country)
    # ax1.plot(years[2], df.loc[country,years][2], linewidth=0, linestyle='--', 
    #          alpha=0.5, marker='o', markerfacecolor=colors[country],
    #          markeredgecolor=colors[country],
    #          markersize=scale*df.loc[country,'Annual electricity demand (TWh)'],
    #          label=country)
    ax1.text(1.2+xpos[country], df.loc[country, '2019']+ ypos[country], country, fontsize=14,
             color=colors[country])
ax1.set_ylabel('Electricity demand covered by solar PV (%)', fontsize=14)    
ax1.grid(color='grey', linestyle='--', axis='y')
ax1.set_xlim(-0.5, 2.5)
ax1.set_ylim(0, 26)
#ax1.legend(fancybox=True, fontsize=16, loc=(0.02,0.4), facecolor='white', frameon=True)

bus_size_factor=10000*scale
handles = make_legend_circles_for([500, 250], 
                                  scale=bus_size_factor, 
                                  facecolor='white',
                                  edgecolor='black')
labels = ["{} TWh".format(s) for s in (500, 250)]
l2 = ax1.legend(handles, labels,
                frameon=True,
                edgecolor='black',
                loc="upper left",                
                bbox_to_anchor=(0.01, 1.01),
                labelspacing=2.,
                borderpad=1.25,
                framealpha=1.,
                #title='Annual demand', prop = {'size':14},
                fontsize=14,
                handler_map=make_handler_map_to_scale_circles_as_in(ax1))
ax1.add_artist(l2)
plt.savefig('figures/pv_penetration.png', dpi=300, bbox_inches='tight')  