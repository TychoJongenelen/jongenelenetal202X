
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
DEPAC_baserun.index = DEPAC_baserun['datetime']
massad_baserun.index = massad_baserun['datetime']
zhang_baserun.index = zhang_baserun['datetime']

#%%Code to make accumulated fluxes plot with uncertainty ranges


#Load the Monte Carlo simulation data
filepath = "/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo/data/MC_results/"
DEPAC_mc_mean = pd.read_csv(filepath + "DEPAC_mc_mean" + ".csv")
DEPAC_mc_std = pd.read_csv(filepath + "DEPAC_mc_std" + ".csv")
DEPAC_mc_025 = pd.read_csv(filepath + "DEPAC_mc_025" + ".csv")
DEPAC_mc_975 = pd.read_csv(filepath + "DEPAC_mc_975" + ".csv")
massad_mc_mean = pd.read_csv(filepath + "massad_mc_mean" + ".csv")
massad_mc_std = pd.read_csv(filepath + "massad_mc_std" + ".csv")
massad_mc_025 = pd.read_csv(filepath + "massad_mc_025" + ".csv")
massad_mc_975 = pd.read_csv(filepath + "massad_mc_975" + ".csv")
zhang_mc_mean = pd.read_csv(filepath + "zhang_mc_mean" + ".csv")
zhang_mc_std = pd.read_csv(filepath + "zhang_mc_std" + ".csv")
zhang_mc_025 = pd.read_csv(filepath + "zhang_mc_025" + ".csv")
zhang_mc_975 = pd.read_csv(filepath + "zhang_mc_975" + ".csv")

dataframes = {'DEPAC_baserun': DEPAC_baserun, 
            'massad_baserun': massad_baserun, 
            'zhang_baserun': zhang_baserun, 
            'DEPAC_mc_mean': DEPAC_mc_mean, 
            'massad_mc_mean': massad_mc_mean, 
            'zhang_mc_mean': zhang_mc_mean, 
            'DEPAC_mc_std': DEPAC_mc_std, 
            'massad_mc_std': massad_mc_std, 
            'zhang_mc_std': zhang_mc_std,
            'DEPAC_mc_025' : DEPAC_mc_025,
            'DEPAC_mc_975' : DEPAC_mc_975,
            'massad_mc_025' : massad_mc_025,
            'massad_mc_975' : massad_mc_975,
            'zhang_mc_025' : zhang_mc_025,
            'zhang_mc_975' : zhang_mc_975,
            }

#Preprocess the runs, some runs are already preprocessed, hence the try-except.
for name, df in dataframes.items():
    try:
        dataframes[name] = preprocessing_baserun(df, u_star_mask, solleveld_data)
    except:
        pass

#Has to be done again for some reason
dataframes['DEPAC_baserun'].index = DEPAC_baserun['datetime']
dataframes['massad_baserun'].index = massad_baserun['datetime']
dataframes['zhang_baserun'].index = zhang_baserun['datetime']




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

DEPAC_acc = dataframes['DEPAC_baserun']['cumflux_mod'][-1]
massad_acc = dataframes['massad_baserun']['cumflux_mod'][-1]
zhang_acc = dataframes['zhang_baserun']['cumflux_mod'][-1]


yerr_DEPAC = [abs(DEPAC_acc-[dataframes['DEPAC_mc_025']['cumflux_mod'][-1]]), abs(DEPAC_acc-[dataframes['DEPAC_mc_975']['cumflux_mod'][-1]])]
yerr_massad = [abs(massad_acc - [dataframes['massad_mc_025']['cumflux_mod'][-1]]), abs(massad_acc - [dataframes['massad_mc_975']['cumflux_mod'][-1]])]
yerr_zhang = [abs(zhang_acc - [dataframes['zhang_mc_025']['cumflux_mod'][-1]]), abs(zhang_acc - [dataframes['zhang_mc_975']['cumflux_mod'][-1]])]


fig, ax = plt.subplots(1, figsize=(12,6))

#OBS
plt.plot(dataframes['DEPAC_baserun'].index, 
              dataframes['DEPAC_baserun']['cumflux_obs'], 
              color='black', label='F$_{tot}$: GRAHAM')

plt.errorbar(dataframes['DEPAC_baserun'].index[-1],
                  y=dataframes['DEPAC_baserun']['cumflux_obs'][-1],
                  yerr=abs(dataframes['DEPAC_baserun']['cumflux_obs'][-1]*error_GRAHAM), color='black', 
                  linewidth=2, capsize=5, fmt='o', markersize=5)
#DEPAC
ax= plt.plot(dataframes['DEPAC_baserun'].index,
            dataframes['DEPAC_baserun']['cumflux_mod'], label='F$_{tot}$: DEPAC')
plt.errorbar(dataframes['DEPAC_baserun'].index[-1] + offset,
                  y=dataframes['DEPAC_baserun']['cumflux_mod'][-1],
                  yerr=yerr_DEPAC, color='tab:blue', linewidth=2, capsize=5, fmt='o', markersize=5)

#MASSAD
plt.plot(dataframes['DEPAC_baserun'].index, dataframes['massad_baserun']['cumflux_mod'], label='F$_{tot}$: Massad')
plt.errorbar(dataframes['massad_baserun'].index[-1] + offset*2,
                  y=dataframes['massad_baserun']['cumflux_mod'][-1],
                  yerr=yerr_massad, color='tab:orange', linewidth=2, capsize=5,
                  fmt='o', markersize=5)

#ZHANG
plt.plot(dataframes['DEPAC_baserun'].index, dataframes['zhang_baserun']['cumflux_mod'], label='F$_{tot}$: Zhang')
plt.errorbar(dataframes['zhang_baserun'].index[-1] + offset*3,
                  y=dataframes['zhang_baserun']['cumflux_mod'][-1],
                  yerr=yerr_zhang, color='tab:green', linewidth=2, capsize=5,
                  fmt='o', markersize=5)


months = pd.date_range(start=dataframes['DEPAC_baserun'].index.min(), end=dataframes['DEPAC_baserun'].index.max(), freq='M')
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
