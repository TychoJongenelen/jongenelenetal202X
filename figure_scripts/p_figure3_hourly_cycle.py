#%%1. Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set `directory_name` to the absolute path of your `/figure_scripts/` directory.
# Example: directory_name = "/path/to/your/project/figure_scripts/"
directory_name = ""
if directory_name == "":
    raise ValueError("Please specify the directory_name variable ")
else:
    os.chdir(directory_name)
    
savefig_fp = "../figures/"
data_fp = "../model_output/"

#%%2.Initialize measurement and model data
models = ['DEPAC', 'massad', 'zhang']
baseruns = {}

for model in models:
    baseruns[model] = pd.read_json(f"{data_fp}{model}_output.json", orient='records', lines=True, convert_dates=False)
    baseruns[model]['datetime'] = pd.to_datetime(baseruns[model]['datetime'], unit='ms')
    baseruns[model].set_index('datetime', inplace=True)

# Access individual datasets:
DEPAC_baserun = baseruns['DEPAC']
massad_baserun = baseruns['massad']
zhang_baserun = baseruns['zhang']

model_dict = {"DEPAC" : DEPAC_baserun, "Massad": massad_baserun, "Zhang" : zhang_baserun}

#%%3. Make hourly averaged figure
label_fontsize = 9
legend_fontsize = 10 #Changed here
title_fontsize = 11
grid_alpha = 0.3

y_label = r"$\text{F}_{\text{tot}}$ (ng m$^{-2}$ s$^{-1}$)"
mod_label = r"$\text{F}_{\text{tot, mod}}$"
obs_label = r"$\text{F}_{\text{tot, obs}}$"


fig, ax = plt.subplots(1, 3, figsize=(7.3, 2.5), sharey=True)

for i, (model_name, model) in enumerate(model_dict.items()):
    # Calculate hourly averaged mod and obs + IQR
    hour_mean_mod = model[['flux_tot', 'hour']].groupby('hour').mean()
    hour_mean_mod_25 = model[['flux_tot', 'hour']].groupby('hour').quantile(0.25)['flux_tot']
    hour_mean_mod_75 = model[['flux_tot', 'hour']].groupby('hour').quantile(0.75)['flux_tot']
    hour_mean_obs = model[['NH3_flux_obs', 'hour']].groupby('hour').mean()
    hour_mean_obs_25 = model[['NH3_flux_obs', 'hour']].groupby('hour').quantile(0.25)['NH3_flux_obs']
    hour_mean_obs_75 = model[['NH3_flux_obs', 'hour']].groupby('hour').quantile(0.75)['NH3_flux_obs']
    
    # Plot model and observed data with IQR shading
    ax[i].plot(hour_mean_mod.index, hour_mean_mod, color='tab:blue', label= mod_label, linewidth=2)
    ax[i].plot(hour_mean_obs.index, hour_mean_obs, color='tab:orange', label= obs_label, linewidth=2)
    ax[i].fill_between(hour_mean_mod.index, y1=hour_mean_mod_25, y2=hour_mean_mod_75, color='tab:blue', alpha=0.3, zorder=3)
    ax[i].fill_between(hour_mean_mod.index, y1=hour_mean_obs_25, y2=hour_mean_obs_75, color='tab:orange', alpha=0.3, zorder=3)
    
    # Additional layout improvements
    ax[i].grid(alpha=grid_alpha)
    ax[i].set_xticks(hour_mean_mod.index[::3])
    ax[i].set_title(model_name, fontsize=title_fontsize, fontweight='bold')
    ax[i].set_xlabel("Hour (UTC+1)", fontsize=label_fontsize)
    ax[i].tick_params(axis='both', which='major', labelsize=label_fontsize)
    ax[i].set_xlim(0,23)

# Add y-label
ax[0].set_ylabel(y_label, fontsize=label_fontsize)

# Consolidate legend into a single, centralized legend
handles, labels = ax[2].get_legend_handles_labels()
legend = fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.55, -0.10), ncol=2, fontsize=legend_fontsize)

# Add subplot labels
labels = ['a)', 'b)', 'c)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.90, labels[i], transform=axi.transAxes, fontsize=label_fontsize)

# Adjust layout to prevent overlap
plt.tight_layout()
plt.savefig(f"{savefig_fp}fig03.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}fig03.png", format='png', dpi=300, bbox_inches='tight')
plt.show()



# %%
