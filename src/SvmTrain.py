from Labeler import PositionLabeler
from AnalyzeTomogram import analyze_tomogram

from sklearn.svm import SVC
import numpy as np


def svm_train(templates, tomograms):
    """
    Create and return a new SVM trained on the templates and tomograms supplied
    :param templates:   Source of the templates - Iterator with random access
    :param tomograms:   Iterator of training set tomograms
    :return A tuple of the resulting SVM and the templates used to train it
    """

    # Initialize variables for the feature vectors and the labels
    feature_vectors = []
    # a label is a template_id, where -1 is junk
    labels = []

    # Generate the training set
    for tomogram in tomograms:
        labeler = PositionLabeler(tomogram.composition)
        (candidates, single_iteration_feature_vectors, single_iteration_labels) = \
            analyze_tomogram(tomogram, templates, labeler)
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

    return (svm, templates)