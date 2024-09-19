import pandas as pd
import numpy as np
import sys
#%%2. Do the Monte Carlo UP
sys.path.extend(['/home/jongenet/jongenet/scripts/a_load_flux_measurements/'])
sys.path.insert(1, '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo/data')
sys.path.extend([r'/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions'])
sys.path.insert(1, '/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo/')

from a01_load_solleveld_data import load_solleveld_data
from pM00_MonteCarlo_settings import variability_boundaries, key_names, key_names_pure_string, suffix
from pM00_run_models import solleveld_run_MC
from pF_functions import add_missing_datetime_rows, preprocessing_baserun


run_dct = {}
fp_sa_data = "/home/jongenet/jongenet/scripts/p_scripts_paper1/pF_functions/MonteCarlo/data/SA_runs/"
for key, values in variability_boundaries.items():
    D = []
    M = []
    Z = []
    for i, value in enumerate(values):
        fp_depac = fp_sa_data + "DEPAC_"+ key + "_" + str(np.round(variability_boundaries[key][i], 2)) + ".csv"
        fp_massad = fp_sa_data + "massad_"+ key + "_" + str(np.round(variability_boundaries[key][i], 2)) + ".csv"
        fp_zhang = fp_sa_data + "zhang_"+ key + "_" + str(np.round(variability_boundaries[key][i], 2)) + ".csv"
        depac_df = pd.read_csv(fp_depac, delimiter=',', index_col=0, header=0)
        massad_df = pd.read_csv(fp_massad, delimiter=',', index_col=0, header=0)
        zhang_df = pd.read_csv(fp_zhang, delimiter=',', index_col=0, header=0)
        depac_df.index = pd.to_datetime(depac_df.index)
        massad_df.index = pd.to_datetime(massad_df.index)
        zhang_df.index = pd.to_datetime(zhang_df.index)
       
        D.append(depac_df)
        M.append(massad_df)
        Z.append(zhang_df)
    
    run_dct["DEPAC_" + key] = D
    run_dct["massad_" + key] = M
    run_dct["zhang_" + key] = Z

#%%Get baserun flux data
baserun = solleveld_run_MC(MC_switch=False,
                            LAI_scaling=True,
                            LAI_scaling_min=0.5,
                            LAI_scaling_max=1.0,
                            enforce_soil_pathway=False)

solleveld_data = load_solleveld_data()
DEPAC_baserun = pd.DataFrame(baserun['DEPAC'], columns=baserun['DEPAC_keys'])
massad_baserun = pd.DataFrame(baserun['massad'], columns=baserun['massad_keys'])
zhang_baserun = pd.DataFrame(baserun['zhang'], columns=baserun['zhang_keys'])
u_star_mask = DEPAC_baserun['u_star'] > 0.1


DEPAC_baserun = preprocessing_baserun(DEPAC_baserun, u_star_mask, solleveld_data)
massad_baserun = preprocessing_baserun(massad_baserun, u_star_mask, solleveld_data)
zhang_baserun =  preprocessing_baserun(zhang_baserun, u_star_mask, solleveld_data)


D_baserun_mean_flux = np.mean(DEPAC_baserun['flux_tot'])
M_baserun_mean_flux = np.mean(massad_baserun['flux_tot'])
Z_baserun_mean_flux = np.mean(zhang_baserun['flux_tot'])

#%%Calculate the statistics and make a nice table
sa_stats_D = {}
sa_stats_M = {}
sa_stats_Z = {}
for var, values in variability_boundaries.items():
    D_mcrun_lower = np.mean(run_dct[f'DEPAC_{var}'][0]['flux_tot'])
    M_mcrun_lower = np.mean(run_dct[f'massad_{var}'][0]['flux_tot'])
    Z_mcrun_lower = np.mean(run_dct[f'zhang_{var}'][0]['flux_tot'])
    D_mcrun_upper = np.mean(run_dct[f'DEPAC_{var}'][-1]['flux_tot'])
    M_mcrun_upper = np.mean(run_dct[f'massad_{var}'][-1]['flux_tot'])
    Z_mcrun_upper = np.mean(run_dct[f'zhang_{var}'][-1]['flux_tot'])
    
    #Without the lower/upper value
    D_lower_upper = (1-(D_mcrun_lower/D_baserun_mean_flux)), (1-(D_mcrun_upper/D_baserun_mean_flux))
    M_lower_upper = (1-(M_mcrun_lower/M_baserun_mean_flux)), (1-(M_mcrun_upper/M_baserun_mean_flux))
    Z_lower_upper = (1-(Z_mcrun_lower/Z_baserun_mean_flux)), (1-(Z_mcrun_upper/Z_baserun_mean_flux))

    #With the lower/upper value added
    #D_lower_upper = (values[0] , 100-(D_mcrun_lower/D_baserun_mean_flux)*100), (values[-1],100-(D_mcrun_upper/D_baserun_mean_flux)*100)
    #M_lower_upper = (values[0], 100-(M_mcrun_lower/M_baserun_mean_flux)*100), (values[-1], 100-(M_mcrun_upper/M_baserun_mean_flux)*100)
    #Z_lower_upper = (values[0], 100-(Z_mcrun_lower/Z_baserun_mean_flux)*100), (values[-1], 100-(Z_mcrun_upper/Z_baserun_mean_flux)*100)

    sa_stats_D[key_names[var][0]] = D_lower_upper
    sa_stats_M[key_names[var][0]] = M_lower_upper
    sa_stats_Z[key_names[var][0]] = Z_lower_upper

sa_stats_D_df = pd.DataFrame.from_dict(sa_stats_D, orient='index', columns=['low', 'high'])
sa_stats_M_df = pd.DataFrame.from_dict(sa_stats_M, orient='index', columns=['low', 'high'])
sa_stats_Z_df = pd.DataFrame.from_dict(sa_stats_Z, orient='index', columns=['low', 'high'])


sa_stats_df = pd.concat([sa_stats_D_df, sa_stats_M_df, sa_stats_Z_df], axis=1)

sa_stats_df.to_csv("/home/jongenet/jongenet/scripts/p_scripts_paper1/figure_scripts/p_table2_SA_statistics.csv", sep=';')
# %%
