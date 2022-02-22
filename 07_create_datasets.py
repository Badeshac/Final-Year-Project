# %%
from pathlib import Path

from yaml import dump

# %%
data = {
    "nc": 14,
    "names": [
        "0-speed_limit",
        "1-goods_vehicles",
        "2-no_overtaking",
        "3-no_stopping",
        "4-no_parking",
        "5-stop",
        "6-bicycle",
        "7-hump",
        "8-no_left",
        "9-no_right",
        "10-priority_to",
        "11-no_entry",
        "12-yield",
        "13-parking",
    ],
}

# %%
for challenge_type in ["00", "09", "11", "12"]:

    if challenge_type != "00":
        for challenge_level in ["01", "02", "03", "04", "05"]:

            path = Path("CURE-TSD", challenge_type, challenge_level)

            data["train"] = str(Path(path, "images", "train"))
            data["val"] = str(Path(path, "images", "val"))

            with Path(path, "dataset.yaml").open("w") as stream:
                dump(data, stream)

    else:
        path = Path("CURE-TSD", challenge_type)

        data["train"] = str(Path(path, "images", "train"))
        data["val"] = str(Path(path, "images", "val"))

        with Path(path, "dataset.yaml").open("w") as stream:
            dump(data, stream)

# %%
