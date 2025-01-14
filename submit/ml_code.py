import pandas as pd
from fpgrowth_py import fpgrowth
import pickle

# arquivos csv
file_1 = "/home/datasets/spotify/2023_spotify_songs.csv"
file_2 = "/home/datasets/spotify/2023_spotify_ds2.csv"

# carregando dataset
df1 = pd.read_csv(file_1, sep="\t")
# Criando sets baseado em artista e track
itemSetList1 = df1[['artist_name', 'track_name']].apply(list, axis=1).tolist()

# carregando dataset
df2 = pd.read_csv(file_2, sep="\t")
# Criando sets baseado em artista e track
itemSetList2 = df2[['artist_name', 'track_name']].apply(list, axis=1).tolist()

# Combinando sets
itemSetList = itemSetList1 + itemSetList2

# Parâmetros
min_support_ratio = 0.4
min_confidence = 0.5

# Gerando frequencias
freqItemSet, rules = fpgrowth(itemSetList, minSupRatio=min_support_ratio, minConf=min_confidence)

# Carregando em arquivo
with open('rules.pkl', 'wb') as f:
    pickle.dump(rules, f)

print("Frequent Itemsets:", freqItemSet)
print("Generated Rules:", rules)
