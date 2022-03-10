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
).drop_duplicates(["sequence", "frame"])

df_train, df_val = train_test_split(
    df,
    test_size=0.3,
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

# get training/val files
train_files = df_train["file"].to_list()
val_files = df_val["file"].to_list()

# save splits
df_train.to_csv(Path("CURE-TSD", "labels", "train.csv"))
df_val.to_csv(Path("CURE-TSD", "labels", "val.csv"))


# %%
def move_files(files, src, to):

    for file in files:

        # move images
        images_src = Path(src, "images", f"{file}.jpg")
        images_dst = Path(src, "images", to)

        # if the images destination does not exist, create it
        if not images_dst.exists():
            images_dst.mkdir(parents=True)

        print(f"Moving {images_src} to {images_dst}")
        shutil.move(
            src=images_src,
            dst=images_dst,
        )

        # move lables
        labels_src = Path(src, "labels", f"{file}.txt")
        labels_dst = Path(src, "labels", to)

        # if the labels destination does not exist, create it
        if not labels_dst.exists():
            labels_dst.mkdir(parents=True)

        print(f"Moving {labels_src} to {labels_dst}")
        shutil.move(
            src=labels_src,
            dst=labels_dst,
        )


# %%
for challenge_type in ["00", "09", "11", "12"]:

    if challenge_type != "00":
        for challenge_level in ["01", "02", "03", "04", "05"]:

            # create full path
            src = Path("CURE-TSD", challenge_type, challenge_level)

            move_files(files=train_files, src=src, to="train")
            move_files(files=val_files, src=src, to="val")

    else:
        # create full path
        src = Path("CURE-TSD", challenge_type)

        move_files(files=train_files, src=src, to="train")
        move_files(files=val_files, src=src, to="val")

# %%
# get remaining images (these do not have lables)
images = Path("CURE-TSD", "00", "images").glob("*.jpg")

train_images, val_images = train_test_split(
    np.array([image.name for image in images]),
    test_size=0.3,
    shuffle=True,
    random_state=42,
)


# %%
def move_remaining_images(images, src, to):

    for image in images:

        # move images
        images_src = Path(src, image)
        images_dst = Path(src, to)

        print(f"Moving {images_src} to {images_dst}")
        shutil.move(
            src=images_src,
            dst=images_dst,
        )


# %%
for challenge_type in ["00", "09", "11", "12"]:

    if challenge_type != "00":
        for challenge_level in ["01", "02", "03", "04", "05"]:

            # create full path
            src = Path("CURE-TSD", challenge_type, challenge_level, "images")

            move_remaining_images(images=train_images, src=src, to="train")
            move_remaining_images(images=val_images, src=src, to="val")

    else:
        # create full path
        src = Path("CURE-TSD", challenge_type, "images")

        move_remaining_images(images=train_images, src=src, to="train")
        move_remaining_images(images=val_images, src=src, to="val")

# %%
