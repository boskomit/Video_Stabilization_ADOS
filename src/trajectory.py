import numpy as np

def build_trajectory(transforms):

    """
    Build the trajectory from the list of transformations.
    """

    trajectory = np.cumsum(transforms, axis=0)
    return trajectory