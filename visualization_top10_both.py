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

total_levels = 81920
total_plays = df["plays"][:81920].sum()

ordered_counts = sorted(counts, key=counts.get, reverse=True)

#print(ordered_keys[-1], counts[ordered_keys[-1]], counts[ordered_keys[-1]]/total_levels)

#disparities = {key: (counts[key] / total_levels - plays[key] / total_plays) / (counts[key] / total_levels) for key in counts.keys()}
disparities = {key: counts[key] / total_levels - plays[key] / total_plays for key in counts.keys()}
ordered_keys = sorted(disparities, key=disparities.get, reverse=True)

# Take top and bottom 5
ordered_keys = [*ordered_keys[:5], *ordered_keys[-5:]]

width = 0.4
group_gap = 0.5
ymax = 80

for i in range(10):
  key = ordered_keys[i]
  pos = i + (i // 5 * group_gap)
  ax.bar(pos - width / 2, counts[key] / total_levels * 100, width=width, color="#FACD00", edgecolor="black")

  ax.text(pos, -ymax/7, f"#{ordered_counts.index(key) + 1}", fontsize=10, ha="center", fontweight="bold", bbox={"boxstyle": "round,pad=0.2,rounding_size=0.3", "edgecolor": "none", "facecolor": "#FFEC99"})

  if counts[key] / total_levels * 100 > 5:
    img = PIL.Image.open("sprites/hammer.png")
    img = img.resize((32, 32))
    ib = OffsetImage(img, zoom=0.33)
    ib.image.axes = ax
    ab = AnnotationBbox(ib,
                        (pos - width / 2, counts[key] / total_levels * 100 - 5 * (ymax/100)),
                        frameon=False
                        )
    ax.add_artist(ab)

  ax.bar(pos + width / 2, plays[key] / total_plays * 100, width=width, color="#FFEC99", edgecolor="black")
  
  if plays[key] / total_plays * 100 > 5:
    img = PIL.Image.open("sprites/controller.png")
    img = img.resize((32, 32))
    ib = OffsetImage(img, zoom=0.33)
    ib.image.axes = ax
    ab = AnnotationBbox(ib,
                        (pos + width / 2, plays[key] / total_plays * 100 - 5 * (ymax/100)),
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
    ib = OffsetImage(img, zoom=0.3)
    ib.image.axes = ax
    ab = AnnotationBbox(ib,
                        labels[i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

ax.set_xticks([])

plt.savefig("plots/top10obj.png", dpi=300, transparent=True)