import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL
import util
import numpy as np

plt.rcParams["font.size"] = 20

counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))
plays = pickle.load(open("object_count_data/obj_plays_0_81920", "rb"))

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")

# Plotting:
# - Top 10 objects used in levels, compare with top 10 objects in played levels
#  o Bar chart with 2 bars for 1st, 2nd, etc. position
#  o Color coded according to item color, hammer icon for "make", controller icon for "play"
# / Bottom 10 objects used in levels
#  o Bar chart
# - Objects like/boo ratio OR clear rate vs. average over all levels
#  o Bar chart with line at 0, light blue for boo and light red for like, only compare most deviating ones
# - Game styles played vs. made
#  o Bar chart with 2 bars
# - Possibly also interesting: how do the number of enemies, powerups, checkpoints, 1-ups, etc. correlate to the like/boo ratio or clear rate?
#     (for enemies: possibly filter out levels that contain stars)
#  o Scatterplot

fig, ax = plt.subplots()
fig.set_size_inches(4, 2)

total_levels = 81920
total_plays = df["plays"][:81920].sum()

ordered_counts = sorted(counts, key=counts.get, reverse=True)

height = 0.5

gs_counts = {i: (df.loc[:total_levels]["gamestyle"] == i).sum() for i in range(5)}
ordered_keys = sorted(gs_counts, key=gs_counts.get, reverse=True)
ordered_values = [gs_counts[key] / total_levels * 100 for key in ordered_keys]

colors = [
  "#DD5917", # SMB1
  "#FFD9A8", # SMB3
  "#93FEFF", # SMW
  "#FFD900", # NSMBU
  "#1393FF", # SM3DW
]

images = [
  "gsi_smb1",
  "gsi_smb3",
  "gsi_smw",
  "gsi_nsmbu",
  "gsi_sm3dw",
]

for i in range(5):
  ax.barh(0.5, ordered_values[i], height, sum(ordered_values[:i]), edgecolor="black", color=colors[ordered_keys[i]])
  img = PIL.Image.open(f"sprites/{images[ordered_keys[i]]}.png")
  img = img.resize((int(64 * img.width / img.height), 64))
  img = img.crop((0, 0, 0, 0))
  ib = OffsetImage(img, zoom=0.3)
  ib.image.axes = ax
  ab = AnnotationBbox(ib,
                      (sum(ordered_values[:i]) + ordered_values[i] / 2, 0.5),
                      frameon=False
                      )
  ax.add_artist(ab)

gs_plays = {i: df.loc[:total_levels][(df.loc[:total_levels]["gamestyle"] == i)]["plays"].sum() for i in range(5)}
ordered_values = [gs_plays[key] / total_plays * 100 for key in ordered_keys]

for i in range(5):
  ax.barh(0, ordered_values[i], height, sum(ordered_values[:i]), edgecolor="black", color=colors[ordered_keys[i]])

ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.set_xlabel(r"% of levels")
#ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
#ax.set_ylabel(r"% of levels")
#ax.set_ylim(0, ymax)
plt.tight_layout()

plt.savefig("plots/gamestyles.png", dpi=300, transparent=True)