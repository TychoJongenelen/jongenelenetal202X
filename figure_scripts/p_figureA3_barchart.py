#%% Importing necessary libraries
import numpy as np
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
mc_fp = "../uncertainty_analysis_output/"


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

#%%Calculate accumulated deposition per enable_soil_pathway
#Conversion factor to go from ng m-2 s-1 to kg ha-1 in total
conversion_factor = 10**-12 * 10**4 * 3600

Obs_acc = DEPAC_baserun['NH3_flux_obs'].sum()  * conversion_factor
D_stom, M_stom, Z_stom = DEPAC_baserun['flux_stom'].sum() * conversion_factor, massad_baserun['flux_stom'].sum() * conversion_factor, zhang_baserun['flux_stom'].sum() * conversion_factor
D_w, M_w, Z_w = DEPAC_baserun['flux_w'].sum() * conversion_factor, massad_baserun['flux_w'].sum() * conversion_factor, zhang_baserun['flux_w'].sum() * conversion_factor
D_g, M_g, Z_g = 0, 0, zhang_baserun['flux_soil'].sum() * conversion_factor

# Define the data
models = ['DEPAC', 'Massad', 'Zhang']
acc_stom = [D_stom, M_stom, Z_stom]  # Values for D_stom, M_stom, Z_stom
acc_w = [D_w, M_w, Z_w]      # Values for D_w, M_w, Z_w
acc_soil = [D_g, M_g, Z_g]    # Values for D_soil, M_soil, Z_soil

#%% Create the stacked bar chart
label_fontsize = 9
legend_fontsize = 9 #Changed here
title_fontsize = 11
grid_alpha = 0.3
width_bar = 0.8

plt.figure(figsize=(4, 4))

# Plot D_stom separately above 0 line
plt.bar(models[0], max(D_stom, 0), width=width_bar, color='tab:green')
plt.bar(models[0], min(D_stom, 0), width=width_bar, label='Stomatal deposition', color='tab:green')

# Plot D_w and D_g stacked below 0 line
plt.bar(models[0], D_w, bottom=0, width=width_bar, label='External deposition', color='tab:orange')

# Plot M and Z values
plt.bar(models[1:], acc_stom[1:], width=width_bar, color='tab:green')
plt.bar(models[1:], acc_w[1:], width=width_bar, bottom=acc_stom[1:], color='tab:orange')
plt.bar(models[1:], acc_soil[1:], width=width_bar, bottom=np.add(acc_stom[1:], acc_w[1:]), color='tab:brown', label='Soil deposition')
plt.axhline(Obs_acc, linestyle='--', color='black', lw=1.0, label = 'Observed total deposition')

# Add labels and legend
plt.xticks(fontsize=label_fontsize, fontweight='bold')
plt.yticks(fontsize=label_fontsize)
plt.ylabel("Σ NH$_{3}$ in kg ha$^{-1}$", fontsize=label_fontsize)
plt.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.3), fontsize=legend_fontsize)
plt.grid(alpha=grid_alpha)
plt.tight_layout()
plt.savefig(f"{savefig_fp}figA03.png", format='png', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}figA03.pdf", format='png', dpi=300, bbox_inches='tight')
plt.show()
# %%
