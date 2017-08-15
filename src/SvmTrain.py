from sklearn.svm import SVC
import numpy as np
import pickle

from TemplateMaxCorrelations import TemplateMaxCorrelations
from TemplateFactory import TemplateFactory
from TomogramFactory import TomogramFactory
import CandidateSelector
import FeaturesExtractor
import Labeler
import TiltFinder

from AnalyzeTomogram import analyze_tomogram

def svm_train(svm_path, template_paths, tomogram_paths, source_svm=None, template_generator=None,
              generate_tomograms=False):
    """
    Train an SVM using the templates and tomograms specified. If template_generator is not None then the templates will
    be generated. If generate_tomograms is True then the tomograms will be generated using the templates.
    The result will be saved in svm_path. The SVM can start from an existing one given in source_svm.
    :param svm_path: Path in which the SVM will be saved.
    :param template_paths: List of paths to the templates.
    :param tomogram_paths: List of paths to the tomograms.
    :param source_svm: Path to a source SVM to start with.
    :param template_generator: The generator to use for the templates. Choose from SUPPORTED_GENERATORS.
    :param generate_tomograms: Bool indicating whether to generate tomograms.
    """
    print('Starting training...')
    gf_templates = TemplateFactory(template_generator if template_generator is not None else 'LOAD')
    gf_templates.set_paths(template_paths)
    templates = list(gf_templates.build())

    gf_tomograms = TomogramFactory(templates if generate_tomograms else None)
    gf_tomograms.set_paths(tomogram_paths)
    tomograms = gf_tomograms.build()

    # Training

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

    # Get/Create a SVM
    if source_svm is not None:
        with open(source_svm, 'rb') as file:
            svm = pickle.load(file)
    else:
        svm = SVC()

    x = np.array(feature_vectors)
    y = np.array(labels)
    # print(x.shape)
    # print(y.shape)
    if (len(np.unique(y)) == 1):
        print("SVM training must contain more than one label type (all candidates are the same label)")
        exit()
    svm.fit(x, y)

    with open(svm_path, 'wb') as file:
        pickle.dump(svm, file)

    # TODO: Consider printing a feedback about the result of the command.
    print('Training finished!')
