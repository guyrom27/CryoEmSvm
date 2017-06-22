from CommonDataTypes import *


import numpy as np
TOMOGRAM_DIMENSION = 40
TOMOGRAM_DIMENSIONS = (TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION)
TOMOGRAM_DIMENSIONS_2D = (TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION,1)

#def put_template(dm, template_dm, position):
#    dm[position[0] - template_dm.shape[0]//2:position[0] + template_dm.shape[0]//2,position[1] - template_dm.shape[1]//2:position[1] + template_dm.shape[1]//2] += template_dm

def put_template(tomogram_dm, template_dm, position):
    corner = [position[i] - template_dm.shape[i] // 2 for i in range(len(tomogram_dm.shape))]
    shape = tuple([slice(corner[i],corner[i] + template_dm.shape[i]) for i in range(len(corner))])
    tomogram_dm[shape] += template_dm


def generate_tomogram(templates, criteria):
    return generate_tomogram_2d(templates, ((1,0,10,10),(1,2,27,18),(0,0,10,28)))


def generate_tomogram_2d(templates, criteria):
    tomogram_dm = np.zeros(TOMOGRAM_DIMENSIONS_2D)
    composition = []
    for item in criteria:
        template = templates[item[0]][item[1]]
        position = (item[2],item[3],0)
        candidate = Candidate(SixPosition(position,template.orientation), None, template.template_id)
        put_template(tomogram_dm, template.density_map, candidate.six_position.COM_position)
        composition.append(candidate)

    return Tomogram(tomogram_dm, tuple(composition))


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
        candidate.set_features(features_extractor.extract_features(tomogram, candidate))


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

