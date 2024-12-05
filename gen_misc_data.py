### Generates misc. data used in the visualization.

import pickle
import pandas as pd

# Gamestyle levels & plays
total_levels = 81920

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")
gs_counts = {i: (df.loc[:total_levels]["gamestyle"] == i).sum() for i in range(5)}
pickle.dump(gs_counts, open("misc_data/gs_counts", "wb"))

gs_plays = {i: df.loc[:total_levels][(df.loc[:total_levels]["gamestyle"] == i)]["plays"].sum() for i in range(5)}
pickle.dump(gs_plays, open("misc_data/gs_plays", "wb"))