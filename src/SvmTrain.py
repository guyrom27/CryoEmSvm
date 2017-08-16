from sklearn.svm import SVC
import numpy as np

from TemplateMaxCorrelations import TemplateMaxCorrelations
import CandidateSelector
import FeaturesExtractor
import Labeler
import TiltFinder

from AnalyzeTomogram import analyze_tomogram


def svm_train(templates, tomograms, return_tomograms=False):
    """
    Create and return a new SVM trained on the templates and tomograms supplied. If return_toomgram is true then the
    list of the tomograms will also be returned.
    :param templates_generator  Source of the templates. Can be a list or a generator of the templates.
    :param tomogram_generator   Source of the tomograms. Can be a list or a generator of the tomograms.
    :param return_tomograms     Boolean value indicating whether the tomograms used should be returned as well.
    :return A tuple of the resulting SVM and the templates used to train it. If return_tomograms is true then the tuple
            of the SVM and templates will be within another tuple containing the tomograms as it's second value.
    """

    # Initialize variables for the feature vectors and the labels
    feature_vectors = []
    # a label is a template_id, where -1 is junk
    labels = []

    # Generate the training set
    for tomogram in tomograms:
        labeler = Labeler.PositionLabeler(tomogram.composition)
        max_correlations = TemplateMaxCorrelations(tomogram, templates)
        candidate_selector = CandidateSelector.CandidateSelector(max_correlations)
        features_extractor = FeaturesExtractor.FeaturesExtractor(max_correlations)
        tilt_finder = TiltFinder.TiltFinder(max_correlations)

        (candidates, single_iteration_feature_vectors, single_iteration_labels) = \
            analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector, tilt_finder)

        feature_vectors.extend(single_iteration_feature_vectors)
        labels.extend(single_iteration_labels)

    # Create new svm
    svm = SVC()

    # Train svm
    x = np.array(feature_vectors)
    y = np.array(labels)
    if len(np.unique(y)) == 1:
        print("SVM training must contain more than one label type (all candidates are the same label)")
        exit()
    svm.fit(x, y)

    # Return the svm
    return (svm, templates)