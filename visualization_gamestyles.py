### Generates the graph relating levels made/played per gamestyle.

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import pickle
import PIL

plt.rcParams["font.size"] = 20

# Load data
counts = pickle.load(open("object_count_data/obj_counts_0_81920", "rb"))
plays = pickle.load(open("object_count_data/obj_plays_0_81920", "rb"))

fig, ax = plt.subplots()

total_levels = 81920
total_plays = 31950883 # df["plays"][:81920].sum()

ordered_counts = sorted(counts, key=counts.get, reverse=True)

width = 0.4
ymax = 40

# Count total levels in each gamestyle
gs_counts = pickle.load(open("misc_data/gs_counts", "rb"))
ordered_keys = sorted(gs_counts, key=gs_counts.get, reverse=True)
ordered_counts = [gs_counts[key] / total_levels * 100 for key in ordered_keys]

# Count total plays of each gamestyle
gs_plays = pickle.load(open("misc_data/gs_plays", "rb"))
ordered_plays = [gs_plays[key] / total_plays * 100 for key in ordered_keys]

# Color defs
colors = [
  "#DD5917", # SMB1
  "#FFD9A8", # SMB3
  "#93FEFF", # SMW
  "#FFD900", # NSMBU
  "#1393FF", # SM3DW
]

colors_light = [
  "#FF8947", # SMB1
  "#FFFFD8", # SMB3
  "#C3FFFF", # SMW
  "#FFFF30", # NSMBU
  "#43C3FF", # SM3DW
]

# Gamestyle icon filenames
images = [
  "gsi_smb1",
  "gsi_smb3",
  "gsi_smw",
  "gsi_nsmbu",
  "gsi_sm3dw",
]

# Plotting
for i in range(5):
  ax.bar(i - width / 2, ordered_counts[i], width, edgecolor="black", color=colors[ordered_keys[i]])
  img = PIL.Image.open("sprites/hammer.png")
  img = img.resize((128, 128))
  oi = OffsetImage(img, zoom=0.15)
  oi.image.axes = ax
  ab = AnnotationBbox(oi,
                      (i - width / 2, ordered_counts[i] - 4 * (ymax/100)),
                      frameon=False
                      )
  ax.add_artist(ab)

  ax.bar(i + width / 2, ordered_plays[i], width, edgecolor="black", color=colors_light[ordered_keys[i]])
  img = PIL.Image.open("sprites/controller.png")
  img = img.resize((128, 128))
  oi = OffsetImage(img, zoom=0.15)
  oi.image.axes = ax
  ab = AnnotationBbox(oi,
                      (i + width / 2, ordered_plays[i] - 4 * (ymax/100)),
                      frameon=False
                      )
  ax.add_artist(ab)


ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.grid(visible=True, axis="y", ls="--", lw=1, c="black")
ax.set_ylabel(r"% of levels")
ax.set_ylim(0, ymax)
plt.tight_layout()

# Rendering sprites
ax.set_xticks(range(5))
labels = ax.get_xticklabels()

for i in range(5):
  img = PIL.Image.open(f"sprites/{images[ordered_keys[i]]}.png")
  img = img.resize((int(128 * img.width / img.height), 128))
  oi = OffsetImage(img, zoom=0.25)
  oi.image.axes = ax
  ab = AnnotationBbox(oi,
                      labels[i].get_position(),
                      frameon=False,
                      box_alignment=(0.5, 1.2)
                      )
  ax.add_artist(ab)

plt.savefig("plots/gamestyles.png", dpi=300, transparent=True)