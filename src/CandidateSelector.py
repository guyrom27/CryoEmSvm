from scipy import signal
import numpy as np

from CommonDataTypes import Candidate, SixPosition
import PeakDetection

# now they are arbitrary values
KERNEL_GAUSSIAN = 'GAUSSIAN'
CORRELATION_THRESHOLD = 10
GAUSSIAN_SIZE = 10
GAUSSIAN_STDEV = 3


def create_kernel(name, dim):
    """
    Creats a kernel of the specified kind and dimension.
    :param name: Kind of kernel to create. Only KERNEL_GAUSSIAN at the moment.
    :param dim: Dimension of the kernel. Only 2 of 3.
    :return: 3 dimensional ndarray where the third dimension is of size 1 for the 2D case.
    """
    if KERNEL_GAUSSIAN == name:
        base = signal.gaussian(GAUSSIAN_SIZE, GAUSSIAN_STDEV)
        if 2 == dim:
            return np.outer(base, base).reshape(len(base), len(base), 1)
        elif 3 == dim:
            plane = np.outer(base, base).reshape(len(base), len(base), 1)
            kernel = np.outer(base, plane[0]).reshape(len(base), len(base), 1)
            for row in plane[1:]:
                kernel = np.concatenate((kernel, np.outer(base, row).reshape(len(base), len(base), 1)), 2)
            return kernel
        else:
            raise NotImplementedError('Dimension can\'t be %d! (only 2 or 3)' % dim)
    else:
        raise NotImplementedError('No kernel option %s!' % name)


class CandidateSelector:
    """
    Selects Candidates for later detection using correlation-
    for each point in the tomogram, try all the different templates and tilts, assign a max_correlation to each point.
    apply a blurring transformation to the max_correlation image (to unite close peaks), and then search for peaks
    """

    def __init__(self, max_correlations, template_shape, dim=2):
        self.max_correlations = max_correlations
        self.dim = dim
        self.kernel = create_kernel(KERNEL_GAUSSIAN, dim=dim)

        self.template_shape = template_shape

        # these are for debug
        self.max_correlation_per_3loc = None
        self.blurred_correlation_array = None
        self.positions = None


    def find_local_maxima(self, correlation_array):
        """
        Generates a list of coordinates of peaks that are greater than the threshold.
        :param correlation_array: The array of the correlation.
        :return: A list of the coordinates of the picks.
        """
        # Blur the correlation to remove close peaks.
        self.blurred_correlation_array = signal.fftconvolve(correlation_array, self.kernel, mode='same')

        # Return all the peaks that are more than the threshold
        res = np.transpose(np.nonzero(PeakDetection.detect_peaks(self.blurred_correlation_array, 3, 3)))
        return [tuple(x) for x in res if self.blurred_correlation_array[tuple(x)] > CORRELATION_THRESHOLD]

    def filter_boundary_positions(self, positions):
        """
        remove positions that are too close to the sides- causes problems further down
        :param positions: a list of 3tuples
        :return: the filtered list
        """
        side = np.array([x//2 + 3 for x in self.template_shape])
        if self.template_shape[2] == 1:
            side[2] = 0
        tom_side = self.max_correlations.correlation_values[0].shape[0]
        filt = lambda pos: (pos-side >= 0).all() and (pos+side < tom_side).all()
        return  [pos for pos in positions if filt(np.array(pos))]

    def select(self, tomogram):
        """
        Find candidates for the template positions using max correlation.
        :param tomogram: The tomogram to search in
        :return: a list of candidates
        """
        self.max_correlation_per_3loc = self.max_correlations.correlation_values[0]
        for correlation_values in self.max_correlations.correlation_values:
            self.max_correlation_per_3loc = np.maximum(self.max_correlation_per_3loc, correlation_values)
        self.positions = self.find_local_maxima(self.max_correlation_per_3loc)
        return [Candidate(SixPosition(position, None), None) for position in self.filter_boundary_positions(self.positions)]


if __name__ == '__main__':
    pass