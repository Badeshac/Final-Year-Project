# %%
import shutil
from pathlib import Path
import os

# %%
# change file name from sequenceType_sequenceNumber.txt to sequenceNumber.txt

files = Path("CURE-TSD", "labels").glob("*.txt")

for file in files:

    print(file.name)

    sequence_type, sequence_number = file.stem.split("_")

    if sequence_type == "01":

        print(f"Renaming {file.name}...")

        dst = Path(
            "CURE-TSD",
            "labels",
            f"{sequence_number}{file.suffix}",
        )

        shutil.move(src=file, dst=dst)

    else:
        os.remove(file)

# %%
