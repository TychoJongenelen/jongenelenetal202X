#%% Importing necessary libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

# %%2.Initialize measurement and model data
models = ['DEPAC', 'massad', 'zhang', 'zhang_original']
baseruns = {}

for model in models:
    baseruns[model] = pd.read_json(f"{data_fp}{model}_output.json", orient='records', lines=True, convert_dates=False)
    baseruns[model]['datetime'] = pd.to_datetime(baseruns[model]['datetime'], unit='ms')
    baseruns[model].set_index('datetime', inplace=True)

# Access individual datasets:
DEPAC_baserun = baseruns['DEPAC']
massad_baserun = baseruns['massad']
zhang_baserun = baseruns['zhang']
zhang_original = baseruns['zhang_original']


#%%3. Plot accumulated fluxes (without MC uncertainty range)
label_fontsize = 9
legend_fontsize = 9
title_fontsize = 11
grid_alpha = 0.3
lw_plot = 1.5

label = r'F$_{\mathrm{tot}}$: '
zhang_original_label = label + r'Zhang, Γ$_{\mathrm{soil}}$ = 2000 '
fig, ax = plt.subplots(1, figsize=(7.3,4))
plt.plot(DEPAC_baserun['cumflux_mod'], label=label + 'DEPAC', color='tab:blue', linewidth = lw_plot)
plt.plot(massad_baserun['cumflux_mod'], label=label + 'Massad', color='tab:orange', linewidth = lw_plot)
plt.plot(zhang_baserun['cumflux_mod'], label=label +'Zhang', color='tab:green', linewidth = lw_plot)
plt.plot(zhang_original['cumflux_mod'], label=zhang_original_label, color='tab:purple', linewidth = lw_plot)
plt.plot(DEPAC_baserun['cumflux_obs'], label=label + "GRAHAM", color='black', linewidth = lw_plot)
plt.ylabel("Σ NH$_{3}$ in kg ha$^{-1}$")
plt.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.50, -0.33), fontsize=legend_fontsize, frameon=True)

#Fix the months
# Format the x-axis to show month and year
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Locator for each month
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')) 
plt.ylim(-1.5, 0.25)
plt.xticks(fontsize=label_fontsize)
plt.yticks(np.arange(-1.5, 0.50, step=0.25), fontsize=label_fontsize)
plt.grid(alpha=grid_alpha)
plt.tight_layout()
plt.savefig(f"{savefig_fp}fig06.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}fig06.png", format='png', dpi=300, bbox_inches='tight')
plt.show()

# %%
