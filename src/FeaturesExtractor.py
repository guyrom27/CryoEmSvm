from scipy import signal


class FeaturesExtractor:
    def __init__(self, max_correlations):
        """
        :param max_correlations: a data structure of type TemplateMaxCorrelations initialized according to the relevant tomogram and templates
        """
        self.max_correlations = max_correlations

    def extract_features(self, candidate, set_features=True):
        features_vector = [correlation_values[candidate.six_position.COM_position] for correlation_values in self.max_correlations.correlation_values]
        if set_features:
            candidate.set_features(features_vector)
        return features_vector

    # def __init__(self, templates):
    #     self.templates = templates
    #
    # def extract_features(self, tomogram, candidate, set_features=True):
    #     features_vector = []
    #     for template_group in self.templates:
    #         max_correlation = 0
    #         for tilted_template in template_group:
    #             correlation = signal.fftconvolve(tomogram.density_map, tilted_template.density_map, mode='same')
    #             #pos = tuple([candidate.six_position.COM_position[0], candidate.six_position.COM_position[1]])
    #             max_correlation = max(max_correlation, correlation[candidate.six_position.COM_position])
    #         features_vector.append(max_correlation)
    #     if set_features:
    #         candidate.set_features(features_vector)
    #     return features_vector

if __name__ == '__main__':
    print("HI")