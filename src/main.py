import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_PATH = BASE_DIR / "videos" / "unstable" / "1.avi"

print(VIDEO_PATH)
print(VIDEO_PATH.exists())

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    print(f"Cannot open video: {VIDEO_PATH}")
    exit()

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow("Original Video", frame)
    frame_count += 1

    key = cv2.waitKey(25)

    if key == 27:  # ESC key
        break

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Rezolucija: {width}x{height}")
print(f"FPS: {fps}")
print(f"Broj frejmova: {frames}")

cap.release()
cv2.destroyAllWindows()

print("Total frames processed:", frame_count)