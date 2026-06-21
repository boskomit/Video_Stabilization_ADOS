import numpy as np


def build_transform(dx, dy, da):

    cos = np.cos(da)
    sin = np.sin(da)

    m = np.array([
        [cos, -sin, dx],
        [sin,  cos, dy]
    ], dtype=np.float32)

    return m