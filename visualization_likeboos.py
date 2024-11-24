import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL

counts_obj = pickle.load(open("object_count_data/obj_counts_0_1024", "rb"))
counts_likes = pickle.load(open("object_count_data/obj_likes_0_1024", "rb"))
counts_boos = pickle.load(open("object_count_data/obj_boos_0_1024", "rb"))

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")

avg_likeboo = df["likes"][:1024].mean() - df["boos"][:1024].mean()

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

# SMW palette
colors = {
  "ground": "#D8A038",
  "block": "#F8D820",
  "hard_block": "#707070",
  "coin": "#F8C000",
  "spikes": "#BCBCBC",
  "question_block": "#F8D820",
  "spring": "#00B800",
  "ice_block": "#29CEFF",
  "door": "#D8A038",
  "pipe": "#00C800",
  "goomba": "#B82800",
  "koopa": "#00F800",
  "steep_slope": "#7E9797",
  "slight_slope": "#7E9797",
  "hidden_block": "#DDDDDD"
}

fig, ax = plt.subplots()

like_boo_ratios = {key: counts_likes[key] / counts_boos[key] for key in counts_likes}

ordered_keys = sorted(like_boo_ratios, key=like_boo_ratios.get, reverse=True)

ax.bar("Average", avg_likeboo, color="white", edgecolor="black")
for key in ordered_keys[:10]:
  ax.bar(key.name, like_boo_ratios[key], color="green", edgecolor="black")

ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.axhline(0, color='black')
ax.set_ylabel(r"Like to boo ratio")
plt.tight_layout()

# Rendering sprites
# ax.set_xticks(range(10))
# labels = ax.get_xticklabels()

# for i in range(10):
#     img = PIL.Image.open(f"sprites/obj_{ordered_keys[i].name}.png")
#     img = img.resize((64, 64), PIL.Image.NEAREST)
#     ib = OffsetImage(img, zoom=0.3)
#     ib.image.axes = ax
#     ab = AnnotationBbox(ib,
#                         labels[i].get_position(),
#                         frameon=False,
#                         box_alignment=(0.5, 1.2)
#                         )
#     ax.add_artist(ab)

#ax.set_xticks([])

plt.savefig("plots/likevsboos.png", transparent=True)