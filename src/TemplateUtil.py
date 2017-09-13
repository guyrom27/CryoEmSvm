import numpy as np
from math import sqrt
from scipy.ndimage import measurements

"""
Different Template manipulations are collected here
"""


def shape_to_slices(shape, corner = None):
    if not corner:
        corner = [0]*len(shape)
    assert(len(shape) == len(corner))
    return tuple([slice(corner[i],corner[i]+shape[i]) for i in range(len(shape))])


def get_normalize_template_dm(template):
    """
    normalize the L2 norm of the template density_map
    """
    factor = sqrt(np.sum(np.square(template.density_map)))
    if factor != 0:
        return template.density_map / factor
    else:
        raise Exception("Error normalizing template: L2 norm is zero")


def put_template(tomogram_dm, template_dm, position):
    """
    3D READY
    :param tomogram_dm:  dm is density map
    :param template_dm: dm is density map
    :param position: center of cube/square position
    :return:
    """
    corner = [position[i] - template_dm.shape[i] // 2 for i in range(len(tomogram_dm.shape))]
    shape = tuple([slice(corner[i],corner[i] + template_dm.shape[i]) for i in range(len(corner))])
    if ([shape[i].start < 0 or shape[i].stop > tomogram_dm.shape[i] for i in range(len(tomogram_dm.shape))].count(True) > 0):
        assert(False)
    tomogram_dm[shape] += template_dm



def align_densitymap_to_COM(densitymap, container_size_3D):
    """
    :param densitymap: the density map to align
    :param container_size_3D: shape of resulting container (tuple of dimension sizes- for 2D use z_size=1 for both)
    :return: a new tomogram whose COM is its center
    """
    #only 2d fit in 3D arrays
    assert(len(densitymap.shape) == len(container_size_3D) and len(densitymap.shape) == 3 and densitymap.shape[2] == 1 and container_size_3D[2] == 1)
    #all sizes must be odd
    assert ([x%2==1 for x in densitymap.shape].count(False) == 0)
    assert ([x % 2 == 1 for x in container_size_3D].count(False) == 0)


    flat_dm = densitymap[:,:,0]
    container_size_2D = container_size_3D[:2]

    big_container = np.zeros([2*x+1 for x in container_size_2D])
    big_container_center = np.floor(np.array(big_container.shape) / 2)

    densitymap_center = np.floor(np.array(flat_dm.shape) / 2)

    put_template(big_container, flat_dm, big_container_center.astype(int).tolist())

    COM = np.array(measurements.center_of_mass(big_container))

    top_left_corner = (np.floor(COM - ((np.array(container_size_2D) - 1)/2))).astype(int).tolist()
    shape = shape_to_slices(container_size_2D, top_left_corner)
    truncated_matrix = big_container[shape]

    return truncated_matrix.reshape(container_size_3D)


if __name__ == '__main__':
    from TemplateGenerator import generate_tilted_templates

    dm = np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]])
    t= align_densitymap_to_COM(dm, (9,9))
    assert((np.array(measurements.center_of_mass(t)) == np.floor(np.array(t.shape)/2)).all())

    templates = generate_tilted_templates()
    t = templates[1][2]
    norm = sqrt(np.sum(np.square(t.density_map)))
    print("norm before normalizing: " + str(norm))
    get_normalize_template_dm(t)
    norm = sqrt(np.sum(np.square(t.density_map)))
    print("norm after normalizing: " + str(norm))
