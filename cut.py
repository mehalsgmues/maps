import os
import re
import sys
from glob import glob
from pathlib import Path

import cv2

zooms = map(int, sys.argv[1:])  # [13, 14, 15, 16, 17, 18]

cwd = Path.cwd()

pattern = r'x(\d+)-(\d+)_y(\d+)-(\d+)\.png$'

for zoom in zooms:
    print(zoom)
    os.chdir(cwd)
    input_file = glob(f'z{zoom}_*.png')[0]
    match = re.search(pattern, input_file)
    if not match:
        raise ValueError(f"Could not parse name of file {input_file}")
    x_start, x_end, y_start, y_end = map(int, match.groups())
    img = cv2.imread(input_file)
    width = img.shape[0]
    height = img.shape[1]
    for y, r in enumerate(range(0, width, 256)):
        if y_start + y > y_end:
            break
        for x, c in enumerate(range(0, height, 256)):
            if x_start + x > x_end:
                break
            p = cwd / "tiles" / str(zoom) / str(x_start + x)
            p.mkdir(parents=True, exist_ok=True)
            os.chdir(p)
            cv2.imwrite(f"{y_start + y}.png", img[r:r + 256, c:c + 256, :])
