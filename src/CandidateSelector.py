CORRELATION_THRESHOLD = 50

from CommonDataTypes import *
from scipy import signal
import numpy as np
import PeakDetection

class CandidateSelector:
    def __init__(self, templates):
        self.templates = templates

    def find_local_maxima(self, correlation_array):
        res = np.nonzero(PeakDetection.detect_peaks(correlation_array))
        return [(x[0],x[1],0) for x in zip(res[0],res[1]) if correlation_array[x] > CORRELATION_THRESHOLD]

    def select(self, tomogram):
        positions = []
        for template_tuple in self.templates:
            for tilted in template_tuple:
                correlation = signal.fftconvolve(tomogram.density_map, tilted.density_map, mode='same')
                positions.extend(self.find_local_maxima(correlation))

        candidates = []
        for position in set(positions):
            candidates.append(Candidate(SixPosition(position, tilted.orientation), tilted.template_id))
        return candidates



if __name__ == '__main__':

    from TemplateGenerator import generate_tilted_templates
    from TomogramGenerator import generate_tomogram
    import matplotlib.pyplot as plt

    templates = generate_tilted_templates()
    tomogram = generate_tomogram(templates, None)

    fig, ax = plt.subplots()
    ax.imshow(tomogram.density_map)

    correlation = signal.fftconvolve(tomogram.density_map, templates[1][2].density_map, mode='same')

    fig, ax = plt.subplots()
    ax.imshow(correlation)

    positions = CandidateSelector.find_local_maxima(None, correlation)
    maximums = np.zeros(correlation.shape)
    for position in positions:
        maximums[position] = correlation[position]
    fig, ax = plt.subplots()
    print(len(positions))
    ax.imshow(maximums)

    #plt.show()
