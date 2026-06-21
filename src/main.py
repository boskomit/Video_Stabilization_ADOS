import cv2
from pathlib import Path
import numpy as np

from motion_estimation import estimate_motion
from trajectory import build_trajectory
from plot_trajectory import plot_trajectory

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_PATH = BASE_DIR / "videos" / "unstable" / "1.avi"

#print(VIDEO_PATH)
#print(VIDEO_PATH.exists())

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    print(f"Cannot open video: {VIDEO_PATH}")
    exit()

frame_count = 0

ret, prev_frame = cap.read()

transforms = []

while True:
    ret, curr_frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    dx, dy, da = estimate_motion(prev_frame, curr_frame)

    transforms.append([dx, dy, da])

    print(f"dx={dx:.2f}, dy={dy:.2f}, da={da:.4f}")

    prev_frame = curr_frame

    cv2.imshow("Original Video", curr_frame)
    
    if cv2.waitKey(25) & 0xFF == 27:
        break

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Rezolucija: {width}x{height}")
print(f"FPS: {fps}")
print(f"Broj frejmova: {frames}")

transforms = np.array(transforms)
trajectory = build_trajectory(transforms)

print(trajectory.shape)
plot_trajectory(trajectory)


cap.release()
cv2.destroyAllWindows()
