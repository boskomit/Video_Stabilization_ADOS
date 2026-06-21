import cv2
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from motion_estimation import estimate_motion
from trajectory import build_trajectory
from plot_trajectory import plot_trajectory
from smoothing import smooth_trajectory
from stabilization import build_transform

def fix_border(frame):

    h, w = frame.shape[:2]

    T = cv2.getRotationMatrix2D(
        (w/2, h/2),
        0,
        1.05
    )

    return cv2.warpAffine(
        frame,
        T,
        (w, h)
    )

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_PATH = BASE_DIR / "videos" / "unstable" / "1.avi"
OUTPUT_PATH = BASE_DIR / "output" / "stabilized.avi"

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
smoothed_trajectory = smooth_trajectory(trajectory, radius=30)
diff_trajectory = smoothed_trajectory - trajectory
transforms_smooth = transforms + diff_trajectory
print(trajectory.shape)
#plot_trajectory(trajectory)

plt.figure(figsize=(12,6))

plt.plot(
    trajectory[:,0],
    label="Original X"
)

plt.plot(
    smoothed_trajectory[:,0],
    label="Smoothed X"
)

plt.plot(
    diff_trajectory[:,0],
    label="Correction X"
)

plt.legend()
plt.grid()
#plt.show()


cap.release()

cap = cv2.VideoCapture(str(VIDEO_PATH))

fps = cap.get(cv2.CAP_PROP_FPS)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(
    str(OUTPUT_PATH),
    fourcc,
    fps,
    (width, height)
)

frame_idx = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    if frame_idx >= len(diff_trajectory):
        break

    # Probaj prvo sa difference
    dx, dy, da = transforms_smooth[frame_idx]

    m = build_transform(
        dx,
        dy,
        da
    )

    stabilized = cv2.warpAffine(
        frame,
        m,
        (width, height),
        borderMode=cv2.BORDER_REPLICATE
    )

    # Crop da uklonimo crne ivice
    border = 20

    stabilized = stabilized[
        border:height-border,
        border:width-border
    ]

    stabilized = cv2.resize(
        stabilized,
        (width, height)
    )

    out.write(stabilized)

    cv2.imshow("Stabilized", stabilized)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    frame_idx += 1


cap.release()
out.release()

cv2.destroyAllWindows()

print(f"Video saved: {OUTPUT_PATH}")


