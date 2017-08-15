from scipy import signal
import numpy as np


class TemplateMaxCorrelations:
    """
    correlation_values is a list of length len(templates) each element is a Tomogram sized matrix containing the max correlation for each point to this template (over all tilts)
    best_tilts is a list of length len(templates) each element is a Tomogram sized matrix containing the tilt_id that resulted with the max correlation
    """

    def __init__(self, tomogram, templates):
        self.correlation_values = []
        self.best_tilt_ids = []
        for template_group in templates:
            max_correlation = np.zeros(tomogram.density_map.shape)
            max_correlation_tilt_id = np.zeros(max_correlation.shape, dtype = int)
            for tilted_template in template_group:
                correlation = signal.fftconvolve(tomogram.density_map, tilted_template.density_map, mode='same')
                max_correlation = np.maximum(correlation, max_correlation)
                max_correlation_tilt_id[max_correlation == correlation] = tilted_template.tilt_id
            self.correlation_values.append(max_correlation)
            self.best_tilt_ids.append(max_correlation_tilt_id)


