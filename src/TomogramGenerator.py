from CommonDataTypes import *

from Constants import TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSIONS_2D, TOMOGRAM_DIMENSIONS_3D
import numpy as np
from TemplateUtil import put_template

#def put_template(dm, template_dm, position):
#    dm[position[0] - template_dm.shape[0]//2:position[0] + template_dm.shape[0]//2,position[1] - template_dm.shape[1]//2:position[1] + template_dm.shape[1]//2] += template_dm


def generate_tomogram_with_given_candidates(templates, composition, dimensions=TOMOGRAM_DIMENSIONS_2D):
    """
    3D READY!
    :param templates: list of lists: first dimension is different template_ids second dimension is tilt_id
    :param composition: list of candidates to put in the tomogram
    :param dimensions: the dimensions of the Tomogram- tuple of sizes e.g. (100,100) for 2D, or (100,100,100) for 3D
    :return: Tomogram object
    """
    tomogram_dm = np.zeros(dimensions)
    for candidate in composition:
        put_template(tomogram_dm, templates[candidate.label][candidate.six_position.tilt_id].density_map, candidate.six_position.COM_position)
    return Tomogram(tomogram_dm, tuple(composition))


def randomize_spaced_out_points(space, separation, n_points):
    """
    randomize n points in the space defined by a square of side tomogram_dim spaced so that no two points are closer than separation
    :param space: tuple of integers- size of each dimension, for 2D use 3rd dim size=1
    :param separation: minimal separation between any two points
    :param n_points: amount of points to randomize
    :return: list of random positions
    """
    import poisson_disk
    obj = poisson_disk.pds(space[0], space[1], space[2], separation, n_points)
    return obj.randomize_spaced_points()

def generate_random_candidates(template_side_len, criteria, dim=2):
    """
    :param template_side_len:  we assume templates are cubes
    :param criteria: list of integers. criteria[i] means how many instances of template_id==i should appear in the resulting tomogram
    :param dim 2 for 2D 3 for 3D
    :return: a random list of candidates according to the criteria
    """
    n = sum(criteria)

    #this is the minimal separation between two square templates
    separation = template_side_len * (dim ** 0.5)

    # we don't want COM points too close to the sides
    gap_shape = [(template_side_len - 1) // 2] * 3

    # pad a bit so we won't have boundary issues during detection
    gap_shape = [2*x for x in gap_shape]

    if dim == 2:
        gap_shape[2] = 0
    else:
        assert(dim == 3)

    COM_valid_space = [TOMOGRAM_DIMENSION - 2*x for x in gap_shape]

    if dim==2:
        COM_valid_space[2] = 1

    points = randomize_spaced_out_points(COM_valid_space, separation, n)
    #correct base (push away from sides of tomogram)
    points = [[x[0] + x[1] for x in zip(p,gap_shape)] for p in points]
    ids = [[i] * criteria[i] for i in range(len(criteria))]
    import itertools
    flat_ids = list(itertools.chain.from_iterable(ids))
    import random
    random.shuffle(flat_ids)
    return [Candidate(SixPosition(pos_id[0], EulerAngle.rand_tilt_id()), label=pos_id[1]) for pos_id in zip(points, flat_ids)]


def generate_random_tomogram(templates, template_side, criteria, dim=2):
    """
    :param templates:  list of lists: first dimension is different template_ids second dimension is tilt_id
    :param template_side: we assume the templates are square with this side length
    :param criteria: list of integers. criteria[i] means how many instances of template_id==i should appear in the resulting tomogram
    :param dim 2 for 2D 3 for 3D
    :return: a random Tomogram according to the criteria
    """
    candidates = generate_random_candidates(template_side, criteria, dim)
    return generate_tomogram_with_given_candidates(templates, candidates, TOMOGRAM_DIMENSIONS_3D if dim == 3 else TOMOGRAM_DIMENSIONS_2D )


if __name__ == '__main__':
    pass