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
def linear_regression(x, y):
    # Perform linear regression
    slope, intercept, r, _, _ = linregress(x.dropna(), y.dropna())
    return slope, intercept, r


# %%2.Initialize measurement and model data
DEPAC_baserun = pd.read_json(data_fp+"DEPAC_output.json", orient='records', lines=True)
massad_baserun = pd.read_json(data_fp+"massad_output.json", orient='records', lines=True)
zhang_baserun = pd.read_json(data_fp+"zhang_output.json", orient='records', lines=True)
model_dict = {"DEPAC" : DEPAC_baserun, "Massad": massad_baserun, "Zhang" : zhang_baserun}

#%%Make monthly averaged figure
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

#Plot figure
fig, ax = plt.subplots(1, 3, figsize=(3*4, 4*1), sharey=True)

offset = 0.2  # Offset for the observed boxplots

for i, (model_name, model) in enumerate(model_dict.items()):
    # Group by month and collect flux_tot and NH3_flux_obs data, dropping NaN values
    month_data_mod = model[['flux_tot', 'month']].dropna().groupby('month')['flux_tot'].apply(list)
    month_data_obs = model[['NH3_flux_obs', 'month']].dropna().groupby('month')['NH3_flux_obs'].apply(list)
    
    # Get the months that have data
    months_mod = month_data_mod.index
    months_obs = month_data_obs.index

    # Plot boxplots for modeled data
    bp_mod = ax[i].boxplot([month_data_mod[m] for m in months_mod], positions=months_mod, patch_artist=True,
                           boxprops=dict(facecolor='tab:blue', alpha=0.5),
                           medianprops=dict(color='tab:blue'),
                           whiskerprops=dict(color='tab:blue'),
                           capprops=dict(color='tab:blue'),
                           showfliers=False)

    # Plot boxplots for observed data, with an offset
    bp_obs = ax[i].boxplot([month_data_obs[m] for m in months_obs], positions=months_obs, patch_artist=True,
                           boxprops=dict(facecolor='tab:orange', alpha=0.5),
                           medianprops=dict(color='tab:orange'),
                           capprops=dict(color='tab:orange'),
                           whiskerprops=dict(color='tab:orange'),
                           showfliers=False)

    # Additional layout
    ax[i].grid(alpha=grid_alpha)
    ax[i].set_xticks(range(1, 13))
    ax[i].set_xticklabels(range(1, 13))
    ax[i].set_title(model_name, **subplot_title_config)
    ax[i].set_xlabel("Month", fontsize=label_font)

ax[0].set_ylabel("Flux in ng m$^{-2}$ s$^{-1}$")

# Add legend
handles = [bp_mod["boxes"][0], bp_obs["boxes"][0]]
labels = ['Modelled $F_{tot}$', 'Observed $F_{tot}$']
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.54, -0.07), ncol=2)

# Add axis labels
labels1 = ['a)', 'b)', 'c)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.98, labels1[i], transform=axi.transAxes, **abclabel_config)

plt.tight_layout()
plt.savefig(f"{savefig_fp}fig04.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}fig04.png", format='png', dpi=800, bbox_inches='tight')
plt.show()

# %%
