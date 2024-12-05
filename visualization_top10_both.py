### Generates the graph of the 5 objects with the largest discrepancy in player/maker usage on both sides.

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import PIL
import numpy as np

plt.rcParams["font.size"] = 20

# Load data
counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))
plays = pickle.load(open("object_count_data/obj_plays_0_81920", "rb"))

fig, ax = plt.subplots()
fig.set_size_inches(8, 4.8)

total_levels = 81920
total_plays = 31950883 # df["plays"][:81920].sum()

ordered_counts = sorted(counts, key=counts.get, reverse=True)

# Calculate largest (relative) difference between maker/player usage, then sort
disparities = {key: counts[key] / total_levels - plays[key] / total_plays for key in counts.keys()}
ordered_keys = sorted(disparities, key=disparities.get, reverse=True)

# Take top and bottom 5
ordered_keys = [*ordered_keys[:5], *ordered_keys[-5:]]

width = 0.45
group_gap = 0.5
ymax = 80

# Plotting
for i in range(10):
  key = ordered_keys[i]
  pos = i + (i // 5 * group_gap)
  ax.bar(pos - width / 2, counts[key] / total_levels * 100, width=width, color="#FACD00", edgecolor="black")

  # Object ranking
  ax.text(pos, -ymax/7, f"#{ordered_counts.index(key) + 1}", fontsize=10, ha="center", fontweight="bold", bbox={"boxstyle": "round,pad=0.2,rounding_size=0.3", "edgecolor": "none", "facecolor": "#FFEC99"})

  if counts[key] / total_levels * 100 > 5:
    img = PIL.Image.open("sprites/hammer.png")
    img = img.resize((64, 64))
    oi = OffsetImage(img, zoom=0.2)
    oi.image.axes = ax
    ab = AnnotationBbox(oi,
                        (pos - width / 2, counts[key] / total_levels * 100 - 3 * (ymax/100)),
                        frameon=False
                        )
    ax.add_artist(ab)

  ax.bar(pos + width / 2, plays[key] / total_plays * 100, width=width, color="#FFEC99", edgecolor="black")
  
  if plays[key] / total_plays * 100 > 5:
    img = PIL.Image.open("sprites/controller.png")
    img = img.resize((64, 64))
    oi = OffsetImage(img, zoom=0.2)
    oi.image.axes = ax
    ab = AnnotationBbox(oi,
                        (pos + width / 2, plays[key] / total_plays * 100 - 3 * (ymax/100)),
                        frameon=False
                        )
    ax.add_artist(ab)

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.set_ylabel(r"% of levels")
ax.axvline(4.75, 0, ymax, ls="--", lw=1, c="black")
ax.set_ylim(0, ymax)
plt.tight_layout()

# Rendering sprites
ax.set_xticks([*range(5), *np.arange(5 + group_gap, 10 + group_gap)])
labels = ax.get_xticklabels()

for i in range(10):
    img = PIL.Image.open(f"sprites/obj_{ordered_keys[i].name}.png")
    img = img.resize((int(64 * img.width / img.height), 64), PIL.Image.NEAREST)
    oi = OffsetImage(img, zoom=0.3)
    oi.image.axes = ax
    ab = AnnotationBbox(oi,
                        labels[i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

ax.set_xticks([])

plt.savefig("plots/top10obj.png", dpi=300, transparent=True)