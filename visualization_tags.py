### Unused in the final data visualization.

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL
import numpy as np

plt.rcParams["font.size"] = 20

counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))
plays = pickle.load(open("object_count_data/obj_plays_0_81920", "rb"))

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")

fig, ax = plt.subplots()

total_levels = 81920
total_plays = df["plays"][:81920].sum()

ordered_counts = sorted(counts, key=counts.get, reverse=True)

width = 0.4
ymax = 40

unique_tags = df.loc[:total_levels][(df.loc[:total_levels]["tag1"] != df.loc[:total_levels]["tag2"])]

tags = pd.concat([df.loc[:total_levels][["tag1", "plays"]], unique_tags[["tag2", "plays"]]])

tag_counts = {}
tag_plays = {}
for i, r in df.loc[:total_levels].iterrows():
  tag_counts[r["tag1"]] = tag_counts.get(r["tag1"], 0) + 1
  tag_plays[r["tag1"]] = tag_counts.get(r["tag1"], 0) + r["plays"]
  if r["tag1"] != r["tag2"]:
    tag_counts[r["tag2"]] = tag_counts.get(r["tag2"], 0) + 1
    tag_plays[r["tag2"]] = tag_counts.get(r["tag2"], 0) + r["plays"]

ordered_keys = sorted(tag_counts, key=tag_counts.get, reverse=True)
ordered_counts = [tag_counts[key] for key in ordered_keys]
ordered_plays = [tag_plays[key] for key in ordered_keys]

print(ordered_counts)

TagNames = {
  0: "None",
  1: "Standard",
  2: "Puzzle solving",
  3: "Speedrun",
  4: "Autoscroll",
  5: "Auto mario",
  6: "Short and sweet",
  7: "Multiplayer versus",
  8: "Themed",
  9: "Music",
  10: "Art",
  11: "Technical",
  12: "Shooter",
  13: "Boss battle",
  14: "Single player",
  15: "Link"
}

for i in range(16):
  ax.bar(i - width / 2, ordered_counts[i], width, edgecolor="black", color="#AAAAAA")
  img = PIL.Image.open("sprites/hammer.png")
  img = img.resize((32, 32))
  oi = OffsetImage(img, zoom=0.4)
  oi.image.axes = ax
  ab = AnnotationBbox(oi,
                      (i - width / 2, ordered_counts[i] - 4 * (ymax/100)),
                      frameon=False
                      )
  ax.add_artist(ab)

  ax.bar(i + width / 2, ordered_plays[i], width, edgecolor="black", color="#CCCCCC")
  img = PIL.Image.open("sprites/controller.png")
  img = img.resize((32, 32))
  oi = OffsetImage(img, zoom=0.4)
  oi.image.axes = ax
  ab = AnnotationBbox(oi,
                      (i + width / 2, ordered_plays[i] - 4 * (ymax/100)),
                      frameon=False
                      )
  ax.add_artist(ab)


ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.set_ylabel(r"Number of levels")
#ax.set_ylim(0, ymax)
plt.tight_layout()

ax.set_xticks(range(16))
ax.set_xticklabels(ordered_keys)

# for i in range(5):
#     img = PIL.Image.open(f"sprites/{images[ordered_keys[i]]}.png")
#     img = img.resize((int(128 * img.width / img.height), 128))
#     oi = OffsetImage(img, zoom=0.25)
#     oi.image.axes = ax
#     ab = AnnotationBbox(oi,
#                         labels[i].get_position(),
#                         frameon=False,
#                         box_alignment=(0.5, 1.2)
#                         )
#     ax.add_artist(ab)

plt.savefig("plots/tags.png", dpi=300, transparent=True)