
TEMPLATE_DIMENSION = 25
TOMOGRAM_DIMENSION = 120
NOISE_GAUSS_PARAM = 0.2 # not in use
NOISE_LINEAR_PARAM = 0.4 # not in use
NOISE_GAUSSIAN_SIZE = 10
NOISE_GAUSSIAN_STDEV = 3
# For correlation search
NEIGHBORHOOD_HALF_SIDE = 5
# Candidate selctor peak detection constants
CORRELATION_THRESHOLD = 10
GAUSSIAN_SIZE = 10
GAUSSIAN_STDEV = 3
# For results metrics - if relative angle < TILT_THRESHOLD then correct tilt
TILT_THRESHOLD = 15
"""
This is used to determine the distance between a correlation peak and a possible Ground Truth that corresponds to it
In our typical configurations, this should be 
2 for non noisy simulations
12 for noisy 2D
16 for noisy 3D
"""
DISTANCE_THRESHOLD = 16

# unused
DEFAULT_COMPOSITION_TUPLES_2D = ((1, 0, 52, 32), (1, 2, 37, 28), (0, 0, 70, 23))
DEFAULT_COMPOSITION_TUPLES_3D = ((1, 0, 52, 32,35), (1, 2, 37, 28,45), (0, 0, 70, 23,45), (0, 9, 70, 23,72))
