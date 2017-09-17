from TomogramGenerator import generate_tomogram_with_given_candidates, generate_random_tomogram
from TemplateGenerator import generate_tilted_templates, load_templates_3d
from Labeler import PositionLabeler, SvmLabeler
from TemplateMaxCorrelations import TemplateMaxCorrelations
from CandidateSelector import CandidateSelector
from FeaturesExtractor import FeaturesExtractor
from TiltFinder import TiltFinder
from TomogramAnalyzer import TomogramAnalyzer
from MetricTester import MetricTester
import VisualUtils
from Noise import make_noisy_tomogram


import numpy as np
from sklearn.svm import SVC

if __name__ == '__main__':
    dim = 3
    #templates = generate_tilted_templates()
    templates = load_templates_3d(r'..\Chimera\Templates' + '\\')

    #composition = [Candidate.fromTuple(t) for t in DEFAULT_COMPOSITION_TUPLES_3D]
    #composition = (Candidate.fromTuple(1, 0, 12, 12, 12), Candidate.fromTuple(0, 6, 27, 27, 27))
    #tomogram = generate_tomogram_with_given_candidates(templates, composition, dim)

    criteria = [3, 3]
    true_tomogram = generate_random_tomogram(templates, criteria, 3)
    tomogram = make_noisy_tomogram(true_tomogram, 3)
    composition = tomogram.composition
    VisualUtils.slider3d(tomogram.density_map)
    print('calculating correlations')
    max_correlations = TemplateMaxCorrelations(tomogram, templates)

    print('selecting')
    selector = CandidateSelector(max_correlations, templates[0][0].density_map.shape)
    candidates = selector.select(tomogram)
    VisualUtils.show_candidates3D(selector, candidates, tomogram)

    print('labeling')
    labeler = PositionLabeler(tomogram.composition)

    print('extracting features')
    features_extractor = FeaturesExtractor(max_correlations)
    for candidate in candidates:
        labeler.label(candidate)
        candidate.set_features(features_extractor.extract_features(candidate))

    #train the SVM on the tomogram
    print('training')
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
    tilt_finder = TiltFinder(max_correlations)

    print('svm labeling')
    analyzer = TomogramAnalyzer(tomogram, templates, svm_labeler)
    (svm_candidates, feature_vectors, labels) = analyzer.analyze()

    print('generating output tomogram')
    svm_tomogram = generate_tomogram_with_given_candidates(templates, svm_candidates, dim)

    print("Ground Truth Candidates:")
    for c in tomogram.composition:
        print("=====\nPos = " + str(c.six_position) + "\nLabel = " + str(c.label))

    print("Reconstructed Candidates:")
    for c in svm_tomogram.composition:
        print("=====\nPos = " + str(c.six_position) + "\nLabel = " + str(c.label))

    metric = MetricTester(tomogram.composition,svm_tomogram.composition, tomogram, svm_tomogram)
    metric.print_metrics()
    from Metrics import Metrics
    m = Metrics()
    m.init_from_tester(metric)
    m.print_stat()
    VisualUtils.slider3d(svm_tomogram.density_map - true_tomogram.density_map)