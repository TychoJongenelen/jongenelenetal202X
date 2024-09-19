#%% Importing necessary libraries
#%% Importing necessary libraries
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Adding paths to custom scripts
sys.path.extend(['/home/jongenet/jongenet/scripts/a_load_flux_measurements/',
                 '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions',
                 '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo'])

# Importing custom scripts
from pM00_run_models import solleveld_run_MC
from a01_load_solleveld_data import load_solleveld_data
from pF_functions import preprocessing_baserun
savefig_fp = "/home/jongenet/jongenet/scripts_new/c_papers/c_paper_1/cb_figure_scripts/"
def preprocessing_baserun(df):
    df.reset_index(drop=True, inplace=True)
    solleveld_data.reset_index(drop=True, inplace=True)
    df = pd.concat([df, solleveld_data], axis=1)
    df = df[u_star_mask]
    df.index = df['datetime']
    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='H')
    df = df.reindex(date_range)
    df['flux_tot'] = df['flux_tot'] * 1000 #from ug to ng
    df['flux_stom'] = df['flux_stom'] * 1000 #from ug to ng
    df['flux_w'] = df['flux_w'] * 1000 #from ug to ng
    df['NH3_flux_obs'] = df['NH3_flux_obs'] * 1000  #from ug to ng
    df['cumflux_mod'] = df['flux_tot'].cumsum() * 3600 / 10**9 * 10**4  # Modelled results
    df['cumflux_obs'] = df['NH3_flux_obs'].cumsum() * 3600 / 10**9 * 10**4  # Measurements
    df['hour'] = df.index.hour
    df['hour'] = df.index.hour
    return df
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

DEPAC_baserun = preprocessing_baserun(DEPAC_baserun)
massad_baserun = preprocessing_baserun(massad_baserun)
zhang_baserun = preprocessing_baserun(zhang_baserun)
zhang_baserun['flux_soil'] = zhang_baserun['flux_soil']*1000 #Manual conversion from ug to ng
model_dict = {"DEPAC" : DEPAC_baserun, "Massad": massad_baserun, "Zhang" : zhang_baserun}
#%%Calculate accumulated deposition per enable_soil_pathway
D_acc = DEPAC_baserun['flux_tot'].sum() / 10**12 * 10**4 * 3600
M_acc = massad_baserun['flux_tot'].sum() / 10**12 * 10**4 * 3600
Z_acc = zhang_baserun['flux_tot'].sum() / 10**12 * 10**4 * 3600
Obs_acc = solleveld_data['NH3_flux_obs'].sum()  / 10**9 * 10**4 * 3600

D_stom, M_stom, Z_stom = DEPAC_baserun['flux_stom'].sum() / 10**12 * 10**4 * 3600, massad_baserun['flux_stom'].sum() / 10**12 * 10**4 * 3600, zhang_baserun['flux_stom'].sum() / 10**12 * 10**4 * 3600
D_w, M_w, Z_w = DEPAC_baserun['flux_w'].sum() / 10**12 * 10**4 * 3600, massad_baserun['flux_w'].sum() / 10**12 * 10**4 * 3600, zhang_baserun['flux_w'].sum() / 10**12 * 10**4 * 3600
D_g, M_g, Z_g = 0, 0, zhang_baserun['flux_soil'].sum() / 10**12 * 10**4 * 3600

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
