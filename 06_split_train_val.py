# %%
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# %%
df = pd.read_csv(
    Path("CURE-TSD", "labels", "lables.csv"),
    index_col=0,
)

df_train, df_val = train_test_split(
    df,
    test_size=0.2,
    stratify=df["sign"],
    shuffle=True,
    random_state=42,
)

# since each sign has a row, the same frame/image per sequence can be duplicated
# drop duplicated frames per sequence to keep only one frame/image
df_train = df_train.drop_duplicates(["sequence", "frame"]).sort_values(
    by=["sequence", "frame"],
    ignore_index=True,
)

df_val = df_val.drop_duplicates(["sequence", "frame"]).sort_values(
    by=["sequence", "frame"],
    ignore_index=True,
)

# save splits
df_train.to_csv(Path("CURE-TSD", "labels", "train.csv"))
df_val.to_csv(Path("CURE-TSD", "labels", "val.csv"))


# %%
def move_files(files, to):
    """Move files to images > to"""

    for file in files:

        # move the image to the images folder
        dst = Path(file.parent, "images", to)

        if not dst.exists():
            dst.mkdir(parents=True)

        print(f"Moving {file.name} to {dst}")
        shutil.move(src=file, dst=dst)

        # look for a label file with the same name as the image file
        file_txt = Path(file.parent, f"{file.stem}.txt")

        # if such a file exists, move it to the labels folder
        if file_txt.exists():
            dst = Path(file_txt.parent, "labels", to)

            if not dst.exists():
                dst.mkdir(parents=True)

            print(f"Moving {file_txt.name} to {dst}")
            shutil.move(src=file_txt, dst=dst)


# %%
for challenge_type in ["00", "09", "11", "12"]:

    if challenge_type != "00":
        for challenge_level in ["01", "02", "03", "04", "05"]:
            files = Path("CURE-TSD", challenge_type, challenge_level).rglob("*.jpg")
            split(files)

    else:
        files = Path("CURE-TSD", challenge_type).rglob("*.jpg")
        split(files)

# %%
