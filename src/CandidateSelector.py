
from CommonDataTypes import *
from scipy import signal
import numpy as np
from scipy.signal import argrelextrema
import PeakDetection

class CandidateSelector:
    def __init__(self, templates):
        self.templates = templates

    def find_local_maxima(self, correlation_array):
        res = np.nonzero(PeakDetection.detect_peaks(correlation_array))
        return [x for x in zip(res[0],res[1])]

    def select(self, tomogram):
        candidates = []
        for template_tuple in self.templates:
            for tilted in template_tuple:
                correlation = signal.fftconvolve(tomogram.density_map, tilted.density_map, mode='same')
                positions = self.find_local_maxima(correlation)
                for position in positions:
                    candidates.append(Candidate(SixPosition(position, tilted.orientation), tilted.template_id))









