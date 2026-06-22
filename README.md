# Video Stabilization using ORB Feature Matching

A simple video stabilization pipeline implemented in Python using OpenCV.

The project estimates camera motion between consecutive video frames using ORB feature detection and matching, reconstructs the camera trajectory, smooths the trajectory using a Gaussian filter, and generates a stabilized output video by applying corrected affine transformations.

## Features

* ORB feature detection and description
* Feature matching using BFMatcher
* Camera motion estimation (translation and rotation)
* Trajectory reconstruction
* Gaussian trajectory smoothing
* Affine transformation-based stabilization
* Output video generation
* Trajectory visualization for analysis

## Project Structure

```text
project/
│
├── src/
│   ├── main.py
│   ├── motion_estimation.py
│   ├── trajectory.py
│   ├── smoothing.py
│   └── stabilization.py
│
├── videos/
│   ├── unstable/
│   └── stable/
│
├── output/
│
└── README.md
```

## Method Overview

### 1. Motion Estimation

For each pair of consecutive frames:

* ORB keypoints are detected
* Descriptors are computed
* Features are matched using BFMatcher
* An affine transformation is estimated

The transformation provides:

* Horizontal translation (`dx`)
* Vertical translation (`dy`)
* Rotation angle (`da`)

### 2. Trajectory Reconstruction

Frame-to-frame transformations are accumulated over time to obtain the camera trajectory.

### 3. Trajectory Smoothing

A Gaussian filter is applied to the trajectory in order to remove high-frequency jitter while preserving the overall camera motion.

### 4. Stabilization

The difference between the original and smoothed trajectories is used to generate corrected transformations.

Each frame is then warped using OpenCV's affine transformation functions to produce a stabilized video sequence.

## Requirements

* Python 3.10+
* OpenCV
* NumPy
* Matplotlib
* SciPy

Install dependencies:

```bash
pip install opencv-python numpy matplotlib scipy
```

## Usage

Place input videos inside:

```text
videos/unstable/
```

Then run:

```bash
python src/main.py
```

The stabilized video will be saved to:

```text
output/
```

with the naming format:

```text
<video_name>_stabilized.avi
```

Example:

```text
1.avi
→
1_stabilized.avi
```

## Example Pipeline

```text
Input Video
      ↓
ORB Feature Detection
      ↓
Feature Matching
      ↓
Motion Estimation
      ↓
Trajectory Reconstruction
      ↓
Gaussian Smoothing
      ↓
Motion Correction
      ↓
Frame Warping
      ↓
Stabilized Video
```

## Future Improvements

Potential extensions include:

* Lucas-Kanade Optical Flow
* Adaptive trajectory smoothing
* Automatic cropping
* Real-time stabilization
* GPU acceleration

## License

This project is intended for educational and research purposes.
