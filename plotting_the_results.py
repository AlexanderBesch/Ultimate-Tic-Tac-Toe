import matplotlib.pyplot as plt
import seaborn as sns

# Example data
players = ['Random Goes First', 'Huiristic 1 Goes First','tie']
random_goes_first = [15, 8, 2]
hue_goes_first = [10, 12, 3]
ties = [3,4,5]
# Create a bar plot for the number of wins
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

bar_width = 0.35
index = range(len(players))

bar1 = plt.bar(index, random_goes_first, bar_width, label='Win', color='skyblue')
bar2 = plt.bar([i + bar_width for i in index], hue_goes_first, bar_width, label='Ties', color='lightcoral')
bar3 = plt.bar(index, ties, bar_width, label='Trial', color='skyblue')

# Add labels and title
plt.xlabel('Players', fontsize=14)
plt.ylabel('Number of Games', fontsize=14)
plt.title('Game Statistics', fontsize=16)
plt.xticks([i + bar_width/2 for i in index], players)
plt.legend()

# Show the plot
plt.show()
