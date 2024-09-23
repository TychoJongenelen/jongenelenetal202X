#%% Importing necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

import os
#Change to your desired directory:
os.chdir('/home/jongenet/jongenelenetal202X/figure_scripts/')

savefig_fp = "../figures/"
data_fp = "../model_output/"


# %%2.Initialize measurement and model data
DEPAC_baserun = pd.read_json(data_fp+"DEPAC_output.json", orient='records', lines=True)
massad_baserun = pd.read_json(data_fp+"massad_output.json", orient='records', lines=True)
zhang_baserun = pd.read_json(data_fp+"zhang_output.json", orient='records', lines=True)

DEPAC_mc_025 = pd.read_json("/home/jongenet/jongenelenetal202X/uncertainty_analysis_output/DEPAC_mc_025.json" , orient='records', lines=True)
DEPAC_mc_975 = pd.read_json("/home/jongenet/jongenelenetal202X/uncertainty_analysis_output/DEPAC_mc_975.json" , orient='records', lines=True)
massad_mc_025 = pd.read_json("/home/jongenet/jongenelenetal202X/uncertainty_analysis_output/massad_mc_025.json" , orient='records', lines=True)
massad_mc_975 = pd.read_json("/home/jongenet/jongenelenetal202X/uncertainty_analysis_output/massad_mc_975.json" , orient='records', lines=True)
zhang_mc_025 = pd.read_json("/home/jongenet/jongenelenetal202X/uncertainty_analysis_output/zhang_mc_025.json" , orient='records', lines=True)
zhang_mc_975 = pd.read_json("/home/jongenet/jongenelenetal202X/uncertainty_analysis_output/zhang_mc_975.json" , orient='records', lines=True)

DEPAC_baserun.index = DEPAC_baserun['datetime']
massad_baserun.index = massad_baserun['datetime']
zhang_baserun.index = zhang_baserun['datetime']

#%% Accumulation plot with the error bars
#Standard font sizes
title_font = 14
label_font = 10
legend_font = 10
text_font = 12
grid_alpha = 0.3

hexbinplot_config = {
    'mincnt' :1, 
    'gridsize' : 30, 
    'edgecolor' :'none'
    }
abclabel_config = {
    'fontsize' : text_font,
    'fontweight' : 'bold',
    'verticalalignment' : 'top'
    }

oneline_config = {
    'linestyle' :'--', 
    'linewidth' :1, 
    'label' : '1:1'
    }

legend_config = {
    'loc' : 'upper right',
    'fontsize' : legend_font
    }

subplot_title_config = {
    'fontweight' :'bold', 
    'fontsize' : title_font
    }

from datetime import timedelta
import matplotlib.dates as mdates

error_GRAHAM = 0.24 #Vendel et al. paper (2023)
offset = timedelta(days=5)

DEPAC_acc = DEPAC_baserun['cumflux_mod'][-1]
massad_acc = massad_baserun['cumflux_mod'][-1]
zhang_acc = zhang_baserun['cumflux_mod'][-1]


yerr_DEPAC = np.array([[abs(DEPAC_acc - DEPAC_mc_025.iloc[-1])], 
                       [abs(DEPAC_acc - DEPAC_mc_975.iloc[-1])]]).reshape(2,1)

yerr_massad = np.array([[abs(massad_acc - massad_mc_025.iloc[-1])], 
                        [abs(massad_acc - massad_mc_975.iloc[-1])]]).reshape(2,1)

yerr_zhang = np.array([[abs(zhang_acc - zhang_mc_025.iloc[-1])], 
                       [abs(zhang_acc - zhang_mc_975.iloc[-1])]]).reshape(2,1)


fig, ax = plt.subplots(1, figsize=(12,6))

#OBS
plt.plot(DEPAC_baserun.index, 
              DEPAC_baserun['cumflux_obs'], 
              color='black', label='F$_{tot}$: GRAHAM')

plt.errorbar(DEPAC_baserun.index[-1],
                  y=DEPAC_baserun['cumflux_obs'][-1],
                  yerr=abs(DEPAC_baserun['cumflux_obs'][-1]*error_GRAHAM), color='black', 
                  linewidth=2, capsize=5, fmt='o', markersize=5)
#DEPAC
ax= plt.plot(DEPAC_baserun.index,
            DEPAC_baserun['cumflux_mod'], label='F$_{tot}$: DEPAC')
plt.errorbar(DEPAC_baserun.index[-1] + offset,
                  y=DEPAC_baserun['cumflux_mod'][-1],
                  yerr=yerr_DEPAC, color='tab:blue', linewidth=2, capsize=5, fmt='o', markersize=5)

#MASSAD
plt.plot(DEPAC_baserun.index, massad_baserun['cumflux_mod'], label='F$_{tot}$: Massad')
plt.errorbar(massad_baserun.index[-1] + offset*2,
                  y=massad_baserun['cumflux_mod'][-1],
                  yerr=yerr_massad, color='tab:orange', linewidth=2, capsize=5,
                  fmt='o', markersize=5)

#ZHANG
plt.plot(DEPAC_baserun.index, zhang_baserun['cumflux_mod'], label='F$_{tot}$: Zhang')
plt.errorbar(zhang_baserun.index[-1] + offset*3,
                  y=zhang_baserun['cumflux_mod'][-1],
                  yerr=yerr_zhang, color='tab:green', linewidth=2, capsize=5,
                  fmt='o', markersize=5)


months = pd.date_range(start=DEPAC_baserun.index.min(), end=DEPAC_baserun.index.max(), freq='M')
month_labels = [month.strftime('%b-%Y') for month in months]
plt.legend(loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.25))

#Fix the months
# Format the x-axis to show month and year
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Locator for each month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')) 

plt.xlabel("Date")
plt.ylim(-2.75, 1)
plt.yticks(np.arange(-2.75, 1.0, step=0.25))
plt.ylabel("Σ NH$_{3}$ in kg ha$^{-1}$")
plt.grid(alpha=grid_alpha)

plt.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.2), fontsize=legend_font)
plt.tight_layout()
plt.savefig(f"{savefig_fp}figA01.pdf", format='pdf', dpi=300)
plt.savefig(f"{savefig_fp}figA01.png", format='png', dpi=500)
plt.show()


# %%
