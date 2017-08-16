from Labeler import SvmLabeler
from AnalyzeTomogram import analyze_tomogram


def svm_eval(svm_and_templates, tomograms, return_tomograms=False):
    """
    Evaluate the tomograms the supplied SVM and templates (As returned from svm_train).
    :param svm_and_templates:   SVM and templates as returned from svm_train.
    :param tomograms:           The tomograms to be evaluated.
    :param return_tomograms     Boolean value indicating whether the tomograms used should be returned as well.
    :return A list of lists of the candidates for each tomogram. If return_tomograms is true then the list
            of lists of the candidates will be within a tuple containing the tomograms as it's second value.
    """
    svm = svm_and_templates[0]
    templates = svm_and_templates[1]

    tomogram_candidates = []
    labeler = SvmLabeler(svm)

    for tomogram in tomograms:
        # Analyze the tomogram
        (candidates, feature_vectors, predicted_labels) = analyze_tomogram(tomogram, templates, labeler, set_labels=True)

        # Add the candidates to the list of results
        tomogram_candidates.append(candidates)

    # Return the result
    return tomogram_candidates
