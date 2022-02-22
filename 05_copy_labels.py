# %%
import os
import shutil
from pathlib import Path


# %%
def copy_file(file, folder_name, sub_folder_name):
    """move file to folder_name > sub_folder_name"""

    # 00 folder (No-challenge) does not have sub-folders
    if folder_name != "00":

        dst = Path(
            "CURE-TSD",
            folder_name,
            sub_folder_name,
            f"{file.name}",
        )

        print(f"Copying {file.name} to {dst}")

    else:

        dst = Path(
            "CURE-TSD",
            folder_name,
            f"{file.name}",
        )

        print(f"Copying {file.name} to {dst}")

    shutil.copy(src=file, dst=dst)


# %%
files = Path("CURE-TSD", "labels").glob("*.txt")

for file in files:
    for folder_name in ["00", "09", "11", "12"]:
        for sub_folder_name in ["01", "02", "03", "04", "05"]:

            copy_file(file, folder_name, sub_folder_name)

    # remove file
    os.remove(file)

# %%
