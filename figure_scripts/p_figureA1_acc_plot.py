#%% Importing necessary libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import matplotlib.dates as mdates

# Set `directory_name` to the absolute path of your `/figure_scripts/` directory.
# Example: directory_name = "/path/to/your/project/figure_scripts/"
directory_name = ""
if directory_name == "":
    raise ValueError("Please specify the directory_name variable ")
else:
    os.chdir(directory_name)
    

savefig_fp = "../figures/"
data_fp = "../model_output/"
mc_fp = "../uncertainty_analysis_output/"


# %%2.Initialize measurement and model data
models = ['DEPAC', 'massad', 'zhang', 'zhang_original']
mc_95CI_runs = ['DEPAC_mc_025', 'DEPAC_mc_975', 'massad_mc_025', 'massad_mc_975', 'zhang_mc_025', 'zhang_mc_975']
baseruns = {}
mc_95CI_data = {}

for model in models:
    baseruns[model] = pd.read_json(f"{data_fp}{model}_output.json", orient='records', lines=True, convert_dates=False)
    baseruns[model]['datetime'] = pd.to_datetime(baseruns[model]['datetime'], unit='ms')
    baseruns[model].set_index('datetime', inplace=True)

for mc_run in mc_95CI_runs:
    mc_95CI_data[mc_run] = pd.read_json(f"{mc_fp}{mc_run}.json", orient='records', lines=True, convert_dates=False)
    mc_95CI_data[mc_run]['datetime'] = pd.to_datetime(mc_95CI_data[mc_run]['datetime'], unit='ms')
    mc_95CI_data[mc_run].set_index('datetime', inplace=True) 
    
# Access individual datasets:
DEPAC_baserun = baseruns['DEPAC']
massad_baserun = baseruns['massad']
zhang_baserun = baseruns['zhang']
zhang_original = baseruns['zhang_original']

# Access 2.5 and 97.5% percentile data to compute 95% CI
DEPAC_mc_025  = mc_95CI_data['DEPAC_mc_025']
DEPAC_mc_975  = mc_95CI_data['DEPAC_mc_975']
massad_mc_025 = mc_95CI_data['massad_mc_025']
massad_mc_975 = mc_95CI_data['massad_mc_975']
zhang_mc_025  = mc_95CI_data['zhang_mc_025']
zhang_mc_975  = mc_95CI_data['zhang_mc_975']

dataframes = {'DEPAC_baserun': DEPAC_baserun, 
            'massad_baserun': massad_baserun, 
            'zhang_baserun': zhang_baserun, 
            'DEPAC_mc_025' : DEPAC_mc_025,
            'DEPAC_mc_975' : DEPAC_mc_975,
            'massad_mc_025' : massad_mc_025,
            'massad_mc_975' : massad_mc_975,
            'zhang_mc_025' : zhang_mc_025,
            'zhang_mc_975' : zhang_mc_975,
            }


#%% Accumulation plot with the error bars
label_fontsize = 9
legend_fontsize = 9
title_fontsize = 11
grid_alpha = 0.3
lw_plot = 1.5

label = r'F$_{\mathrm{tot}}$: '

error_GRAHAM = 0.24 #Vendel et al. paper (2023)
offset = timedelta(days=5)

DEPAC_acc = dataframes['DEPAC_baserun']['cumflux_mod'][-1]
massad_acc = dataframes['massad_baserun']['cumflux_mod'][-1]
zhang_acc = dataframes['zhang_baserun']['cumflux_mod'][-1]


yerr_DEPAC = [abs(DEPAC_acc-[dataframes['DEPAC_mc_025']['cumflux_mod'][-1]]), abs(DEPAC_acc-[dataframes['DEPAC_mc_975']['cumflux_mod'][-1]])]
yerr_massad = [abs(massad_acc - [dataframes['massad_mc_025']['cumflux_mod'][-1]]), abs(massad_acc - [dataframes['massad_mc_975']['cumflux_mod'][-1]])]
yerr_zhang = [abs(zhang_acc - [dataframes['zhang_mc_025']['cumflux_mod'][-1]]), abs(zhang_acc - [dataframes['zhang_mc_975']['cumflux_mod'][-1]])]


fig, ax = plt.subplots(1, figsize=(7.3,4))

#DEPAC
ax= plt.plot(dataframes['DEPAC_baserun'].index, 
            dataframes['DEPAC_baserun']['cumflux_mod'], label=label + 'DEPAC',
            linewidth= lw_plot)
plt.errorbar(dataframes['DEPAC_baserun'].index[-1] + offset,
                  y=dataframes['DEPAC_baserun']['cumflux_mod'][-1],
                  yerr=yerr_DEPAC, color='tab:blue', linewidth=lw_plot, capsize=3, fmt='o', markersize=3)

#MASSAD
plt.plot(dataframes['DEPAC_baserun'].index, dataframes['massad_baserun']['cumflux_mod'], 
         label=label + 'Massad', linewidth= lw_plot)
plt.errorbar(dataframes['massad_baserun'].index[-1] + offset*2,
                  y=dataframes['massad_baserun']['cumflux_mod'][-1],
                  yerr=yerr_massad, color='tab:orange', linewidth=lw_plot, capsize=3,
                  fmt='o', markersize=3)

#ZHANG
plt.plot(dataframes['DEPAC_baserun'].index, dataframes['zhang_baserun']['cumflux_mod'], 
         label=label + 'Zhang', linewidth= lw_plot)
plt.errorbar(dataframes['zhang_baserun'].index[-1] + offset*3,
                  y=dataframes['zhang_baserun']['cumflux_mod'][-1],
                  yerr=yerr_zhang, color='tab:green', linewidth=lw_plot, capsize=3,
                  fmt='o', markersize=3)
#OBS
plt.plot(dataframes['DEPAC_baserun'].index, 
              dataframes['DEPAC_baserun']['cumflux_obs'], 
              color='black', label=label + 'GRAHAM', linewidth= lw_plot)

plt.errorbar(dataframes['DEPAC_baserun'].index[-1],
                  y=dataframes['DEPAC_baserun']['cumflux_obs'][-1],
                  yerr=abs(dataframes['DEPAC_baserun']['cumflux_obs'][-1]*error_GRAHAM), color='black', 
                  linewidth=lw_plot, capsize=3, fmt='o', markersize=3)


months = pd.date_range(start=dataframes['DEPAC_baserun'].index.min(), end=dataframes['DEPAC_baserun'].index.max(), freq='M')
month_labels = [month.strftime('%b-%Y') for month in months]
#Fix the months
# Format the x-axis to show month and year
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Locator for each month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')) 

plt.xticks(fontsize=label_fontsize)
plt.ylim(-2.75, 1)
plt.yticks(np.arange(-3.0, 1.0, step=0.5), fontsize=label_fontsize)
plt.ylabel("Σ NH$_{3}$ in kg ha$^{-1}$")
plt.grid(alpha=grid_alpha)

plt.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.50, -0.20), fontsize=legend_fontsize, frameon=True)
plt.tight_layout()
plt.savefig(f"{savefig_fp}figA01.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}figA01.png", format='png', dpi=300, bbox_inches='tight')
plt.show()