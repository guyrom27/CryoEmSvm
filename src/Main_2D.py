import matplotlib.pyplot as plt

import CandidateSelector
import TemplateGenerator
import TomogramGenerator
import Labeler
import FeaturesExtractor

def analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector):
    candidates = candidate_selector.select(tomogram)
    feature_vectors = []
    labels = []
    for candidate in candidates:
        feature_vector = features_extractor.extract_features(tomogram, candidate)
        feature_vectors.append(feature_vector)
        candidate.set_features(feature_vector)
        # this sets each candidate's label
        label = labeler.label(candidate)
        candidate.set_label(label)
        labels.append(label)
    return (candidates, feature_vectors, labels)

#this is tuple of tuples of TiltedTemplates (each group has the same template_id)
templates = TemplateGenerator.generate_tilted_templates_2d()
#save templates to files

candidate_selector = CandidateSelector.CandidateSelector(templates)
features_extractor = FeaturesExtractor.FeaturesExtractor(templates)

tomogram = TomogramGenerator.generate_tomogram_2d(templates, ((1,0,10,10),(1,2,27,18),(0,0,10,28)))
fig, ax = plt.subplots()
ax.imshow(tomogram.density_map[:,:,0])

labeler = Labeler.PositionLabeler(tomogram.composition)
(candidates, single_iteration_feature_vectors, single_iteration_labels) = analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector)

plt.show()