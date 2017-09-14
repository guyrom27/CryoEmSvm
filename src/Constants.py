


"""
The label that corresponds to NOTHING_IS_HERE
"""
JUNK_ID = -1


TOMOGRAM_DIMENSION = 120
TEMPLATE_DIMENSION = 25
NEIGHBORHOOD_HALF_SIDE = 5  # for correlations search

TILT_THRESHOLD = 15  # For results metrics - if relative angle < TILT_THRESHOLD then correct tilt

"""
Candidate selctor peak detection constants 
"""
CORRELATION_THRESHOLD = 10
GAUSSIAN_SIZE = 10
GAUSSIAN_STDEV = 3

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


class Constants:
    def __init__(self):
        """
        Candidate selctor peak detection constants
        """

        self.dim = 2
        self.template_side = 25
        self.tomogram_side = 120

        self.tomogram_noise = False
        self.tomogram_noise_value = 5

        self.correlations_neighborhood_half_side = 5

        self.selector_correlation_threshold = 10
        self.selector_gaussian_size = 10
        self.selector_gaussian_stdev = 3

        """
        This is used to determine the distance between a correlation peak and a possible Ground Truth that corresponds to it
        In our typical configurations, this should be 
        2 for non noisy simulations
        12 for noisy 2D
        16 for noisy 3D
        """
        self.labeler_distance_threshold = 16

        self.metrics_tilt_threshold = 15 #For results metrics - if relative angle < TILT_THRESHOLD then correct tilt




CONSTANTS = Constants()