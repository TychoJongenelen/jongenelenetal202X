#%% Importing necessary libraries
import numpy as np
import pandas as pd
from scipy.stats import linregress
import os

#Change to your desired directory:
os.chdir('/home/jongenet/jongenelenetal202X/figure_scripts/')
savefig_fp = "../figures/"
data_fp = "../model_output/"
def linear_regression(x, y):
    # Perform linear regression
    slope, intercept, r, _, _ = linregress(x.dropna(), y.dropna())
    return slope, intercept, r


# %%2.Initialize measurement and model data
DEPAC_baserun = pd.read_json(data_fp+"DEPAC_output.json", orient='records', lines=True)
massad_baserun = pd.read_json(data_fp+"massad_output.json", orient='records', lines=True)
zhang_baserun = pd.read_json(data_fp+"zhang_output.json", orient='records', lines=True)
model_dict = {"DEPAC" : DEPAC_baserun, "Massad": massad_baserun, "Zhang" : zhang_baserun}
#%%Scatterplot: Model versus observations 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as tkr
import matplotlib.colors as mcolors

#Standard font sizes
title_font = 14
label_font = 10
legend_font = 10
text_font = 12
grid_alpha = 0.3

hexbinplot_config = {
    'mincnt' :1, 
    'gridsize' : 30, 
    'edgecolor' :'white',
    'linewidth' : 0.1
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
    'loc' : 'lower right',
    'fontsize' : legend_font
    }

subplot_title_config = {
    'fontweight' :'bold', 
    'fontsize' : title_font
    }


# Define discrete color levels
vmax = 80
levels = np.arange(0, vmax + 1, 5)  # Adjust the step as needed
cmap = plt.get_cmap('viridis', len(levels) - 1)
norm = mcolors.BoundaryNorm(boundaries=levels, ncolors=cmap.N)

# Scatterplot: Model versus observations
factor = 1.25
fig, ax = plt.subplots(1, 3, figsize=(12 * factor, 4 * factor), sharey=True)

xlim = [-100, 40]
ylim = [-100, 10]
x_label = "$F_{tot}$: Observations (ng m$^{-2}$ s$^{-1}$)"
y_label = "$F_{tot}$: Model (ng m$^{-2}$ s$^{-1}$)"
colors = ['red', 'black', 'grey']

for i, (model_name, model) in enumerate(model_dict.items()):
    obs = model['NH3_flux_obs']
    mod = model['flux_tot']
    slope, intercept, r = linear_regression(obs, mod)
    
    # Hexbin plot
    hb = ax[i].hexbin(obs, mod, vmax=vmax, cmap=cmap, **hexbinplot_config)
    
    # 1:1 line
    ax[i].plot(xlim, xlim, c=colors[0], **oneline_config)
    
    # Regression line
    ax[i].plot(np.linspace(*xlim), slope * np.linspace(*xlim) + intercept, color=colors[1], linewidth=2, label=f'y={slope:.2f}x {intercept:.2f}\nr: {r:.2f}')
    
    # Titles and labels
    ax[i].set_title(model_name, **subplot_title_config)
    ax[i].set_xlabel(x_label, fontsize=label_font)
    
    # Legends
    ax[i].legend(**legend_config)
    
    # Axes limits
    ax[i].set_xlim(xlim)
    ax[i].set_ylim(ylim)
    
    # Grid and axes lines
    ax[i].grid(alpha=grid_alpha)
    ax[i].axhline(0, color=colors[2], linewidth=0.5)
    ax[i].axvline(0, color=colors[2], linewidth=0.5)
    
# Adjust the layout and add the color bar below the middle plot
fig.subplots_adjust(bottom=0.25)
cbar_ax = fig.add_axes([0.4, 0.12, 0.23, 0.03])  # [left, bottom, width, height]
cbar = fig.colorbar(hb, cax=cbar_ax, orientation='horizontal', format=tkr.FormatStrFormatter('%.0f'), ticks=levels)
cbar.set_label('Count', fontsize=legend_font, labelpad=0)
    
ax[0].set_ylabel(y_label, fontsize=label_font)

# Add subplot labels
labels = ['a)', 'b)', 'c)']
for i, axi in enumerate(ax.flat):
    axi.text(0.02, 0.98, labels[i], transform=axi.transAxes, **abclabel_config)

# Improve layout using tight_layout
plt.savefig(f"{savefig_fp}fig02.pdf", format='pdf', dpi=300)
plt.savefig(f"{savefig_fp}fig02.png", format='png', dpi=800)
plt.show()
# %%
