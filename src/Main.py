"""
Read
"""

TRAINING_SET_SIZE = 10

import CommonDataTypes
import CandidateSelector
import TemplateGenerator
import TomogramGenerator
import Labeler
import FeaturesExractor


def analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector):
    candidates = candidate_selector.select(tomogram)

    for candidate in candidates:
        feature_vector = features_extractor.extract_features(candidate)
        feature_vectors.append(feature_vector)
        # this sets each candidate's label
        labeler.associate_label(candidate, tomogram.composition)
        labels.append(candidate.label)
    return (candidates, feature_vectors, labels)


templates = generate_templates()

#TODO: what about tilting?

candidate_selector = CandidateSelector.CandidateSelector(templates)
features_extractor = FeaturesExractor.FeaturesExractor(templates)


#Training

feature_vectors = []
labels = []



for i in range(TRAINING_SET_SIZE):
    # configuration for tomogram generation
    criteria = ()
    #with a set composition
    tomogram = generate_tomogram(templates, criteria)

    labeler = Labeler.Labeler(tomogram.composition)

    (candidates, single_iteration_feature_vectors, single_iteration_labels) = analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector)
    feature_vectors.extend(single_iteration_feature_vectors)
    labels.extend(single_iteration_labels)



import numpy as np
X = np.array(feature_vectors)
y = np.array(labels)
from sklearn.svm import SVC
svm = SVC()
svm.fit(X, y)

#how to save to disk?



#identification

# configuration for tomogram generation
criteria = ()
#with a set composition
tomogram = generate_tomogram(templates, criteria)

labeler = SvmLabeler(svm)

(candidates, feature_vectors, predicted_labels) = analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector)

#save results

