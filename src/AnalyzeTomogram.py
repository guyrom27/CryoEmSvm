from TemplateMaxCorrelations import TemplateMaxCorrelations
from CandidateSelector import CandidateSelector
from FeaturesExtractor import FeaturesExtractor
from TiltFinder import TiltFinder

def analyze_tomogram(tomogram, templates, labeler, set_labels=False):
    print('caclualting correlations')
    max_correlations = TemplateMaxCorrelations(tomogram, templates)

    print('analyzing tomogram')
    candidate_selector = CandidateSelector(max_correlations)
    features_extractor = FeaturesExtractor(max_correlations)
    tilt_finder = TiltFinder(max_correlations)

    candidates = candidate_selector.select(tomogram)
    feature_vectors = []
    labels = []

    for candidate in candidates:
        feature_vectors.append(features_extractor.extract_features(candidate))
        # this sets each candidate's label
        labels.append(labeler.label(candidate, set_label=set_labels))
        tilt_finder.find_best_tilt(candidate)

    return candidates, feature_vectors, labels


