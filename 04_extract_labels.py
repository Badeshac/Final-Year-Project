# %%
import os
from pathlib import Path

import pandas as pd

# %%
# all images have the same dims
image_width = 1628
image_height = 1236

# create a dict that will be used to create a df
data = {
    "label_file": [],
    "image_file": [],
    "sequence": [],
    "frame": [],
    "sign": [],
    "width": [],
    "height": [],
    "area": [],
}

# create a dict to map signs
signs = {
    "01": "speed_limit",
    "02": "goods_vehicles",
    "03": "no_overtaking",
    "04": "no_stopping",
    "05": "no_parking",
    "06": "stop",
    "07": "bicycle",
    "08": "hump",
    "09": "no_left",
    "10": "no_right",
    "11": "priority_to",
    "12": "no_entry",
    "13": "yield",
    "14": "parking",
}

# %%
files = Path("CURE-TSD", "labels").glob("*.txt")

for file in files:

    print(f"Processing {file.name}...")

    sequence_number = file.stem

    with file.open("r") as f:
        lines = f.read().splitlines()

    # skip first line
    for line in lines[1:]:

        # frameNumber_signType_llx_lly_lrx_lry_ulx_uly_urx_ury
        (
            frame_number,
            sign_type,
            llx,
            lly,
            lrx,
            lry,
            ulx,
            uly,
            urx,
            ury,
        ) = line.split("_")

        # get the centre of box
        x_center = (int(llx) + int(lrx)) / 2
        y_center = (int(lly) + int(uly)) / 2

        # get dims
        width = abs(int(llx) - int(lrx))
        height = abs(int(lly) - int(uly))

        # box coordinates must be normalized from 0 - 1
        # divide x_center and width by image width
        x_center_norm = round(x_center / image_width, 6)
        width_norm = round(width / image_width, 6)

        # divide y_center and height by image height
        y_center_norm = round(y_center / image_height, 6)
        height_norm = round(height / image_height, 6)

        # class numbers should be zero-indexed (start from 0)
        class_number = int(sign_type) - 1

        # concatenate each row as:
        # class_number x_center y_center width height
        row = f"{class_number} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n"

        print(row)

        # save output as:
        # sequenceNumber_frameNumber.txt

        dst = Path(
            "CURE-TSD",
            "labels",
            f"{sequence_number}_{frame_number}{file.suffix}",
        )

        print(dst)

        # if file exists, it will be opened and the row appended
        # otherwise, file will be created, opened and the row appended
        # 'a' opens the file for appending and data is written to the end automatically
        with dst.open("a") as f:
            f.write(row)

        data["label_file"].append(f"{sequence_number}_{frame_number}.txt")
        data["image_file"].append(f"{sequence_number}_{frame_number}.jpg")
        data["sequence"].append(sequence_number)
        data["frame"].append(frame_number)
        data["sign"].append(signs[sign_type])
        data["width"].append(width_norm)
        data["height"].append(height_norm)
        data["area"].append(width_norm * height_norm)

    # remvoe file after extracting its frames
    os.remove(file)

# %%
df = pd.DataFrame(data).sort_values(
    by=["sequence", "frame"],
    ignore_index=True,
)

df.to_csv(Path("CURE-TSD", "labels", "lables.csv"))

# %%
