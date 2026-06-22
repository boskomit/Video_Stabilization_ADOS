import cv2
import numpy as np

orb = cv2.ORB_create(
    nfeatures=500
)

matcher = cv2.BFMatcher(
    cv2.NORM_HAMMING,
    crossCheck=True
)


def estimate_motion(prev_frame, curr_frame):

    prev_gray = cv2.cvtColor(
        prev_frame,
        cv2.COLOR_BGR2GRAY
    )

    curr_gray = cv2.cvtColor(
        curr_frame,
        cv2.COLOR_BGR2GRAY
    )

    kp1, des1 = orb.detectAndCompute(
        prev_gray,
        None
    )

    kp2, des2 = orb.detectAndCompute(
        curr_gray,
        None
    )

    if des1 is None or des2 is None:
        return 0, 0, 0

    matches = matcher.match(
        des1,
        des2
    )

    if len(matches) < 10:
        return 0, 0, 0

    pts1 = np.float32([
        kp1[m.queryIdx].pt
        for m in matches
    ])

    pts2 = np.float32([
        kp2[m.trainIdx].pt
        for m in matches
    ])

    M, _ = cv2.estimateAffinePartial2D(
        pts1,
        pts2
    )

    if M is None:
        return 0, 0, 0

    dx = M[0, 2]
    dy = M[1, 2]

    da = np.arctan2(
        M[1, 0],
        M[0, 0]
    )

    return dx, dy, da