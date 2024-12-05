### Unused in the final data visualization.

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL

plt.rcParams["font.size"] = 20

counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))
counts_likes = pickle.load(open("object_count_data/obj_likes_0_81920", "rb"))
counts_boos = pickle.load(open("object_count_data/obj_boos_0_81920", "rb"))

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")

avg_likeboo = df["likes"][:81920].mean() / (df["likes"][:81920].mean() + df["boos"][:81920].mean())

fig, ax = plt.subplots()

like_boo_ratios = {key: (counts_likes[key]) / (counts_likes[key] + counts_boos[key]) for key in counts_likes}

ordered_counts = sorted(counts, key=counts.get, reverse=True)
ordered_keys = sorted(like_boo_ratios, key=like_boo_ratios.get, reverse=True)

width = 0.2
gap = 0.025
group_gap = 0.6
# Top 3
multiplier = -1
for key in ordered_keys[:3]:
  ax.bar(1 + (width + gap) * multiplier, like_boo_ratios[key], width, color="#FFEC99", edgecolor="black")
  ax.text(1 + (width + gap) * multiplier, -0.2, f"#{ordered_counts.index(key) + 1}", fontsize=10, ha="center", fontweight="bold", bbox={"boxstyle": "round,pad=0.2,rounding_size=0.3", "edgecolor": "none", "facecolor": "#FFEC99"})
  multiplier += 1
# Average
ax.bar(1 + group_gap, avg_likeboo, width, color="white", edgecolor="black")
# Bottom 3
multiplier = -1
for key in ordered_keys[-3:]:
  ax.bar(1 + 2 * group_gap + (width + gap) * multiplier, like_boo_ratios[key], width, color="#FFEC99", edgecolor="black")
  ax.text(1 + 2 * group_gap + (width + gap) * multiplier, -0.2, f"#{ordered_counts.index(key) + 1}", fontsize=10, ha="center", fontweight="bold", bbox={"boxstyle": "round,pad=0.2,rounding_size=0.3", "edgecolor": "none", "facecolor": "#FFEC99"})
  multiplier += 1

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.axhline(0, color='black')
ax.set_ylabel(r"Average level score*")
ax.set_ylim(0, 1)
plt.tight_layout()

# Rendering sprites
ax.set_xticks([
   1 - (width + gap),
   1,
   1 + (width + gap),
   1 + 2 * group_gap - (width + gap),
   1 + 2 * group_gap,
   1 + 2 * group_gap + (width + gap)
])
labels = ax.get_xticklabels()

for i in range(3):
    img = PIL.Image.open(f"sprites/obj_{ordered_keys[i].name}.png")
    img = img.resize((64, 64), PIL.Image.NEAREST)
    oi = OffsetImage(img, zoom=0.4)
    oi.image.axes = ax
    ab = AnnotationBbox(oi,
                        labels[i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

for i in range(3):
    img = PIL.Image.open(f"sprites/obj_{ordered_keys[-(3 - i)].name}.png")
    img = img.resize((64, 64), PIL.Image.NEAREST)
    oi = OffsetImage(img, zoom=0.4)
    oi.image.axes = ax
    ab = AnnotationBbox(oi,
                        labels[3 + i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

ax.set_xticks([1 + group_gap])
ax.set_xticklabels(["Avg."])

plt.savefig("plots/likevsboos.png", dpi=300, transparent=True)