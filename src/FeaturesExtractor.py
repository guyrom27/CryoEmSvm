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


if __name__ == '__main__':
    pass