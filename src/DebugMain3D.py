
from TomogramGenerator import generate_tomogram_with_given_candidates, generate_random_tomogram, TOMOGRAM_DIMENSIONS_3D
from TemplateGenerator import generate_tilted_templates, load_templates_3d
from Constants import JUNK_ID
from FeaturesExtractor import FeaturesExtractor
from CommonDataTypes import Candidate, EulerAngle
from TemplateMaxCorrelations import TemplateMaxCorrelations
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import VisualUtils
import CandidateSelector
import Labeler
import TiltFinder
import numpy as np

def print_candidate_list(candidates):
    print("There are " + str(len(candidates)) + " candidates")
    #print true and false seperately? using position labeler?
    print([c.six_position.COM_position for c in candidates])

def candidates2dm(candidates, shape):
    peaks = np.zeros(shape)
    for c in candidates:
        peaks[c.six_position.COM_position] = 1
    return peaks



def show_templates(templates):
    print("There are " + str(len(templates)) + " templates-")

def show_tomogram(tomogram, criteria):
    print('This is the generated tomogram for criteria: ' + str(criteria))
    print('The tomogram composition is: ' + str(tomogram.composition))

def show_candidates(selector, candidates, tomogram):
    print_candidate_list(candidates)



if __name__ == '__main__':
    #templates = generate_tilted_templates()
    templates = load_templates_3d(r'..\Chimera\Templates' + '\\')
    show_templates(templates)

    #composition = [Candidate.fromTuple(t) for t in DEFAULT_COMPOSITION_TUPLES_3D]
    #composition = (Candidate.fromTuple(1, 0, 12, 12, 12), Candidate.fromTuple(0, 6, 27, 27, 27))
    #tomogram = generate_tomogram_with_given_candidates(templates, composition, TOMOGRAM_DIMENSIONS_3D)

    criteria = [1,1]
    tomogram = generate_random_tomogram(templates, criteria, 3)
    composition = tomogram.composition
    show_tomogram(tomogram, criteria)
    VisualUtils.slider3d(tomogram.density_map)

    print('calculating correlations')
    max_correlations = TemplateMaxCorrelations(tomogram, templates)

    print('selecting')
    selector = CandidateSelector.CandidateSelector(max_correlations)
    candidates = selector.select(tomogram)
    #show_candidates(selector, candidates, tomogram)

    print('labeling')
    labeler = Labeler.PositionLabeler(tomogram.composition)

    print('extracting features')
    features_extractor = FeaturesExtractor(max_correlations)
    for candidate in candidates:
        labeler.label(candidate)
        candidate.set_features(features_extractor.extract_features(candidate))

    #train the SVM on the tomogram
    print('training')
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
    tilt_finder = TiltFinder.TiltFinder(max_correlations)

    print('svm labeling')
    from AnalyzeTomogram import analyze_tomogram
    (svm_candidates, feature_vectors, labels) = \
        analyze_tomogram(tomogram, svm_labeler, features_extractor, selector, tilt_finder, True)

    print('generating output tomogram')
    non_junk_candidates = [c for c in svm_candidates if c.label != JUNK_ID]
    svm_tomogram = generate_tomogram_with_given_candidates(templates, non_junk_candidates, 3)

    print("Ground Truth Candidates:")
    for c in composition:
        print("=====\nPos = " + str(c.six_position) + "\nLabel = " + str(c.label))

    print("Reconstructed Candidates:")
    for c in non_junk_candidates:
        print("=====\nPos = " + str(c.six_position) + "\nLabel = " + str(c.label))