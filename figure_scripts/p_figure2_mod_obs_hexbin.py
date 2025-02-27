#%%1. Importing necessary libraries
import numpy as np
import pandas as pd
from scipy.stats import linregress
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

# Set `directory_name` to the absolute path of your `/figure_scripts/` directory.
# Example: directory_name = "/path/to/your/project/figure_scripts/"
directory_name = ""
if directory_name == "":
    raise ValueError("Please specify the directory_name variable ")
else:
    os.chdir(directory_name)
    
savefig_fp = "../figures/"
data_fp = "../model_output/"
def linear_regression(x, y):
    # Perform linear regression
    slope, intercept, r, _, _ = linregress(x.dropna(), y.dropna())
    return slope, intercept, r


# %%2.Initialize measurement and model data
models = ['DEPAC', 'massad', 'zhang']
baseruns = {}

for model in models:
    baseruns[model] = pd.read_json(f"{data_fp}{model}_output.json", orient='records', lines=True, convert_dates=False)
    baseruns[model]['datetime'] = pd.to_datetime(baseruns[model]['datetime'], unit='ms')
    baseruns[model].set_index('datetime', inplace=True)

# Access individual datasets:
DEPAC_baserun = baseruns['DEPAC']
massad_baserun = baseruns['massad']
zhang_baserun = baseruns['zhang']


model_dict = {"DEPAC" : DEPAC_baserun, "Massad": massad_baserun, "Zhang" : zhang_baserun}
#%%S3. catterplot: Model versus observations 

label_fontsize = 9
legend_fontsize = 9
title_fontsize = 11
grid_alpha = 0.3

# Define discrete color levels
vmax = 100
levels = np.arange(0, vmax + 1, 10)  # Adjust the step as needed
cmap = plt.get_cmap('viridis', len(levels) - 1)

fig, ax = plt.subplots(1, 3, figsize=(7, 3.1), sharey=True)  

xlim = [-110, 40]
ylim = [-110, 10]
x_label = r"$\text{F}_{\text{tot, obs}}$ (ng m$^{-2}$ s$^{-1}$)"
y_label = r"$\text{F}_{\text{tot, mod}}$ (ng m$^{-2}$ s$^{-1}$)"
colors = ['red', 'black', 'grey']
vmax = 100
levels = np.arange(0, vmax + 1, 20) 

for i, (model_name, model) in enumerate(model_dict.items()):
    obs = model['NH3_flux_obs']
    mod = model['flux_tot']
    slope, intercept, r = linear_regression(obs, mod)
    
    # Hexbin plot
    hb = ax[i].hexbin(obs, mod, vmax=vmax, cmap=cmap, mincnt= 1, gridsize= 30, edgecolor='white', linewidth=0.1)
    
    # 1:1 line
    ax[i].plot(xlim, xlim, c=colors[0], linestyle = '--', linewidth = 1, label='1:1')
    
    # Regression line
    ax[i].plot(np.linspace(*xlim), slope * np.linspace(*xlim) + intercept, color=colors[1], linewidth=2, 
               label=f'$y={slope:.2f}x {intercept:.2f}$\n$r={r:.2f}$')
    
    # Titles and labels
    ax[i].set_title(model_name, fontsize=title_fontsize, fontweight='bold') 
    ax[i].set_xlabel(x_label, fontsize=label_fontsize)
    ax[i].tick_params(axis='both', which='major', labelsize=label_fontsize) 
    
    # Legends
    ax[i].legend(loc='lower right', fontsize=legend_fontsize, frameon=True) 
    
    # Axes limits
    ax[i].set_xlim(xlim)
    ax[i].set_ylim(ylim)
    
    # Grid and axes lines
    ax[i].grid(alpha=grid_alpha)
    ax[i].axhline(0, color=colors[2], linewidth=0.5)
    ax[i].axvline(0, color=colors[2], linewidth=0.5)

# Add y-label
ax[0].set_ylabel(y_label, fontsize=label_fontsize)

# Add subplot labels
labels = ['a)', 'b)', 'c)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.93, labels[i], transform=axi.transAxes, fontsize=label_fontsize)

#Add a colorbar
cbar_width = 0.25
cbar_x = (1 - cbar_width) / 2
cbar_ax = fig.add_axes([cbar_x, 0, cbar_width+0.02, 0.03])  # [left, bottom, width, height]
cbar = fig.colorbar(hb, cax=cbar_ax, orientation='horizontal', format=tkr.FormatStrFormatter('%.0f'), ticks=levels)
cbar.ax.tick_params(labelsize=label_fontsize)
cbar.set_label('Count', fontsize=label_fontsize)

fig.tight_layout()

plt.savefig(f"{savefig_fp}fig02.pdf", format='pdf', dpi=300, bbox_inches='tight')
plt.savefig(f"{savefig_fp}fig02.png", format='png', dpi=300, bbox_inches='tight')

plt.show()
# %%
