def analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector, tilt_finder, set_labels=False):
    candidates = candidate_selector.select(tomogram)
    feature_vectors = []
    labels = []

    for candidate in candidates:
        feature_vectors.append(features_extractor.extract_features(candidate))
        # this sets each candidate's label
        labels.append(labeler.label(candidate, set_label=set_labels))
        tilt_finder.find_best_tilt(tomogram, candidate)

    return candidates, feature_vectors, labels
