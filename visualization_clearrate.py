import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import pandas as pd
import PIL
import util

plt.rcParams["font.size"] = 20

counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))
counts_clears = pickle.load(open("object_count_data/obj_clears_0_81920", "rb"))
counts_attempts = pickle.load(open("object_count_data/obj_attempts_0_81920", "rb"))

df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")

avg_clearrate = df["clears"][:81920].mean() / df["attempts"][:81920].mean() * 100

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

clear_rates = {key: counts_clears[key] / counts_attempts[key] * 100 for key in counts_clears}

ordered_counts = sorted(counts, key=counts.get, reverse=True)
ordered_keys = sorted(clear_rates, key=clear_rates.get, reverse=True)

width = 0.2
gap = 0.025
group_gap = 0.6
# Top 3
multiplier = -1
for key in ordered_keys[:3]:
  ax.bar(1 + (width + gap) * multiplier, clear_rates[key], width, color=util.Objects[key].get_color(), edgecolor="black")
  ax.text(1 + (width + gap) * multiplier, -10, f"#{ordered_counts.index(key) + 1}", fontsize=10, ha="center", fontweight="bold", bbox={"boxstyle": "round,pad=0.2,rounding_size=0.3", "edgecolor": "none", "facecolor": "#FFEC99"})
  multiplier += 1
# Average
ax.bar(1 + group_gap, avg_clearrate, width, color="white", edgecolor="black")
# Bottom 3
multiplier = -1
for key in ordered_keys[-3:]:
  ax.bar(1 + 2 * group_gap + (width + gap) * multiplier, clear_rates[key], width, color=util.Objects[key].get_color(), edgecolor="black")
  ax.text(1 + 2 * group_gap + (width + gap) * multiplier, -10, f"#{ordered_counts.index(key) + 1}", fontsize=10, ha="center", fontweight="bold", bbox={"boxstyle": "round,pad=0.2,rounding_size=0.3", "edgecolor": "none", "facecolor": "#FFEC99"})
  multiplier += 1

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.axhline(0, color='black')
ax.set_ylabel(r"Average clear rate (%)")
ax.set_ylim(0, 50)
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
    ib = OffsetImage(img, zoom=0.45)
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
    ib = OffsetImage(img, zoom=0.45)
    ib.image.axes = ax
    ab = AnnotationBbox(ib,
                        labels[3 + i].get_position(),
                        frameon=False,
                        box_alignment=(0.5, 1.2)
                        )
    ax.add_artist(ab)

ax.set_xticks([1 + group_gap])
ax.set_xticklabels(["Avg."])

plt.savefig("plots/clearrates.png", dpi=300, transparent=True)