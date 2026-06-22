import numpy as np
from scipy.ndimage import gaussian_filter1d


def moving_average(curve, radius):

    window_size = 2 * radius + 1
    # Define the filter
    f = np.ones(window_size)/window_size
    # Add padding to the boundaries
    curve_pad = np.pad(curve, (radius, radius), 'edge')
    # Apply convolution
    curve_smoothed = np.convolve(curve_pad, f, mode='same')
    # Remove padding
    curve_smoothed = curve_smoothed[radius:-radius]
    # return smoothed curve
    return curve_smoothed

def smooth_trajectory(trajectory, radius=30):

    smoothed_trajectory = np.copy(trajectory)

    for i in range(3):
        smoothed_trajectory[:,i] = moving_average(trajectory[:,i], radius=radius)

    return smoothed_trajectory

def smooth_trajectory_with_gaussian(trajectory, sigma=15):

    smoothed_trajectory = np.copy(trajectory)
    
    for i in range(3):
        smoothed_trajectory[:,i] = gaussian_filter1d(trajectory[:,i], sigma=sigma)

    return smoothed_trajectory