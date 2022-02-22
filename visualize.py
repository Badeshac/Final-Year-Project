# %%
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import pandas as pd

from cv_utils import draw_polygons, poly_norm_to_abs

# %%
image = Path("CURE-TSD", "00", "images", "train", "01_063.jpg")
labels = Path("CURE-TSD", "00", "labels", "train", "01_063.txt")

# %%
img = cv2.imread(
    filename=str(image),
    flags=cv2.IMREAD_COLOR,
)

h, w, c = img.shape
print(f"Image shape: {h}H x {w}W x {c}C")

# %%
# read the lables file so each line is a row
df = pd.read_csv(
    labels,
    delimiter="\t",
    header=None,
    names=["line"],
)

# split each line into a list of items
# expand each list into a number of columns
df = (
    df["line"]
    .str.split(" ", expand=True)
    .rename(
        columns={
            0: "class",
            1: "x",
            2: "y",
            3: "width",
            4: "height",
        }
    )
).astype(
    {
        "class": str,
        "x": float,
        "y": float,
        "width": float,
        "height": float,
    }
)

# get the x coordinates back from x-centre and width
df["llx"] = df["ulx"] = df["x"] - df["width"] / 2
df["lrx"] = df["urx"] = df["x"] + df["width"] / 2

# get the y coordinates back from y-centre and height
df["lly"] = df["lry"] = df["y"] - df["height"] / 2
df["uly"] = df["ury"] = df["y"] + df["height"] / 2


# %%
polys = df[["llx", "lly", "lrx", "lry", "ulx", "uly", "urx", "ury"]].values
polys = poly_norm_to_abs(polys, img.shape)
cats = df["class"].values.flatten()

drawn = draw_polygons(
    img,
    polys.astype(int),
    thickness=3,
    labels=cats,
    colors=(0, 180, 0),
    label_font_size=1,
)

# %%
fig, ax = plt.subplots(figsize=(20, 20))
ax.imshow(X=drawn, interpolation="none")
plt.axis("off")
plt.show()

# %%
