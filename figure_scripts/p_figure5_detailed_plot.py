#%% Importing necessary libraries
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

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


#%%Make detailed plot
#Some models use different names for variables, that has to be dealt with when making the plot
varnames_dct = {
    'DEPAC': ['flux_tot', 'flux_stom', 'flux_w', 'hour', 'NH3_conc', 'canopy_comp_point',
              'ext_comp_point', 'stom_comp_point', 'gamma_stom', 'gamma_w', 'r_s', 'r_w', 'month'],
    'Massad': ['flux_tot', 'flux_stom', 'flux_w', 'hour', 'NH3_conc', 'chi_z0',
               'chi_stom', 'gamma_stom', 'r_s', 'r_w', 'month'],
    'Zhang': ['flux_tot', 'flux_stom', 'flux_w', 'flux_soil', 'hour', 'NH3_conc', 'chi_c',
              'chi_stom', 'chi_soil', 'gamma_stom', 'gamma_soil', 'r_s', 'r_w', 'r_soil_eff', 'month']
}

# Define equivalent variable names across models
model_varnames = {
    'chi_c': ['canopy_comp_point', 'chi_z0', 'chi_c'],
    'chi_stom': ['stom_comp_point', 'chi_stom', 'chi_stom']
}

# Store model datasets in a dictionary
model_dict = {"DEPAC": DEPAC_baserun, "Massad": massad_baserun, "Zhang": zhang_baserun}

# Keeping the colors exactly as they were
color_ftot = 'tab:blue'
color_fs = 'tab:green'
color_fw = 'tab:orange'
color_fsoil = 'tab:brown'

# Standard font sizes 
label_fontsize = 9
legend_fontsize = 9
title_fontsize = 11
grid_alpha = 0.3
offset = 0.2  # Offset for the observed boxplots

fig, ax = plt.subplots(3, 3, figsize=(7.3, 5.8), sharey='row')

# Iterate over models to generate plots
for i, (model_name, model) in enumerate(model_dict.items()):
    
    # Calculate mean and quantiles for model and observations
    hour_mean_mod = model[varnames_dct[model_name]].groupby('hour').mean()
    hour_mean_obs = model[['NH3_flux_obs', 'hour']].groupby('hour').mean()

    # Row 1: Plot NH₃ fluxes
    ax[0, i].plot(hour_mean_mod.index, hour_mean_mod['flux_tot'], label="F$_{tot}$", color=color_ftot)
    ax[0, i].plot(hour_mean_mod.index, hour_mean_mod['flux_stom'], label="F$_{s}$", color=color_fs)
    ax[0, i].plot(hour_mean_mod.index, hour_mean_mod['flux_w'], label="F$_{w}$", color=color_fw)

    # Add soil flux graph of Zhang scheme
    if model_name == 'Zhang':
        hour_mean_mod_soil = model[['flux_soil', 'hour']].groupby('hour').mean()
        ax[0, i].plot(hour_mean_mod.index, hour_mean_mod_soil['flux_soil'], label="F$_{soil}$", color=color_fsoil)

    ax[0, i].grid(alpha=grid_alpha)
    ax[0, i].set_xticks(hour_mean_mod.index[::3])
    ax[0, i].set_xlim(0, 23)
    ax[0, i].set_yticks(np.arange(-25, 5.0, 5))
    ax[0, i].set_title(model_name, fontsize=title_fontsize, fontweight='bold')
    ax[0, i].axhline(y=0, alpha=0.2, color='black')
    ax[0, i].tick_params(axis='both', labelsize=label_fontsize)

    # Row 2: Plot compensation points
    ax[1, i].plot(hour_mean_obs.index, hour_mean_mod['NH3_conc'], label='χ$_{a}$', color='tab:blue')
    ax[1, i].plot(hour_mean_mod.index, hour_mean_mod[model_varnames['chi_stom'][i]], label='χ$_{s}$', color=color_fs)
    ax[1, i].plot(hour_mean_obs.index, hour_mean_mod[model_varnames['chi_c'][i]], label='χ$_{c}$', color='black')

    # Plot scheme-unique compensation points for DEPAC and Zhang scheme
    if model_name == "DEPAC":
        ax[1, i].plot(hour_mean_mod.index, hour_mean_mod['ext_comp_point'], color=color_fw, label='χ$_{w}$')
    if model_name == "Zhang":
        ax[1, i].plot(hour_mean_mod.index, hour_mean_mod['chi_soil'], color=color_fsoil, label='χ$_{soil}$')

    ax[1, i].grid(alpha=grid_alpha)
    ax[1, i].set_xticks(hour_mean_mod.index[::3])
    ax[1, i].set_xlim(0, 23)
    ax[1, i].set_yticks(np.arange(0, 2.5, 0.5))
    ax[1, i].axhline(y=0, alpha=0.2, color='black')
    ax[1, i].tick_params(axis='both', labelsize=label_fontsize)

    # Row 3: Plot resistances as conductance
    filtered_rs = model[['r_s', 'hour']].replace([np.inf, -np.inf, 1e25], np.nan).dropna().groupby('hour').mean()
    ax[2, i].plot(filtered_rs.index, 1 / filtered_rs, label="G$_{s}$", color=color_fs)
    ax[2, i].plot(hour_mean_mod.index, 1 / hour_mean_mod['r_w'], label="G$_{w}$", color=color_fw)

    if model_name == "Zhang":
        ax[2, i].plot(hour_mean_mod.index, 1 / hour_mean_mod['r_soil_eff'], label="G$_{soil}$", color=color_fsoil)

    ax[2, i].grid(alpha=grid_alpha)
    ax[2, i].set_xlim(0, 23)
    ax[2, i].set_xticks(hour_mean_mod.index[::3])
    ax[2, i].set_yscale('log')
    ax[2, i].set_yticks(np.logspace(-7, -1, num=7))
    ax[2, i].set_ylim(1e-7, 1e-1)
    ax[2, i].set_xlabel("Hour (UTC+1)", fontsize=label_fontsize)
    ax[2, i].tick_params(axis='both', labelsize=label_fontsize)

# Configure labels, legends, and layout
ax[0, 0].set_ylabel("Flux (ng m$^{-2}$ s$^{-1}$)", fontsize=label_fontsize)
ax[1, 0].set_ylabel("Concentration (μg m$^{-3}$)", fontsize=label_fontsize)
ax[2, 0].set_ylabel("Conductance (m s$^{-1}$)", fontsize=label_fontsize)

ax[0, 2].legend(bbox_to_anchor=(1, 1.05), fontsize=legend_fontsize)
ax[2, 2].legend(bbox_to_anchor=(1, 1.05), fontsize=legend_fontsize)

# Add subfigure labels (a, b, ...)
for i, axi in enumerate(ax.flat):
    axi.text(0.03, 0.90, f"{chr(97 + i)})", transform=axi.transAxes, fontsize=label_fontsize)

plt.tight_layout()
plt.savefig(f"{savefig_fp}fig05.pdf", format='pdf', dpi=300)
plt.savefig(f"{savefig_fp}fig05.png", format='png', dpi=300)
plt.show()

# %%
