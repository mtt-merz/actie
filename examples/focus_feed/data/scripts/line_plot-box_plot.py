import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from statsmodels.nonparametric.smoothers_lowess import lowess

# Load the dataset
file_path = 'publish_same_topic.csv'
data = pd.read_csv(file_path)

# data = data.drop(columns=['S2'])
data = data.drop(columns=['S1*'])

def apply_lowess(data, frac=0.4):
    # frac is the fraction of data used to compute each smoothed value
    x = np.arange(len(data))
    return lowess(data, x, frac=frac)[:, 1]

# Applying a linear regression to each column to find the trend lines
trend_lines = {}
for column in data.columns:
    trend_lines[column] = apply_lowess(data[column])

# Customizing colors for the plots
colors = {
    'S1': 'limegreen',
    # 'S1_50': 'green',
    # 'S1_20': 'dodgerblue',
    # 'S1_5': 'blue',
    # 'S1*': 'blueviolet',
    'S2': 'red',
}
trend_colors = {key: f'{color}' for key, color in colors.items()}
transparency = 0.3  # Semi-transparent for the original curves

# Adjusting the size of the subplots: line plot to take 3/4 of the horizontal space, and the box plot 1/4
fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [3, 1]})

# Line Plot with Trend Lines
for column, color in colors.items():
    axes[0].plot(data[column], label=f'{column}', color=color, alpha=transparency)
    axes[0].plot(trend_lines[column], linestyle='-', color=trend_colors[column], linewidth=3)  # Bolder trend lines

axes[0].set_xlabel('Observations', fontsize=16)
axes[0].set_ylabel('Duration', fontsize=16)
axes[0].legend(loc='upper right', fontsize=16)

# Box Plot with matching colors
for i, column in enumerate(data.columns):
    data.boxplot(column=column, ax=axes[1], positions=[i], boxprops=dict(color=colors[column]), 
                 medianprops=dict(color=colors[column]), whiskerprops=dict(color=colors[column]), 
                 capprops=dict(color=colors[column]), flierprops=dict(markeredgecolor=colors[column]))

axes[1].set_xticklabels(data.columns)

# Adjusting the y-axis limits to focus on the most relevant part
relevant_range = data.quantile([0.05, 0.95]).values
ymin, ymax = 0, 260# relevant_range.max()
axes[0].set_ylim(ymin, ymax)
axes[1].set_ylim(ymin, ymax)

# Ensuring alignment between the two plots
plt.tight_layout()
plt.show()
