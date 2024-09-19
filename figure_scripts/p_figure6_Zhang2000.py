#Make accumulated plot with the original Zhang Gamma_soil = 2000 value

#%% Importing necessary libraries
import sys
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import tqdm as tqdm
import os

# Adding paths to custom scripts
sys.path.extend(['/home/jongenet/jongenet/scripts/a_load_flux_measurements/',
                 '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions',
                 '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo'])
savefig_fp = "/home/jongenet/jongenet/scripts_new/c_papers/c_paper_1/cb_figure_scripts/"
# Importing custom scripts
from pM00_run_models import solleveld_run_MC
from a01_load_solleveld_data import load_solleveld_data
from pF_functions import add_missing_datetime_rows, preprocessing_baserun
savefig_fp = "/home/jongenet/jongenet/scripts_new/c_papers/c_paper_1/cb_figure_scripts/"

# %%2.Initialize measurement and model data, and also run the zhang gamma_g = 2000 data
solleveld_data = load_solleveld_data()

baserun = solleveld_run_MC(MC_switch=False,
                            LAI_scaling=True,
                            LAI_scaling_min=0.5,
                            LAI_scaling_max=1.0,
                            enforce_soil_pathway=False)
zhang2000 = solleveld_run_MC(MC_switch=False,
                            LAI_scaling=True,
                            LAI_scaling_min=0.5,
                            LAI_scaling_max=1.0,
                            enforce_soil_pathway=False,
                            run_DEPAC = False,
                            run_massad = False,
                            gamma_g_Z_i = 2000)

run_betatemp = solleveld_run_MC(MC_switch=True,
                            LAI_scaling=True,
                            LAI_scaling_min=0.5,
                            LAI_scaling_max=1.0,
                            enforce_soil_pathway=False,
                            add_massad_betaTemp = True,
                            run_massad = False,
                            run_zhang = False)

datetimes = solleveld_data['datetime']
DEPAC_baserun = pd.DataFrame(baserun['DEPAC'], columns=baserun['DEPAC_keys'])
massad_baserun = pd.DataFrame(baserun['massad'], columns=baserun['massad_keys'])
zhang_baserun = pd.DataFrame(baserun['zhang'], columns=baserun['zhang_keys'])
zhang2000 = pd.DataFrame(zhang2000['zhang'], columns=baserun['zhang_keys'])
depac_betatemp = pd.DataFrame(run_betatemp['DEPAC'], columns=baserun['DEPAC_keys'])
u_star_mask = DEPAC_baserun['u_star'] > 0.1

DEPAC_baserun = preprocessing_baserun(DEPAC_baserun, u_star_mask, solleveld_data)
massad_baserun = preprocessing_baserun(massad_baserun, u_star_mask, solleveld_data)
zhang_baserun = preprocessing_baserun(zhang_baserun, u_star_mask, solleveld_data)
zhang2000 = preprocessing_baserun(zhang2000, u_star_mask, solleveld_data)
depac_betatemp = preprocessing_baserun(depac_betatemp, u_star_mask, solleveld_data)
DEPAC_baserun.index = DEPAC_baserun['datetime']
massad_baserun.index = massad_baserun['datetime']
zhang_baserun.index = zhang_baserun['datetime']

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
plt.plot( DEPAC_baserun['cumflux_obs'], label='F$_{tot}$: GRAHAM', color='black')
plt.plot( DEPAC_baserun['cumflux_mod'], label='F$_{tot}$: DEPAC', color = 'tab:blue')
plt.plot( massad_baserun['cumflux_mod'], label='F$_{tot}$: Massad', color='tab:orange')
plt.plot( zhang_baserun['cumflux_mod'], label='F$_{tot}$: Zhang', color='tab:green')
plt.plot( zhang2000['cumflux_mod'], label='F$_{tot}$: Zhang with Γ$_{soil}$ = 2000', color='tab:purple')
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


