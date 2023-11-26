import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'set_policy.csv'
data = pd.read_csv(file_path)

# Adjusting the y-axis limits to focus on the most relevant part
relevant_range = data.quantile([0.05, 0.95]).values
ymin, ymax = relevant_range.min(), relevant_range.max()

# Plotting the box plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=data)
plt.ylim(ymin, ymax)
plt.ylabel('Duration')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
