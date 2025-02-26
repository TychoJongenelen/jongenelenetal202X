#%% Importing necessary libraries
import pandas as pd
from scipy.stats import linregress
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

def linear_regression(x, y):
    # Perform linear regression
    slope, intercept, r, _, _ = linregress(x.dropna(), y.dropna())
    return slope, intercept, r


# %%2.Initialize measurement and model data
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

#%%Make monthly averaged figure
label_fontsize = 9
legend_fontsize = 9
title_fontsize = 11
grid_alpha = 0.3
offset = 0.2  # Offset for the observed boxplots

y_label = r"$\text{F}_{\text{tot}}$ (ng m$^{-2}$ s$^{-1}$)"
mod_label = r"$\text{F}_{\text{tot, mod}}$"
obs_label = r"$\text{F}_{\text{tot, obs}}$"

fig, ax = plt.subplots(1, 3, figsize=(7.3, 2.5), sharey=True)

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
    ax[i].set_title(model_name, fontsize=title_fontsize, fontweight='bold')
    ax[i].set_xlabel("Month", fontsize=label_fontsize)
    ax[i].tick_params(axis='both', which='major', labelsize=label_fontsize)

ax[0].set_ylabel(y_label, fontsize=label_fontsize)

# Add legend
handles = [bp_mod["boxes"][0], bp_obs["boxes"][0]]
labels = [mod_label, obs_label]
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.55, -0.10), ncol=2)

# Add subplot labels
labels = ['a)', 'b)', 'c)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.90, labels[i], transform=axi.transAxes, fontsize=label_fontsize)

plt.tight_layout()
plt.savefig(f"{savefig_fp}fig04.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}fig04.png", format='png', dpi=300, bbox_inches='tight')
plt.show()

# %%
