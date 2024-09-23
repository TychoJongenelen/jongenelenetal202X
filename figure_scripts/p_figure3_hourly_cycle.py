#%% Importing necessary libraries
import numpy as np
import pandas as pd
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

#%%Make hourly averaged figure
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

fig, ax = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

for i, (model_name, model) in enumerate(model_dict.items()):
    # Calculate hourly averaged mod and obs + IQR
    hour_mean_mod = model[['flux_tot', 'hour']].groupby('hour').mean()
    hour_mean_mod_25 = model[['flux_tot', 'hour']].groupby('hour').quantile(0.25)['flux_tot']
    hour_mean_mod_75 = model[['flux_tot', 'hour']].groupby('hour').quantile(0.75)['flux_tot']
    hour_mean_obs = model[['NH3_flux_obs', 'hour']].groupby('hour').mean()
    hour_mean_obs_25 = model[['NH3_flux_obs', 'hour']].groupby('hour').quantile(0.25)['NH3_flux_obs']
    hour_mean_obs_75 = model[['NH3_flux_obs', 'hour']].groupby('hour').quantile(0.75)['NH3_flux_obs']
    
    # Plot model and observed data with IQR shading
    ax[i].plot(hour_mean_mod.index, hour_mean_mod, color='tab:blue', label='Modeled $F_{tot}$', linewidth=2)
    ax[i].plot(hour_mean_obs.index, hour_mean_obs, color='tab:orange', label='Observed $F_{tot}$', linewidth=2)
    ax[i].fill_between(hour_mean_mod.index, y1=hour_mean_mod_25, y2=hour_mean_mod_75, color='tab:blue', alpha=0.3, zorder=3)
    ax[i].fill_between(hour_mean_mod.index, y1=hour_mean_obs_25, y2=hour_mean_obs_75, color='tab:orange', alpha=0.3, zorder=3)
    
    # Additional layout improvements
    ax[i].grid(alpha=grid_alpha)
    ax[i].set_xticks(hour_mean_mod.index[::3])
    ax[i].set_title(model_name, **subplot_title_config)
    ax[i].set_xlabel("Hour (UTC)", fontsize=label_font)
    ax[i].tick_params(axis='both', which='major', labelsize=10)

ax[0].set_ylabel("Flux in ng m$^{-2}$ s$^{-1}$", fontsize=label_font)

# Consolidate legend into a single, centralized legend
handles, labels = ax[2].get_legend_handles_labels()
legend = fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize=legend_font)

# Add subplot labels
labels = ['a)', 'b)', 'c)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.98, labels[i], transform=axi.transAxes, **abclabel_config)

# Adjust layout to prevent overlap
plt.tight_layout(pad=2.5)
plt.savefig(f"{savefig_fp}fig03.pdf", format='pdf', dpi=300, bbox_extra_artists=(legend,), bbox_inches='tight')
plt.savefig(f"{savefig_fp}fig03.png", format='png', dpi=800, bbox_extra_artists=(legend,), bbox_inches='tight')
plt.show()



# %%
