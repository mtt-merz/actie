import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path1 = ''
file_path2 = ''

# Retry loading the datasets
try:
    data1 = pd.read_csv(file_path1, sep=';')
except Exception as e1:
    error1 = str(e1)

try:
    data2 = pd.read_csv(file_path2, sep=';')
except Exception as e2:
    error2 = str(e2)


data1_duration = data1.iloc[:, 1].reset_index(drop=True)
data2_duration = data2.iloc[:, 1].reset_index(drop=True)

# Creating a combined DataFrame for plotting
combined_data = pd.DataFrame({
    'Data 1 Duration (ms)': data1_duration,
    'Data 2 Duration (ms)': data2_duration
})

# Reset index to use as x-axis
combined_data = combined_data.reset_index().rename(
    columns={'index': 'Entry Position'})


# Importing Seaborn and Matplotlib for plotting

# Plotting the data
plt.figure(figsize=(12, 6))
sns.lineplot(data=combined_data)
plt.title("Comparison of Durations from Two Datasets")
plt.xlabel("Data Entry Position")
plt.ylabel("Duration (ms)")
plt.grid(True)
plt.show()
