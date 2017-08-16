from TomogramGenerator import *
from TemplateGenerator import generate_tilted_templates_2d
from FeaturesExtractor import FeaturesExtractor
from TemplateMaxCorrelations import TemplateMaxCorrelations
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import CandidateSelector
import Labeler
import TiltFinder
import Noise
from VisualUtils import candidates2dm, show_templates, show_candidates, show_tomogram, compare_reconstruced_tomogram, compare_candidate_COM



if __name__ == '__main__':
    templates = generate_tilted_templates_2d()
    #show_templates(templates)

    #composition = [Candidate.fromTuple(t) for t in DEFAULT_COMPOSITION_TUPLES_2D]
    #tomogram = generate_tomogram_with_given_candidates(templates, criteria)
    criteria = [1, 2, 3]
    import random
    random.seed(12)
    truth_tomogram = generate_random_tomogram(templates, criteria)
    # tomogram = Noise.make_noisy_tomogram(truth_tomogram)
    tomogram = truth_tomogram
    #show_tomogram(tomogram, criteria)

    # prepare for training
    max_correlations = TemplateMaxCorrelations(tomogram, templates)
    selector = CandidateSelector.CandidateSelector(max_correlations)
    features_extractor = FeaturesExtractor(max_correlations)
    tilt_finder = TiltFinder.TiltFinder(max_correlations)
    labeler = Labeler.PositionLabeler(tomogram.composition)

    candidates = selector.select(tomogram)
    show_candidates(selector, candidates, tomogram)

    for candidate in candidates:
        labeler.label(candidate)
        candidate.set_features(features_extractor.extract_features(candidate))

    #train the SVM on the tomogram
    Xlist = [c.features for c in candidates]
    Ylist = [c.label for c in candidates]
    from sklearn.svm import SVC
    svm = SVC()
    x = np.array(Xlist)
    y = np.array(Ylist)
    if (len(np.unique(y)) == 1):
        print("SVM training must contain more than one label type (all candidates are the same label)")
        exit()
    svm.fit(x, y)

    svm_labeler = Labeler.SvmLabeler(svm)


    from AnalyzeTomogram import analyze_tomogram
    (svm_candidates, feature_vectors, labels) = \
        analyze_tomogram(tomogram, svm_labeler, features_extractor, selector, tilt_finder, True)

    svm_tomogram = generate_tomogram_with_given_candidates(templates, svm_candidates, 2)

    print("Ground Truth Candidates:")
    for c in truth_tomogram.composition:
        print("=====\nPos = " + str(c.six_position) + "\tLabel = " + str(c.label))

    print("Reconstructed Candidates:")
    for c in svm_tomogram.composition:
        print("=====\nPos = " + str(c.six_position) + "\tLabel = " + str(c.label))

    import MetricTester
    metric = MetricTester.MetricTester(truth_tomogram.composition,svm_tomogram.composition)
    metric.print_metrics()

    compare_reconstruced_tomogram(truth_tomogram, svm_tomogram, True) #True = draw the difference map as well

    compare_candidate_COM(svm_tomogram.composition, svm_candidates, truth_tomogram) #display the center of mass of the candidates

    exit(0)