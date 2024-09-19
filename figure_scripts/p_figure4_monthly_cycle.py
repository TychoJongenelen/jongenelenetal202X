#%% Importing necessary libraries
import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# Adding paths to custom scripts
sys.path.extend(['/home/jongenet/jongenet/scripts/a_load_flux_measurements/',
                 '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions',
                 '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo'])

# Importing custom scripts
from pM00_run_models import solleveld_run_MC
from a01_load_solleveld_data import load_solleveld_data
from pF_functions import add_missing_datetime_rows, preprocessing_baserun
savefig_fp = "/home/jongenet/jongenet/scripts_new/c_papers/c_paper_1/cb_figure_scripts/"

# %%2.Initialize measurement and model data
solleveld_data = load_solleveld_data()

baserun = solleveld_run_MC(MC_switch=False,
                            LAI_scaling=True,
                            LAI_scaling_min=0.5,
                            LAI_scaling_max=1.0,
                            enforce_soil_pathway=False)

datetimes = solleveld_data['datetime']
DEPAC_baserun = pd.DataFrame(baserun['DEPAC'], columns=baserun['DEPAC_keys'])
massad_baserun = pd.DataFrame(baserun['massad'], columns=baserun['massad_keys'])
zhang_baserun = pd.DataFrame(baserun['zhang'], columns=baserun['zhang_keys'])
u_star_mask = DEPAC_baserun['u_star'] > 0.1

DEPAC_baserun = preprocessing_baserun(DEPAC_baserun, u_star_mask, solleveld_data)
massad_baserun = preprocessing_baserun(massad_baserun, u_star_mask, solleveld_data)
zhang_baserun = preprocessing_baserun(zhang_baserun, u_star_mask, solleveld_data)
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
