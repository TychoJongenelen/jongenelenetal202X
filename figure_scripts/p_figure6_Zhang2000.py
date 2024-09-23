#%% Importing necessary libraries
import numpy as np
import pandas as pd
from scipy.stats import linregress

import matplotlib.pyplot as plt
import os
#Change to your desired directory:
os.chdir('/home/jongenet/jongenelenetal202X/figure_scripts/')

savefig_fp = "../figures/"
data_fp = "../model_output/"


# %%2.Initialize measurement and model data
DEPAC_baserun = pd.read_json(data_fp+"DEPAC_output.json", orient='records', lines=True)
massad_baserun = pd.read_json(data_fp+"massad_output.json", orient='records', lines=True)
zhang_baserun = pd.read_json(data_fp+"zhang_output.json", orient='records', lines=True)
zhang2000 = pd.read_json(data_fp+"zhang_original_output.json", orient='records', lines=True)

DEPAC_baserun.index = DEPAC_baserun['datetime']
massad_baserun.index = massad_baserun['datetime']
zhang_baserun.index = zhang_baserun['datetime']
zhang2000.index = zhang2000['datetime']


#%%3. Plot accumulated fluxes (without MC uncertainty range)
import matplotlib.dates as mdates
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
fig, ax = plt.subplots(1, figsize=(12,6))
plt.plot(DEPAC_baserun['cumflux_obs'], label='F$_{tot}$: GRAHAM', color='black')
plt.plot(DEPAC_baserun['cumflux_mod'], label='F$_{tot}$: DEPAC', color = 'tab:blue')
plt.plot(massad_baserun['cumflux_mod'], label='F$_{tot}$: Massad', color='tab:orange')
plt.plot(zhang_baserun['cumflux_mod'], label='F$_{tot}$: Zhang', color='tab:green')
plt.plot(zhang2000['cumflux_mod'], label='F$_{tot}$: Zhang with Γ$_{soil}$ = 2000', color='tab:purple')
plt.ylabel("Σ NH$_{3}$ in kg ha$^{-1}$")
plt.legend(loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.2), fontsize=legend_font)

#Fix the months
# Format the x-axis to show month and year
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Locator for each month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')) 
plt.ylim(-1.5, 0.5)
plt.yticks(np.arange(-1.5, 0.75, step=0.25))
plt.grid(alpha=grid_alpha)
plt.tight_layout()
plt.savefig(f"{savefig_fp}fig06.pdf", format='pdf', dpi=300)
plt.savefig(f"{savefig_fp}fig06.png", format='png', dpi=800)
plt.show()



# %%
