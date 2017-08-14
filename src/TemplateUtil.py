import numpy as np
from math import sqrt
from scipy.ndimage import measurements


#I think we should just call this function after generating the tomogram. Should this just be a module?
#I think we should also consider subtrackting the average first. That would make all the templates unit vectors
def normalize_template(template):
    factor = sqrt(np.sum(np.square(template.density_map)))
    if factor != 0:
        template.density_map /= factor
    else:
        print("Error normalizing template: L2 norm is zero")


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
    tomogram_dm[shape] += template_dm



def align_densitymap_to_COM(densitymap, container_size):
    """
    :param densitymap: the density map to align
    :param container_size: shape of resulting container (tuple of dimension sizes- for 2D use z_size=1 for both)
    :return: a new tomogram whose COM is its center
    """
    assert(len(densitymap.shape) == len(container_size))
    COM = np.array(measurements.center_of_mass(densitymap))
    container = np.zeros(container_size)
    container_shape = np.array(container_size)
    container_center = np.floor(container_shape / 2)
    densitymap_center = np.floor(np.array(densitymap.shape) / 2)
    COM_offset = densitymap_center - COM
    put_template(container, densitymap, (container_center + COM_offset).astype(int).tolist())

    return container


if __name__ == '__main__':
    from TemplateGenerator import generate_tilted_templates

    dm = np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]])
    t= align_densitymap_to_COM(dm, (9,9))
    assert((np.array(measurements.center_of_mass(t)) == np.floor(np.array(t.shape)/2)).all())

    templates = generate_tilted_templates()
    t = templates[1][2]
    norm = sqrt(np.sum(np.square(t.density_map)))
    print("norm before normalizing: " + str(norm))
    normalize_template(t)
    norm = sqrt(np.sum(np.square(t.density_map)))
    print("norm after normalizing: " + str(norm))
