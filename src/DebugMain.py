from TomogramGenerator import *
from TemplateGenerator import generate_tilted_templates_2d
from FeaturesExtractor import FeaturesExtractor
from TemplateMaxCorrelations import TemplateMaxCorrelations
from CandidateSelector import CandidateSelector
from Labeler import PositionLabeler, SvmLabeler
from TiltFinder import TiltFinder
import Noise
from MetricTester import MetricTester
import VisualUtils
from AnalyzeTomogram import analyze_tomogram

from sklearn.svm import SVC


if __name__ == '__main__':
    dim = 2
    templates = generate_tilted_templates_2d()
    #VisualUtils.show_templates(templates)

    #composition = [Candidate.fromTuple(t) for t in DEFAULT_COMPOSITION_TUPLES_2D]
    #tomogram = generate_tomogram_with_given_candidates(templates, composition, dim)
    criteria = [1, 2, 3, 1]
    truth_tomogram = generate_random_tomogram(templates, criteria, dim)
    # tomogram = Noise.make_noisy_tomogram(truth_tomogram) #TODO: might be broken
    tomogram = truth_tomogram
    #VisualUtils.show_tomogram(tomogram, criteria)

    # prepare for training
    max_correlations = TemplateMaxCorrelations(tomogram, templates)
    selector = CandidateSelector(max_correlations)
    features_extractor = FeaturesExtractor(max_correlations)
    tilt_finder = TiltFinder(max_correlations)
    labeler = PositionLabeler(tomogram.composition)

    candidates = selector.select(tomogram)
    VisualUtils.show_candidates(selector, candidates, tomogram)

    for candidate in candidates:
        labeler.label(candidate)
        candidate.set_features(features_extractor.extract_features(candidate))

    #train the SVM on the tomogram
    Xlist = [c.features for c in candidates]
    Ylist = [c.label for c in candidates]
    svm = SVC()
    x = np.array(Xlist)
    y = np.array(Ylist)
    if (len(np.unique(y)) == 1):
        print("SVM training must contain more than one label type (all candidates are the same label)")
        exit()
    svm.fit(x, y)

    svm_labeler = SvmLabeler(svm)


    (svm_candidates, feature_vectors, labels) = \
        analyze_tomogram(tomogram, templates, svm_labeler, True)

    svm_tomogram = generate_tomogram_with_given_candidates(templates, svm_candidates, dim)

    print("Ground Truth Candidates:")
    for c in truth_tomogram.composition:
        print("=====\nPos = " + str(c.six_position) + "\tLabel = " + str(c.label))

    print("Reconstructed Candidates:")
    for c in svm_tomogram.composition:
        print("=====\nPos = " + str(c.six_position) + "\tLabel = " + str(c.label))


    metric = MetricTester(truth_tomogram.composition,svm_tomogram.composition)
    metric.print_metrics()

    VisualUtils.compare_reconstruced_tomogram(truth_tomogram, svm_tomogram, True) #True = draw the difference map as well
    VisualUtils.compare_candidate_COM(svm_tomogram.composition, svm_candidates, truth_tomogram) #display the center of mass of the candidates

    exit(0)