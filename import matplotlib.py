import matplotlib.pyplot as plt
import seaborn as sns

# Sample data: Replace this with your actual data
matches = 25
player1_wins = 10
player2_wins = 8
ties = 7

# Additional data for matches when Player 2 played first
matches_player2_first = 25
player1_wins_player2_first = 12
player2_wins_player2_first = 8
ties_player2_first = 5

# Data preparation
data = {
    'Outcome': ['Player 1 Wins', 'Player 2 Wins', 'Tied'],
    'Player1_Count': [player1_wins, player2_wins, ties],
    'Player2_Count': [player1_wins_player2_first, player2_wins_player2_first, ties_player2_first],
    'Winner': ['Player 1', 'Player 2', 'Tied']
}

# Create a DataFrame
import pandas as pd
df = pd.DataFrame(data)

# Set the style for the plot
sns.set(style="whitegrid")

# Create a bar plot for Player 1 vs Player 2
plt.figure(figsize=(12, 6))
barplot = sns.barplot(x='Outcome', y='Player1_Count', data=df, color='blue', alpha=0.7, label='Player 1 First')
barplot = sns.barplot(x='Outcome', y='Player2_Count', data=df, color='orange', alpha=0.7, label='Player 2 First')

# Add labels and title
plt.title('Game Statistics - Player 1 vs Player 2')
plt.xlabel('Outcome')
plt.ylabel('Number of Matches')

# Annotate the bars with winner names
for index, value in enumerate(df['Player1_Count']):
    barplot.text(index - 0.2, value + 0.1, df['Winner'][index], ha='center', va='bottom', color='blue')

for index, value in enumerate(df['Player2_Count']):
    barplot.text(index + 0.2, value + 0.1, df['Winner'][index], ha='center', va='bottom', color='orange')

# Add legend
plt.legend()

# Show the plot
plt.show()