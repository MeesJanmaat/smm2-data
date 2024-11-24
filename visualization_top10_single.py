import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL
import util

counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))

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

ordered_keys = sorted(counts, key=counts.get, reverse=True)

for key in ordered_keys[-10:]:
  ax.bar(key.name, counts[key] / total_levels * 100, color=util.Objects[key].get_color(), edgecolor="black")

ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.set_ylabel(r"% of levels")
plt.tight_layout()

# Rendering sprites
ax.set_xticks(range(10))
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

plt.savefig("plots/top10obj_single.png", transparent=True)