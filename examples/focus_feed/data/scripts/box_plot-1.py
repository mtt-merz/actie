import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load and clean the data
data = pd.read_csv('publish_different_topics.csv')

data_cleaned = data.drop(columns=['S1*'], errors='ignore')

# Create a box plot with specific aesthetics
plt.figure(figsize=(4, 8))
sns.boxplot(data=data_cleaned)

# Adjusting the y-axis limits to focus on the most relevant part
relevant_range = data.quantile([0, 0.95]).values
ymin, ymax = 0, 320# relevant_range.max()
plt.ylim(ymin, ymax)

plt.ylabel('Duration', fontsize=16)
plt.yticks()
plt.tight_layout()
plt.show()

#0.174 right