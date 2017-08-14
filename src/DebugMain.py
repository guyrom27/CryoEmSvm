from TomogramGenerator import *
from TemplateGenerator import generate_tilted_templates
from Constants import JUNK_ID
from FeaturesExtractor import FeaturesExtractor
import matplotlib.pyplot as plt
import CandidateSelector
import Labeler
import TiltFinder


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
    fig = plt.figure(2)
    fig.suptitle("Tomogram")
    ax = plt.subplot()
    ax.imshow(tomogram.density_map[:, :, 0])
    plt.show()

def show_candidates(selector, candidates, tomogram):
    print_candidate_list(candidates)

    fig = plt.figure(3)
    fig.suptitle("Candidate selection")

    ax = plt.subplot(141)
    ax.set_title('Original Tomogram')
    ax.imshow(tomogram.density_map[:, :, 0])

    ax = plt.subplot(142)
    ax.set_title('Max Correlation')
    ax.imshow(selector.max_correlation_per_3loc[:,:,0])

    ax = plt.subplot(143)
    ax.set_title('Blurred Correlation')
    ax.imshow(selector.blurred_correlation_array[:,:,0])

    ax = plt.subplot(144)
    ax.set_title('Selected Candidates')
    dm = candidates2dm(candidates, tomogram.density_map.shape)
    ax.imshow(dm[:, :, 0])

    plt.show()

if __name__ == '__main__':

    templates = generate_tilted_templates()
    #show_templates(templates)

    criteria = (Candidate.fromTuple(1, 0, 10, 10), Candidate.fromTuple(1, 3, 27, 18), Candidate.fromTuple(0, 0, 10, 28))
    tomogram = generate_tomogram_with_given_candidates(templates, criteria)
    #show_tomogram(tomogram, criteria)

    selector = CandidateSelector.CandidateSelector(templates)
    candidates = selector.select(tomogram)
    #show_candidates(selector, candidates, tomogram)


    labeler = Labeler.PositionLabeler(tomogram.composition)
    features_extractor = FeaturesExtractor(templates)

    for candidate in candidates:
        labeler.label(candidate)
        candidate.set_features(features_extractor.extract_features(tomogram, candidate))

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
    #from SvmEval import analyze_tomogram
    svm_candidates = selector.select(tomogram)
    tilt_finder = TiltFinder.TiltFinder(templates)
    for c in svm_candidates:
        #analyze_tomogram(tomogram, svm_labeler, features_extractor, selector, tilt_finder)
        c.set_features(features_extractor.extract_features(tomogram, c))
        svm_labeler.label(c)
        tilt_finder.find_best_tilt(tomogram, c)

    non_junk_candidates = [c for c in svm_candidates if c.label != JUNK_ID]
    svm_tomogram = generate_tomogram_with_given_candidates(templates, non_junk_candidates)

    print("Ground Truth Candidates:")
    for c in criteria:
        print("=====\n" + str(c))

    print("Reconstructed Candidates:")
    for c in non_junk_candidates:
        print("=====\n" + str(c))

    fig = plt.figure(2)
    ax = plt.subplot(121)
    ax.set_title('Truth Tomogram')
    ax.imshow(tomogram.density_map[:, :, 0])

    ax = plt.subplot(122)
    ax.set_title('Reconstructed Tomogram')
    ax.imshow(svm_tomogram.density_map[:, :, 0])

    plt.show()

    exit(0)

    #print(len(candidates))
    for candidate in candidates:
        print(candidate)

    fig, ax = plt.subplots()
    ax.imshow(tomogram.density_map[:,:,0])

    fig, ax = plt.subplots()
    candidate_positions = np.zeros(tomogram.density_map[:,:,0].shape)
    for candidate in candidates:
        pos = candidate.six_position.COM_position
        if candidate.label == 1:
            col = 0.9
        elif candidate.label == 2:
            col = 0.6
        else:
            col = 0.3
        candidate_positions[pos[0]][pos[1]] = col
    ax.imshow(candidate_positions)


    plt.show()


