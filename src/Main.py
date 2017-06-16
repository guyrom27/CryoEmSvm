"""
Read
"""

TRAINING_SET_SIZE = 10

JUNK_ID = 0

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
        label = labeler.associate_label(candidate)
        candidate.set_label(label)
        labels.append(label)
    return (candidates, feature_vectors, labels)








#this is tuple of tuples of TiltedTemplates (each group has the same template_id)
templates = TemplateGenerator.generate_tilted_templates()
#save templates to files

candidate_selector = CandidateSelector.CandidateSelector(templates)
features_extractor = FeaturesExractor.FeaturesExractor(templates)


#Training

feature_vectors = []
#a label is a template_id, where 0 is junk
labels = []



for i in range(TRAINING_SET_SIZE):
    # configuration for tomogram generation
    criteria = (2,0)
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

#test results

ground_truth_labeler = PositionLabeler(tomogram.composition)

#junk was identified as non junk
false_positive = 0
#non junk was identified as junk
false_negative = 0
#non junk was identified as a wrong template
false_identification = 0

#non junk was accurately identified
true_identification = 0
#junk was accurately identified
true_rejection = 0

for candidate in candidates:
    true_label = ground_truth_labeler.label(candidate)
    predicted_label = candidate.label
    if (true_label == JUNK_ID):
        if (predicted_label == JUNK_ID):
            true_rejection += 1
        else:
            false_positive += 1
    else:
        if (predicted_label == true_label):
            true_identification += 1
        elif (predicted_label == JUNK_ID):
            false_negative += 1
        else:
            false_identification += 1


success = true_identification + true_rejection

#print SVM statistics
print("SVM error rate= " + (len(candidates) - success) / len(candidates))



#save results

