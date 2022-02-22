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
            name = Path(
                file.parent,
                f"{file.stem}_{frame_no:03}.jpg",
            )
            print(f"Saving image: {name}")

            cv2.imwrite(str(name), image)

            frame_no += 1

        else:
            cap.release()
            os.remove(file)
            break

# %%
