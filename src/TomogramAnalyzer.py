from TemplateMaxCorrelations import TemplateMaxCorrelations
from CandidateSelector import CandidateSelector
from FeaturesExtractor import FeaturesExtractor
from TiltFinder import TiltFinder

class TomogramAnalyzer:
    def __init__(self, tomogram, templates, labeler):
        self.tomogram = tomogram
        self.templates = templates
        self.labeler = labeler
        self.max_correlations = None

    def analyze(self, set_labels=False):
        print('\tcaclualting correlations')
        self.max_correlations = TemplateMaxCorrelations(self.tomogram, self.templates)

        candidate_selector = CandidateSelector(self.max_correlations)
        features_extractor = FeaturesExtractor(self.max_correlations)
        tilt_finder = TiltFinder(self.max_correlations)

        print('\tselecting candidates')
        candidates = candidate_selector.select(self.tomogram)
        feature_vectors = []
        labels = []

        print('\tlabeling and extracting features')
        for candidate in candidates:
            feature_vectors.append(features_extractor.extract_features(candidate))
            # this sets each candidate's label
            labels.append(self.labeler.label(candidate, set_label=set_labels))
            tilt_finder.find_best_tilt(candidate)

        return candidates, feature_vectors, labels