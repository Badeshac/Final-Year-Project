# %%
import shutil
from pathlib import Path


# %%
def create_folders(folder_name):
    """create a folder in "CURE-TSD" for a weather condition and a sub-folder for each level."""

    if not Path("CURE-TSD", folder_name).exists():
        Path("CURE-TSD", folder_name).mkdir(parents=True)

    # create 5 sub-folders in each folder
    # do not create sub-folders for 00 folder (No-challenge)
    if folder_name != "00":
        for sub_folder_name in ["01", "02", "03", "04", "05"]:
            if not Path("CURE-TSD", folder_name, sub_folder_name).exists():
                Path("CURE-TSD", folder_name, sub_folder_name).mkdir(parents=True)


# {"00": "No-challenge", "09": "Rain", "11": "Snow", "12": "Haze"}
create_folders("00")
create_folders("09")
create_folders("11")
create_folders("12")


# %%
def move_file(file, folder_name, sub_folder_name, sequence_number):
    """move file to folder_name > sub_folder_name > sequence_number.mp4"""

    # 00 folder (No-challenge) does not have sub-folders
    if folder_name != "00":

        print(f"Moving {file.name} to {folder_name}>{sub_folder_name}")

        dst = Path(
            "CURE-TSD",
            folder_name,
            sub_folder_name,
            f"{sequence_number}{file.suffix}",
        )

    else:

        print(f"Moving {file.name} to {folder_name}")

        dst = Path(
            "CURE-TSD",
            folder_name,
            f"{sequence_number}{file.suffix}",
        )

    shutil.move(src=file, dst=dst)


# %%
# move each file to folder_name > sub_folder_name

files = Path("CURE-TSD", "data").glob("*.mp4")

for file in files:

    print(file.name)

    (
        sequence_type,
        sequence_number,
        challenge_source_type,
        challenge_type,
        challenge_level,
    ) = file.stem.split("_")

    # move files to different folders if it's real data
    # rename to sequence_number.mp4
    if sequence_type == "01":

        if challenge_type in ["00", "09", "11", "12"]:

            move_file(
                file,
                folder_name=challenge_type,
                sub_folder_name=challenge_level,
                sequence_number=sequence_number,
            )


# %%
