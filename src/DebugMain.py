from TomogramGenerator import *
from TemplateGenerator import generate_tilted_templates
from Constants import JUNK_ID
from FeaturesExtractor import FeaturesExtractor
from TemplateMaxCorrelations import TemplateMaxCorrelations
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import CandidateSelector
import Labeler
import TiltFinder
import Noise


def print_candidate_list(candidates):
    print("There are " + str(len(candidates)) + " candidates")
    #print true and false seperately? using position labeler?
    print([c.six_position.COM_position for c in candidates])

def candidates2dm(candidates, shape):
    peaks = np.zeros(shape)
    for c in candidates:
        peaks[c.six_position.COM_position] = 1
    return peaks


def show_densitymap(dm, title, subplot=111):
    ax = plt.subplot(subplot)
    fig = plt.gcf()
    fig.suptitle(title)
    if len(dm.shape) == 3:
        ax.imshow(dm[:, :, 0])
    else:
        ax.imshow(dm)

def show_templates(templates):
    print("There are " + str(len(templates)) + " templates-")
    fig = plt.figure(1)
    fig.suptitle("Templates")
    SHOW_N_TILTS = 3
    for i in range(len(templates)):
        for j in range(SHOW_N_TILTS):
            #this fits them to len(template) rows each containing SHOW_N_TILTS plots
            ax = plt.subplot(int(str(len(templates)) + str(SHOW_N_TILTS) + str(i * SHOW_N_TILTS + j + 1)))
            ax.imshow(templates[i][j].density_map[:, :, 0])
    plt.show()

def show_tomogram(tomogram, criteria):
    print('This is the generated tomogram for criteria: ' + str(criteria))
    print('The tomogram composition is: ' + str(tomogram.composition))
    fig = plt.figure(2)
    fig.suptitle("Tomogram")
    ax = plt.subplot()
    ax.imshow(tomogram.density_map[:, :, 0])
    plt.show()

def show_candidates(selector, candidates, tomogram):
    print_candidate_list(candidates)

    fig = plt.figure(3)
    fig.suptitle("Candidate selection")

    ax = plt.subplot(221)
    ax.set_title('Original Tomogram')
    ax.imshow(tomogram.density_map[:, :, 0])

    ax = plt.subplot(222)
    ax.set_title('Max Correlation')
    ax.imshow(selector.max_correlation_per_3loc[:,:,0])

    ax = plt.subplot(223)
    ax.set_title('Blurred Correlation')
    ax.imshow(selector.blurred_correlation_array[:,:,0])

    ax = plt.subplot(224)
    ax.set_title('Selected Candidates')
    dm = candidates2dm(candidates, tomogram.density_map.shape)
    ax.imshow(dm[:, :, 0])

    plt.show()

def compare_reconstruced_tomogram(truth_tomogram, recon_tomogram, plot_dif_map = False):
    fig = plt.figure(2)
    ax = plt.subplot(121)
    ax.set_title('Truth Tomogram')
    ax.imshow(truth_tomogram.density_map[:, :, 0])

    ax = plt.subplot(122)
    ax.set_title('Reconstructed Tomogram')
    ax.imshow(recon_tomogram.density_map[:, :, 0])
    plt.show()

    if not plot_dif_map:
        return
    fig = plt.figure(3)
    ax = plt.subplot()
    ax.set_title('Overlap')
    ax.imshow(truth_tomogram.density_map[:, :, 0] - recon_tomogram.density_map[:, :, 0])
    plt.show()

def compare_candidate_COM(truth_candidates, reco_candidates, tomogram):
    map = tomogram.density_map
    for c in truth_candidates:
        pos = c.six_position.COM_position
        map[pos[0], pos[1], 0] += 2
    for c in reco_candidates:
        pos = c.six_position.COM_position
        if c.label == JUNK_ID:
            map[pos[0], pos[1], 0] -= 1
        else:
            map[pos[0], pos[1], 0] += 1
    print('This is the generated tomogram for criteria: ' + str(criteria))
    fig = plt.figure(2)
    fig.suptitle("Centers")
    ax = plt.subplot()
    ax.imshow(map[:, :, 0])
    plt.show()

if __name__ == '__main__':
    templates = generate_tilted_templates()
    templates = (templates[2], templates[3]) #Test only L shaped templates
    #show_templates(templates)

    #composition = [Candidate.fromTuple(t) for t in DEFAULT_COMPOSITION_TUPLES_2D]
    #tomogram = generate_tomogram_with_given_candidates(templates, criteria)

    criteria = [3, 3]
    truth_tomogram = generate_random_tomogram(templates, templates[0][0].density_map.shape[0], criteria)
    composition = truth_tomogram.composition
    #show_tomogram(tomogram, criteria)

    #tomogram = Noise.make_noisy_tomogram(truth_tomogram)
    tomogram = truth_tomogram
    max_correlations = TemplateMaxCorrelations(tomogram, templates)

    selector = CandidateSelector.CandidateSelector(max_correlations)
    candidates = selector.select(tomogram)
    show_candidates(selector, candidates, tomogram)


    labeler = Labeler.PositionLabeler(tomogram.composition)
    #features_extractor = FeaturesExtractor(templates)
    features_extractor = FeaturesExtractor(max_correlations)

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
    tilt_finder = TiltFinder.TiltFinder(max_correlations)

    from AnalyzeTomogram import analyze_tomogram
    (svm_candidates, feature_vectors, labels) = \
        analyze_tomogram(tomogram, svm_labeler, features_extractor, selector, tilt_finder, True)

    non_junk_candidates = [c for c in svm_candidates if c.label != JUNK_ID]
    svm_tomogram = generate_tomogram_with_given_candidates(templates, non_junk_candidates)

    print("Ground Truth Candidates:")
    for c in composition:
        print("=====\nPos = " + str(c.six_position) + "\tLabel = " + str(c.label))

    print("Reconstructed Candidates:")
    for c in non_junk_candidates:
        print("=====\nPos = " + str(c.six_position) + "\tLabel = " + str(c.label))

    compare_reconstruced_tomogram(truth_tomogram, svm_tomogram, True) #True = draw the difference map as well

    compare_candidate_COM(composition, svm_candidates, truth_tomogram) #display the center of mass of the candidates

    exit(0)