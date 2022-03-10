# %%
import os
from pathlib import Path

import cv2

# %%
files = Path("CURE-TSD").rglob("*.mp4")

for file in files:

    print(file)

    cap = cv2.VideoCapture(str(file))

    # there are 300 frames in each video sequence
    frame_no = 1

    while True:

        # grab, decode and return the next video frame
        # if no frames has been grabbed retval will be false and the image will be empty
        retval, image = cap.read()

        if retval:

            # write extracted frame as an image
            dst = Path(
                file.parent,
                "images",
                f"{file.stem}_{frame_no:03}.jpg",
            )

            # if the destination does not exist, create it
            if not dst.parent.exists():
                dst.parent.mkdir(parents=True)

            print(f"Saving image: {dst}")

            cv2.imwrite(str(dst), image)

            frame_no += 1

        else:
            cap.release()
            os.remove(file)
            break

# %%
