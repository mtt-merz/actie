import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '../aggregate_policy_1000.csv'
data = pd.read_csv(file_path)

# Adjusting the y-axis limits to focus on the most relevant part
relevant_range = data.quantile([0.05, 0.95]).values
ymin, ymax = relevant_range.min(), relevant_range.max()

# Plotting the horizontal box plot with reduced height
plt.figure(figsize=(10, 3))  # Reduced height to 4 inches
sns.boxplot(data=data, orient='h')  # Horizontal box plot
plt.xlabel('Duration')
plt.xlim(0, 550)
plt.yticks()
plt.tight_layout()
plt.show()
