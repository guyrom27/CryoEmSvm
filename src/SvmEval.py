import pickle

from TomogramGenerator import generate_tomogram_with_given_candidates
from CommonDataTypes import Tomogram
from TemplateFactory import TemplateFactory, Generator
from TomogramFactory import TomogramFactory
import Labeler
import CandidateSelector
import FeaturesExtractor


def analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector, set_labels=False):
    candidates = candidate_selector.select(tomogram)
    feature_vectors = []
    labels = []

    for candidate in candidates:
        feature_vectors.append(features_extractor.extract_features(tomogram, candidate))
        # this sets each candidate's label
        labels.append(labeler.label(candidate, set_label=set_labels))

    return candidates, feature_vectors, labels


def svm_eval(svm_path, template_paths, tomogram_paths, out_paths):
    """
    Evaluate the tomograms using the specified templates. If no candidates are present creates them. Labels all the
    candidates using the SVM.
    :param svm_path: Path from which the SVM will be loaded.
    :param template_paths: List of paths to the templates.
    :param tomogram_paths: List of paths to the tomograms.
    :param out_paths: List of paths to which the results of the evaluation of the tomograms will be saved.
    """
    print('Starting evaluation...')
    # Load the data
    with open(svm_path, 'rb') as file:
        svm = pickle.load(file)
    templates = list(TemplateFactory(Generator.LOAD).set_paths(template_paths).build())

    labeler = Labeler.SvmLabeler(svm)
    candidate_selector = CandidateSelector.CandidateSelector(templates)
    features_extractor = FeaturesExtractor.FeaturesExtractor(templates)

    tomograms = TomogramFactory(None).set_paths(tomogram_paths).build()
    tomogram_outs = TomogramFactory(None).set_paths(out_paths).set_save(True).build()

    for tomogram, save_tomogram in zip(tomograms, tomogram_outs):

        # Analyze the tomogram
        (candidates, feature_vectors, predicted_labels) = analyze_tomogram(tomogram, labeler, features_extractor,
                                                                           candidate_selector, set_labels=True)

        save_tomogram(tomogram)

    print('Evaluation finished!')
