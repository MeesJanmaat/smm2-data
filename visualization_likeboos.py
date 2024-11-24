import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL
import util

counts_likes = pickle.load(open("object_count_data/obj_likes_0_81920", "rb"))
counts_boos = pickle.load(open("object_count_data/obj_boos_0_81920", "rb"))

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")

avg_likeboo = df["likes"][:81920].mean() / (df["likes"][:81920].mean() + df["boos"][:81920].mean())

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

fig, ax = plt.subplots()

like_boo_ratios = {key: (counts_likes[key]) / (counts_likes[key] + counts_boos[key]) for key in counts_likes}

ordered_keys = sorted(like_boo_ratios, key=like_boo_ratios.get, reverse=True)

width = 0.2
gap = 0.025
group_gap = 0.6
# Top 3
multiplier = -1
for key in ordered_keys[:3]:
  ax.bar(1 + (width + gap) * multiplier, like_boo_ratios[key], width, color=util.Objects[key].get_color(), edgecolor="black")
  multiplier += 1
# Average
ax.bar(1 + group_gap, avg_likeboo, width, color="white", edgecolor="black")
# Bottom 3
multiplier = -1
for key in ordered_keys[-3:]:
  print(key)
  print(like_boo_ratios[key])
  ax.bar(1 + 2 * group_gap + (width + gap) * multiplier, like_boo_ratios[key], width, color=util.Objects[key].get_color(), edgecolor="black")
  multiplier += 1

ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.axhline(0, color='black')
ax.set_ylabel(r"Average score per level")
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
    ib = OffsetImage(img, zoom=0.3)
    ib.image.axes = ax
    ab = AnnotationBbox(ib,
                        labels[i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

for i in range(3):
    img = PIL.Image.open(f"sprites/obj_{ordered_keys[-(3 - i)].name}.png")
    img = img.resize((64, 64), PIL.Image.NEAREST)
    ib = OffsetImage(img, zoom=0.3)
    ib.image.axes = ax
    ab = AnnotationBbox(ib,
                        labels[3 + i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

ax.set_xticks([1 + group_gap])
ax.set_xticklabels(["Average"])

plt.savefig("plots/likevsboos.png", transparent=True)