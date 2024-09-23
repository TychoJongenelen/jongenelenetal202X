#%% Importing necessary libraries
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


#%% Importing necessary libraries
import numpy as np
import pandas as pd
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
model_dict = {"DEPAC" : DEPAC_baserun, "Massad": massad_baserun, "Zhang" : zhang_baserun}


#%%Make detailed plot
varnames_dct = {'DEPAC': ['flux_tot', 'flux_stom', 'flux_w','hour', 'conc', 'canopy_comp_point', \
                          'ext_comp_point', 'stom_comp_point', 'gamma_stom', 'gamma_w', 'r_s', \
                            'r_w', 'month'],
                'Massad': ['flux_tot', 'flux_stom', 'flux_w','hour', 'conc', 'chi_c', \
                           'chi_stom', 'gamma_stom', 'r_s', 'r_w', 'month'],
                'Zhang' : ['flux_tot', 'flux_stom', 'flux_w', 'flux_soil', 'hour', 'conc', 'chi_c', \
                           'chi_stom', 'chi_soil', 'gamma_stom', 'gamma_soil', 'r_s', 'r_w', 'r_soil_eff', 'month']}
model_varnames = {'chi_c': ['canopy_comp_point', 'chi_c', 'chi_c'],
                  'chi_stom': ['stom_comp_point', 'chi_stom', 'chi_stom']
    }

color_ftot = 'tab:blue'
color_fs = 'tab:orange'
color_fw = 'tab:green'
color_fsoil = 'tab:brown'

#Standard font sizes
title_font = 14
label_font = 10
legend_font = 11
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

#Plot the figure
# Set up the figure and axes for a 3x3 grid of plots
factor= 1
fig, ax = plt.subplots(3, 3, figsize=(12*factor, 9*factor), sharey='row')

# Iterate over models in the model_dict
for i, (model_name, model) in enumerate(model_dict.items()):
    # Calculate mean and quantiles for model and observations
    hour_mean_mod = model[varnames_dct[model_name]].groupby('hour').mean()
    hour_mean_mod_25 = model[varnames_dct[model_name]].groupby('hour').quantile(0.25)['flux_tot']
    hour_mean_mod_75 = model[varnames_dct[model_name]].groupby('hour').quantile(0.75)['flux_tot']
    hour_mean_obs = model[['NH3_flux_obs', 'hour']].groupby('hour').mean()
    hour_mean_obs_25 = model[['NH3_flux_obs', 'hour']].groupby('hour').quantile(0.25)['NH3_flux_obs']
    hour_mean_obs_75 = model[['NH3_flux_obs', 'hour']].groupby('hour').quantile(0.75)['NH3_flux_obs']
    
    # Row one: Plot fluxes
    ax[0, i].plot(hour_mean_mod.index, hour_mean_mod['flux_tot'], label="F$_{tot}$", color=color_ftot)
    ax[0, i].plot(hour_mean_mod.index, hour_mean_mod['flux_stom'], label="F$_{s}$", color=color_fs)
    ax[0, i].plot(hour_mean_mod.index, hour_mean_mod['flux_w'], label="F$_{w}$", color=color_fw)
    if model_name == 'Zhang':
        hour_mean_mod_soil = model[['flux_soil', 'hour']].groupby('hour').mean()
        ax[0, i].plot(hour_mean_mod.index, hour_mean_mod_soil['flux_soil'], label="F$_{soil}$", color=color_fsoil)

    # Additional layout for row 1
    ax[0, i].grid(alpha=grid_alpha)
    ax[0, i].set_xticks(hour_mean_mod.index[::3])
    ax[0, i].set_yticks(np.arange(-25, 5.0, 5))
    ax[0, i].set_title(model_name, **subplot_title_config)
    ax[0, i].axhline(y=0, alpha=0.2, color='black')

    # Row two: Plot compensation points
    ax[1, i].plot(hour_mean_obs.index, hour_mean_mod['conc'], label='χ$_{a}$', color='tab:blue')
    ax[1, i].plot(hour_mean_mod.index, hour_mean_mod[model_varnames['chi_stom'][i]], label='χ$_{s}$', color=color_fs)
    ax[1, i].plot(hour_mean_obs.index, hour_mean_mod[model_varnames['chi_c'][i]], label='χ$_{c}$', color='black')
    if model_name == "DEPAC":
        ax[1, i].plot(hour_mean_mod.index, hour_mean_mod['ext_comp_point'], color=color_fw, label='χ$_{w}$')
    if model_name == "Zhang":
        ax[1, i].plot(hour_mean_mod.index, hour_mean_mod['chi_soil'], color=color_fsoil, label='χ$_{soil}$')

    # Additional layout for row 2
    ax[1, i].grid(alpha=grid_alpha)
    ax[1, i].set_xticks(hour_mean_mod.index[::3])
    ax[1, i].set_yticks(np.arange(0, 2.5, 0.5))
    ax[1, i].axhline(y=0, alpha=0.2, color='black')

    # Row three: Plot resistances as conductance
    filtered_rs = model[['r_s', 'hour']].replace([np.inf, -np.inf], np.nan).dropna()
    filtered_rs = filtered_rs.groupby('hour').mean()
    ax[2, i].plot(filtered_rs.index, 1/filtered_rs, label="G$_{s}$", color=color_fs)
    ax[2, i].plot(hour_mean_mod.index, 1/hour_mean_mod['r_w'], label="G$_{w}$", color=color_fw)
    if model_name == "Zhang":
        ax[2, i].plot(hour_mean_mod.index, 1/hour_mean_mod['r_soil_eff'], label="G$_{soil}$", color=color_fsoil)

    # Additional layout for row 3
    ax[2, i].grid(alpha=grid_alpha)
    ax[2, i].set_xticks(hour_mean_mod.index[::3])
    ax[2, i].set_yscale('log')
    ax[2, i].set_yticks(np.logspace(-6, 0, num=7))
    ax[2, i].set_ylim(1e-6, 1e0)
    ax[2, i].set_xlabel("Hour (UTC)")

