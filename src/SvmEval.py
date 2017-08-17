from Labeler import SvmLabeler
from TomogramAnalyzer import TomogramAnalyzer


def svm_eval(svm_and_templates, tomograms):
    """
    Evaluate the tomograms the supplied SVM and templates (As returned from svm_train).
    :param svm_and_templates:   SVM and templates as returned from svm_train.
    :param tomograms:           Iterator of the tomograms to be evaluated.
    :return A list of lists of the candidates for each tomogram.
    """

    (svm, templates) = svm_and_templates
    tomogram_candidates = []
    labeler = SvmLabeler(svm)

    for tomogram in tomograms:
        # Analyze the tomogram
        analyzer = TomogramAnalyzer(tomogram, templates, labeler)
        (candidates, feature_vectors, predicted_labels) = analyzer.analyze()

        # Add the candidates to the list of results
        tomogram_candidates.append(candidates)

    return tomogram_candidates
