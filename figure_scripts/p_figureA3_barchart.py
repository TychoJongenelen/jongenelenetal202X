#%% Importing necessary libraries
import numpy as np
import pandas as pd
from scipy.stats import linregress

import matplotlib.pyplot as plt
import os

#Change to your desired directory:
os.chdir('/home/jongenet/jongenelenetal202X/figure_scripts/')

savefig_fp = "../figures/"
data_fp = "../model_output/"


# %%2.Initialize measurement and model data
DEPAC_baserun = pd.read_json(data_fp+"DEPAC_output.json", orient='records', lines=True)
massad_baserun = pd.read_json(data_fp+"massad_output.json", orient='records', lines=True)
zhang_baserun = pd.read_json(data_fp+"zhang_output.json", orient='records', lines=True)

#%%Calculate accumulated deposition per enable_soil_pathway
#Note total fluxes are in ng m-2 s-1 while compartment fluxes are in ug m-2 s-1.
#This is accounted for during the conversion to kg NH3 ha-1
D_acc = DEPAC_baserun['flux_tot'].sum() / 10**12 * 10**4 * 3600
M_acc = massad_baserun['flux_tot'].sum() / 10**12 * 10**4 * 3600
Z_acc = zhang_baserun['flux_tot'].sum() / 10**12 * 10**4 * 3600
Obs_acc = DEPAC_baserun['NH3_flux_obs'].sum()  / 10**12 * 10**4 * 3600

D_stom, M_stom, Z_stom = DEPAC_baserun['flux_stom'].sum() / 10**9 * 10**4 * 3600, massad_baserun['flux_stom'].sum() / 10**9 * 10**4 * 3600, zhang_baserun['flux_stom'].sum() / 10**9 * 10**4 * 3600
D_w, M_w, Z_w = DEPAC_baserun['flux_w'].sum() / 10**9 * 10**4 * 3600, massad_baserun['flux_w'].sum() / 10**9 * 10**4 * 3600, zhang_baserun['flux_w'].sum() / 10**9 * 10**4 * 3600
D_g, M_g, Z_g = 0, 0, zhang_baserun['flux_soil'].sum() / 10**9 * 10**4 * 3600

# Define the data
categories = ['Stomata', 'Cuticular', 'Ground']

models = ['DEPAC', 'Massad', 'Zhang']
acc_stom = [D_stom, M_stom, Z_stom]  # Values for D_stom, M_stom, Z_stom
acc_w = [D_w, M_w, Z_w]      # Values for D_w, M_w, Z_w
acc_soil = [D_g, M_g, Z_g]    # Values for D_soil, M_soil, Z_soil

DEPAC_acc = [D_stom, D_w, D_g]
Massad_acc = [M_stom, M_w, M_g]
Zhang_acc = [Z_stom, Z_w, Z_g]

#%% Create the stacked bar chart
from matplotlib.backends.backend_pdf import PdfPages
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



plt.figure(figsize=(4*2, 3*2))

# Plot D_stom separately above 0 line
plt.bar(models[0], max(D_stom, 0), color='tab:orange')
plt.bar(models[0], min(D_stom, 0), label='Stomatal deposition', color='tab:orange')

# Plot D_w and D_g stacked below 0 line
plt.bar(models[0], D_w, bottom=0, label='External deposition', color='tab:green')

# Plot M and Z values
plt.bar(models[1:], acc_stom[1:], color='tab:orange')
plt.bar(models[1:], acc_w[1:], bottom=acc_stom[1:], color='tab:green')
plt.bar(models[1:], acc_soil[1:], bottom=np.add(acc_stom[1:], acc_w[1:]), color='tab:brown', label='Soil deposition')
plt.axhline(Obs_acc, linestyle='--', color='black', lw=1.0, label = 'Observed total deposition')

# Add labels and legend
plt.ylabel("Σ NH$_{3}$ in kg ha$^{-1}$")
plt.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.2), fontsize=legend_font)
plt.grid(alpha=grid_alpha)
plt.tight_layout()
plt.savefig(f"{savefig_fp}figA03.png", format='png', dpi=800)
plt.savefig(f"{savefig_fp}figA03.pdf", format='png', dpi=300)
# %%