# Row 1: Set ylabel for the first column and adjust legend
ax[0, 0].set_ylabel("Flux in ng m$^{-2}$ s$^{-1}$", fontsize=label_font)
ax[0, 2].legend(bbox_to_anchor=(1, 1), ncol=1, fontsize=legend_font)

# Row 2: Set ylabel for the first column and adjust legend
ax[1, 0].set_ylabel("Concentration in μg m$^{-3}$", fontsize=label_font) 
handles, labels = ax[1, 2].get_legend_handles_labels()
# Reorder and update handles and labels
handles[1], handles[2] = handles[2], handles[1]
labels[1], labels[2] = labels[2], labels[1]
labels.append(labels[1])
handles.append(handles[1])
labels[4], labels[3] = labels[3], '$χ_{w}$'
new_handle3 = plt.Line2D([], [], color=color_fsoil, label=labels[4])
new_handle2 = plt.Line2D([], [], color=color_fw, label=labels[3])
handles[3] = new_handle2
handles[4] = new_handle3
ax[1, 2].legend(handles, labels, bbox_to_anchor=(1, 1), fontsize=legend_font)

# Row 3: Set ylabel for the first column and adjust legend
ax[2, 0].set_ylabel("Conductance in m s$^{-1}$", fontsize=label_font)
ax[2, 2].legend(bbox_to_anchor=(1.32, 1), ncol=1, fontsize=legend_font)

# Add subfigure labels (a), (b), etc.
labels = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)', 'g)', 'h)', 'i)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.98, labels[i], transform=axi.transAxes, **abclabel_config)

# Final layout adjustments
plt.tight_layout()
plt.savefig(f"{savefig_fp}fig05.pdf", format='pdf', dpi=300)
plt.savefig(f"{savefig_fp}fig05.png", format='png', dpi=800)
plt.show()



# %%
