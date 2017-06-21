from CommonDataTypes import *


import numpy as np
import scipy.ndimage.interpolation
#from mpl_toolkits.mplot3d import Axes3D


#The non zero density must lie inside a centered sphere of radius TEMPLATE_DIMENSION/2 so that rotations do not exceed the template size
TOMOGRAM_DIMENSION = 40
TOMOGRAM_DIMENSIONS = (TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION)

def put_template(dm, template_dm, position):
    dm[position[0] - template_dm.shape[0]//2:position[0] + template_dm.shape[0]//2,position[1] - template_dm.shape[1]//2:position[1] + template_dm.shape[1]//2] += template_dm


def generate_tomogram(templates, criteria):
    dm = np.zeros(TOMOGRAM_DIMENSIONS)

    c1 = Candidate(SixPosition((10, 10, 0),templates[1][0].orientation), None, templates[1][0].template_id)
    put_template(dm,templates[1][0].density_map, c1.six_position.COM_position)

    c2 = Candidate(SixPosition((27, 18, 0), templates[1][2].orientation), None, templates[1][2].template_id)
    put_template(dm, templates[1][2].density_map, c2.six_position.COM_position)

    c3 = Candidate(SixPosition((10, 28, 0), templates[0][0].orientation), None, templates[0][0].template_id)
    put_template(dm, templates[0][0].density_map, c3.six_position.COM_position)


    return Tomogram(dm, (c1,c2,c3))


if __name__ == '__main__':

    from TemplateGenerator import generate_tilted_templates
    from FeaturesExtractor import FeaturesExtractor
    import matplotlib.pyplot as plt

    templates = generate_tilted_templates()

    tomogram = generate_tomogram(templates, None)

    import CandidateSelector
    import Labeler

    selector = CandidateSelector.CandidateSelector(templates)
    candidates = selector.select(tomogram)
    labeler = Labeler.PositionLabeler(tomogram.composition)
    features_extractor = FeaturesExtractor(templates)
    for candidate in candidates:
        labeler.label(candidate)
        candidate.set_featers(features_extractor.extract_features(tomogram, candidate))


    #print(len(candidates))
    for candidate in candidates:
        print(candidate)

    fig, ax = plt.subplots()
    ax.imshow(tomogram.density_map)

    fig, ax = plt.subplots()
    candidate_positions = np.zeros(tomogram.density_map.shape)
    for candidate in candidates:
        pos = candidate.six_position.COM_position
        if candidate.label == 0:
            col = 0.9
        elif candidate.label == 1:
            col = 0.6
        else:
            col = 0.3

        candidate_positions[pos[0]][pos[1]] = col
    ax.imshow(candidate_positions)

    plt.show()

