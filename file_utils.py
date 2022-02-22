# %%
import shutil
from pathlib import Path


# %%
def move_files(ext, folder):
    # move images to the images folder for each challenge level
    for challenge_type in ["00", "09", "11", "12"]:

        if challenge_type != "00":
            for challenge_level in ["01", "02", "03", "04", "05"]:

                files = Path(
                    "CURE-TSD",
                    challenge_type,
                    challenge_level,
                ).rglob(f"*.{ext}")

                for file in files:
                    shutil.move(
                        src=file,
                        dst=Path("CURE-TSD", challenge_type, challenge_level, folder),
                    )

        else:
            files = Path(
                "CURE-TSD",
                challenge_type,
            ).rglob(f"*.{ext}")

            for file in files:
                shutil.move(
                    src=file,
                    dst=Path("CURE-TSD", challenge_type, folder),
                )


# %%
move_files(ext="jpg", folder="images")
move_files(ext="txt", folder="labels")
