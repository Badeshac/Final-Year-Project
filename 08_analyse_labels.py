# %%
from pathlib import Path

import pandas as pd

# %%
df = pd.read_csv(
    Path("CURE-TSD", "labels", "lables.csv"),
    index_col=0,
)

# %%
# signs frequency count
df["sign"].value_counts()

# %%
# signs statistics in a frame
df.groupby(["sequence", "frame"]).agg({"sign": "count"}).agg(["min", "mean", "max"])

# %%
# number of frames with signs in each frame
df.groupby(["sequence"]).agg({"frame": "nunique"})

# %%
# area statistics
(df["area"] * 100).describe().round(2)

# %%
df_train = pd.read_csv(Path("CURE-TSD", "labels", "train.csv"))
df_val = pd.read_csv(Path("CURE-TSD", "labels", "val.csv"))

df_train["sign"].value_counts()
df_val["sign"].value_counts()
