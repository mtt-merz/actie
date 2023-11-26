import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the dataset
file_path = 'unsubscribe.csv'
data = pd.read_csv(file_path)

# Function to calculate a polynomial trend line
def calculate_polynomial_trend_line(data, degree = 3):
    x = np.arange(len(data))
    z = np.polyfit(x, data, degree)
    return np.poly1d(z)(x)

# Applying a linear regression to each column to find the trend lines
trend_lines = {}
for column in data.columns:
    trend_lines[column] = calculate_polynomial_trend_line(data[column])

# Customizing colors for the plots
colors = {
    'Actie': 'green',
    'Actie*': 'blue',
    'Functions': 'red'
}
trend_colors = {key: f'dark{color}' for key, color in colors.items()}
transparency = 0.5  # Semi-transparent for the original curves

# Adjusting the size of the subplots: line plot to take 3/4 of the horizontal space, and the box plot 1/4
fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={'width_ratios': [3, 1]})

# Line Plot with Trend Lines
for column, color in colors.items():
    axes[0].plot(data[column], label=f'{column}', color=color, alpha=transparency)
    axes[0].plot(trend_lines[column], linestyle='-', color=trend_colors[column], linewidth=3)  # Bolder trend lines

axes[0].set_title('Line Plot with Trends')
axes[0].set_xlabel('Observations')
axes[0].set_ylabel('Duration')
axes[0].legend(loc='upper right')

# Box Plot with matching colors
for i, column in enumerate(data.columns):
    data.boxplot(column=column, ax=axes[1], positions=[i], boxprops=dict(color=colors[column]), 
                 medianprops=dict(color=colors[column]), whiskerprops=dict(color=colors[column]), 
                 capprops=dict(color=colors[column]), flierprops=dict(markeredgecolor=colors[column]))

axes[1].set_title('Box Plot')
axes[1].set_xticklabels(data.columns, rotation=45)

# Adjusting the y-axis limits to focus on the most relevant part
relevant_range = data.quantile([0.05, 0.95]).values
ymin, ymax = relevant_range.min(), relevant_range.max()
axes[0].set_ylim(ymin, ymax)
axes[1].set_ylim(ymin, ymax)

# Ensuring alignment between the two plots
plt.tight_layout()
plt.show()
