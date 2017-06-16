from CommonDataTypes import *


import numpy as np
import scipy.ndimage.interpolation
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


#The non zero density must lie inside a centered sphere of radius TEMPLATE_DIMENSION/2 so that rotations do not exceed the template size
TOMOGRAM_DIMENSION = 300
TOMOGRAM_DIMENSIONS = (TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION)

def put_template(dm, template_dm, position):
    dm[position[0] - template_dm.shape[0]//2:position[0] + template_dm.shape[0]//2,position[1] - template_dm.shape[1]//2:position[1] + template_dm.shape[1]//2]=template_dm


def generate_tomogram(templates, criteria):
    dm = np.zeros(TOMOGRAM_DIMENSIONS)

    c1 = Candidate(SixPosition((40, 40, 0),templates[1][0].orientation), None, templates[1][0].template_id)
    put_template(dm,templates[1][0].density_map, c1.six_position.COM_position)

    c2 = Candidate(SixPosition((250, 250, 0), templates[1][2].orientation), None, templates[1][2].template_id)
    put_template(dm, templates[1][2].density_map, c2.six_position.COM_position)

    return Tomogram(dm, (c1,c2))


if __name__ == '__main__':
    fig, ax = plt.subplots()
    from TemplateGenerator import generate_tilted_templates
    templates = generate_tilted_templates()

    tom = generate_tomogram(templates, None)

    import CandidateSelector

    selector = CandidateSelector.CandidateSelector(templates)
    candidates = selector.select(tom)
    print(candidates)

    #ax.imshow(create_circle(100))
    ax.imshow(tom.density_map)


#    plt.show()






