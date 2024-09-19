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
from pF_functions import preprocessing_baserun

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

#%%3. Check if everything is fine, accumulated fluxes
plt.figure(figsize=(10, 6))
plt.plot( DEPAC_baserun['cumflux_mod'], label='$F_{tot}$: DEPAC')
plt.plot( massad_baserun['cumflux_mod'], label='$F_{tot}$: Massad')
plt.plot( zhang_baserun['cumflux_mod'], label='$F_{tot}$: Zhang')
plt.plot( DEPAC_baserun['cumflux_obs'], label='$F_{tot}$: GRAHAM', color='black')
plt.ylabel("Accumulated flux in kg/ha")

plt.title("$NH_{3}$ accumulated dry deposition: measurements versus model")
plt.legend(loc=3)
plt.grid()
plt.show()

#%%Create the table
#Mean flux - MAE - RMSE - Pearson r
def stats(mod):
    mean_flux = np.nanmean(mod['flux_tot'])
    MAE = mean_absolute_error(mod['NH3_flux_obs'].dropna(), mod['flux_tot'].dropna())
    RMSE = np.sqrt(mean_squared_error(mod['NH3_flux_obs'].dropna(), mod['flux_tot'].dropna()))
    p = pearsonr(mod['NH3_flux_obs'].dropna(), mod['flux_tot'].dropna())
    final_deposition = mod['cumflux_mod'].iloc[-1]
    print(f"Mean flux: {mean_flux:.4f}\nMean absolute error: {MAE:.4f}\nRoot mean square error: {RMSE:.4f}\nPearson correlation: {p[0]:.4f}\nTotal Deposition: {final_deposition:.4f}")

stats(DEPAC_baserun)
stats(massad_baserun)
stats(zhang_baserun)

#%%Calculate performance per measured flux range
#First plot the histogram with the measured flux ranges
plt.hist(DEPAC_baserun['NH3_flux_obs'], bins=20)
plt.axvline(DEPAC_baserun['NH3_flux_obs'].quantile(0.25), label="q=0.25", color='red')
plt.axvline(DEPAC_baserun['NH3_flux_obs'].quantile(0.50), label="q=0.50", color='blue')
plt.axvline(DEPAC_baserun['NH3_flux_obs'].quantile(0.75), label="q=0.75", color='green')
plt.legend()
plt.show()

# conc < -20
# -20 > conc < 0
# conc > 0

def stats_subset(mod):
    mod_high_dep = mod[mod['NH3_flux_obs'] <= -20]
    mod_low_dep = mod[(mod['NH3_flux_obs'] > -20) & (mod['NH3_flux_obs'] < 0)]
    mod_emis = mod[mod['NH3_flux_obs'] >= 0]

    dct = {'High deposition (f >= -20 )': mod_high_dep,
           'Moderate deposition (-20 < f < 0)': mod_low_dep,
           'mod_emis (f >= 0)' : mod_emis}
    
    for subset_name, subset in dct.items():
        print(subset_name)
        mean_flux = np.nanmean(subset['flux_tot'].dropna())
        mean_flux_obs = np.nanmean(subset['NH3_flux_obs'].dropna())
        RMSE = np.sqrt(mean_squared_error(subset['NH3_flux_obs'].dropna(), subset['flux_tot'].dropna()))
        MAE = mean_absolute_error(subset['NH3_flux_obs'].dropna(), subset['flux_tot'].dropna())
        p = pearsonr(subset['NH3_flux_obs'].dropna(), subset['flux_tot'].dropna())
        print(f"Mean flux: {mean_flux:.4f}\nMean flux obs: {mean_flux_obs:.4f}\nMean absolute error: {MAE:.4f}\nRoot mean square error: {RMSE:.4f}\nPearson correlation: {p[0]:.4f}\nLength:{len(subset)}")

print("DEPAC")
stats_subset(DEPAC_baserun)
print("Massad")
stats_subset(massad_baserun)
print("Zhang")
stats_subset(zhang_baserun)

# %%
