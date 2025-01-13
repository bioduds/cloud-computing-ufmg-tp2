import pandas as pd
from fpgrowth_py import fpgrowth
import pickle

# File paths
file_1 = "/home/datasets/spotify/2023_spotify_songs.csv"
file_2 = "/home/datasets/spotify/2023_spotify_ds2.csv"

# Load the first dataset
df1 = pd.read_csv(file_1, sep="\t")
# Create itemsets based on artist names and track names
itemSetList1 = df1[['artist_name', 'track_name']].apply(list, axis=1).tolist()

# Load the second dataset
df2 = pd.read_csv(file_2, sep="\t")
# Create itemsets based on artist names and track names
itemSetList2 = df2[['artist_name', 'track_name']].apply(list, axis=1).tolist()

# Combine itemsets from both datasets
itemSetList = itemSetList1 + itemSetList2

# Parameters
min_support_ratio = 0.4
min_confidence = 0.5

# Generate frequent itemsets and rules
freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=min_support_ratio, minConf=min_confidence)

# Save rules to a file
with open('rules.pkl', 'wb') as f:
    pickle.dump(rules, f)

# Print results
print("Frequent Itemsets:", freqItemSet)
print("Generated Rules:", rules)
