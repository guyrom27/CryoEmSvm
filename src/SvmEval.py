from TemplateMaxCorrelations import TemplateMaxCorrelations
import Labeler
import CandidateSelector
import FeaturesExtractor
import TiltFinder
from AnalyzeTomogram import analyze_tomogram


def svm_eval(svm_and_templates, tomograms):
    """
    Evaluate the tomograms the supplied SVM and templates (As returned from svm_train). The tomograms are evaluated in
    place i.e. their labels are set by the SVM.
    :param svm_and_templates: SVM and templates as returned from svm_train.
    :param tomograms: The tomograms to be evaluated.
    :return Returns the tomograms
    """
    svm = svm_and_templates[0]
    templates = svm_and_templates[1]

    labeler = Labeler.SvmLabeler(svm)

    for tomogram in tomograms:
        max_correlations = TemplateMaxCorrelations(tomogram, templates)
        candidate_selector = CandidateSelector.CandidateSelector(max_correlations)
        features_extractor = FeaturesExtractor.FeaturesExtractor(max_correlations)
        tilt_finder = TiltFinder.TiltFinder(max_correlations)

        # Analyze the tomogram
        (candidates, feature_vectors, predicted_labels) = analyze_tomogram(tomogram, labeler, features_extractor,
                                                                           candidate_selector, tilt_finder, set_labels=True)

    return tomograms