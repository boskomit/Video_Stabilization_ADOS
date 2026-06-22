import cv2
from pathlib import Path
import numpy as np

from motion_estimation import estimate_motion
from trajectory import build_trajectory
from smoothing import smooth_trajectory_with_gaussian
from stabilization import build_transform

def fix_border(frame):

    h, w = frame.shape[:2]

    T = cv2.getRotationMatrix2D((w / 2, h / 2), 0, 1.05)

    return cv2.warpAffine(frame, T, (w, h), flags=cv2.INTER_CUBIC)


BASE_DIR = Path(__file__).resolve().parent.parent

VIDEO_PATH = BASE_DIR / "videos" / "unstable" / "1.avi"

video_name = VIDEO_PATH.stem

OUTPUT_PATH = BASE_DIR / "output" / f"{video_name}_stabilized.avi"


cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    print(f"Cannot open video: {VIDEO_PATH}")
    exit()

ret, prev_frame = cap.read()

if not ret:
    print("Cannot read first frame")
    exit()

transforms = []

while True:

    ret, curr_frame = cap.read()

    if not ret:
        break

    dx, dy, da = estimate_motion(prev_frame, curr_frame)

    transforms.append([dx,dy,da])

    prev_frame = curr_frame


fps = cap.get(cv2.CAP_PROP_FPS)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap.release()


transforms = np.array(transforms)

trajectory = build_trajectory(transforms)

smoothed_trajectory = smooth_trajectory_with_gaussian(trajectory, sigma=15)

diff_trajectory = (smoothed_trajectory - trajectory)

transforms_smooth = (transforms + diff_trajectory)


cap = cv2.VideoCapture(str(VIDEO_PATH))

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(str(OUTPUT_PATH), fourcc, fps, (width, height))

frame_idx = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    if frame_idx >= len(transforms_smooth):
        break

    dx, dy, da = transforms_smooth[frame_idx]

    m = build_transform(dx,dy,da)

    stabilized = cv2.warpAffine(frame, m, (width, height), borderMode=cv2.BORDER_REPLICATE)

    stabilized = fix_border(stabilized)

    border = 20

    stabilized = stabilized[border:height-border, border:width-border]

    stabilized = cv2.resize(stabilized, (width, height), interpolation=cv2.INTER_CUBIC)

    out.write(stabilized)

    frame_idx += 1


cap.release()
out.release()

print(f"Video saved: {OUTPUT_PATH}")