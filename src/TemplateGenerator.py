import numpy as np
import scipy.ndimage.interpolation
import pickle

from CommonDataTypes import TiltedTemplate, EulerAngle
from Constants import TEMPLATE_DIMENSION, TEMPLATE_DIMENSIONS_2D, TEMPLATE_DIMENSIONS_3D, TEMPLATE_DIMENSIONS_2D_CONTAINER
from TemplateUtil import align_densitymap_to_COM
from StringComperableEnum import StringComperableEnum


#The non zero density must lie inside a centered sphere of radius TEMPLATE_DIMENSION/2 so that rotations do not exceed the template size



# -------------------------------------------------------------------------------- #
# --------------------------------------- 3D ------------------------------------- #
# -------------------------------------------------------------------------------- #

def fill_with_sphere(dm, rad):
    for x in range(2*rad):
        for y in range(2*rad):
            for z in range(2*rad):
                if (x-rad)**2 + (y-rad)**2 + (z-rad)**2 <= rad**2:
                    dm[x,y,z] = 1
    return dm


def fill_with_cube(dm, side):
    dim = dm.shape[0]
    top_left = int(dim/2-side/2)
    for x in range(int(side)):
        for y in range(int(side)):
            for z in range(int(side)):
                dm[top_left+x,top_left+y, top_left+z] = 1
    return dm


def rotate3d(dm, eu_angle):
    # rotate euler angles
    rotated = scipy.ndimage.interpolation.rotate(dm, eu_angle.Phi, (0, 1))
    rotated = scipy.ndimage.interpolation.rotate(rotated, eu_angle.Theta, (0, 2))
    rotated = scipy.ndimage.interpolation.rotate(rotated, eu_angle.Psi, (0, 1))

    # truncate
    rotated_dim = rotated.shape[0]
    original_dim = dm.shape[0]

    return rotated[rotated_dim // 2 - original_dim // 2:rotated_dim // 2 + original_dim // 2,
                   rotated_dim // 2 - original_dim // 2:rotated_dim // 2 + original_dim // 2,
                   rotated_dim // 2 - original_dim // 2:rotated_dim // 2 + original_dim // 2]

    return rotated


def show3d(dm):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    d = int(dm.shape[2]**0.5)+1
    fig, axarr = plt.subplots(d,d)
    for z in range(dm.shape[2]):
        zdm = dm[:,:,z]
        zdm[0,0] = 2
        axarr[z//d, z%d].imshow(zdm)
    plt.show()


def load_templates_3d(templates_path):
    # load pickles
    template_metadata = pickle.load(open(templates_path + 'template_ids.p','rb'))
    tilt_metadata = pickle.load(open(templates_path + 'tilt_ids.p','rb'))

    # load and create tilted template for every tilt_id and template_id
    tilted_templates = tuple([tuple([TiltedTemplate(np.load(templates_path + str(template_id) + '_' + str(tilt_id) + '.npy'), tilt_id, template_id) for tilt_id in range(len(tilt_metadata))]) for template_id in range(len(template_metadata))])

    # assert tilt and template ids match location in tuples
    for template_id in range(len(tilted_templates)):
        for tilt_id in range(len(tilted_templates[template_id])):
            tilted_template = tilted_templates[template_id][tilt_id]
            assert(tilted_template.template_id == template_id and tilted_template.tilt_id == tilt_id)

    return tilted_templates, template_metadata, tilt_metadata


def generate_tilted_templates_3d(templates_path):
    return


# -------------------------------------------------------------------------------- #
# --------------------------------------- 2D ------------------------------------- #
# -------------------------------------------------------------------------------- #

def fill_with_square(dm, side):
    dim = dm.shape[0]
    top_left = int(dim/2-side/2)
    for x in range(int(side)):
        for y in range(int(side)):
            dm[top_left+x,top_left+y] = 1
    return dm


def fill_with_circle(dm, rad):
    dim = dm.shape[0]
    for x in range(dim):
        for y in range(dim):
            if (x-dim/2)**2 + (y-dim/2)**2 <= rad**2:
                dm[x,y] = 1
    return dm

#   |--w1--|
# _   ____
# |  |x __| h2
# h1 | |
# |  | |
# _  |_|
#     w2
#   x is the position of the center of the picture
#
def fill_with_L(dm, h1, w1, h2, w2, flip= False):
    dim = dm.shape[0]
    corner_x = (dim - 1)/2
    corner_y = (dim - 1)/2
    offset_x = (w2 - 1)/2
    offset_y = (h2 - 1)/2
    #I want the center of rotation to be the corner
    ind_map = lambda p: (int(corner_y - p[1]), int(corner_x + p[0]))
    if flip:
        ind_map = lambda p: (int(corner_y - p[1]), int(corner_x - p[0]))
    for x in range(int(w1)):
        for y in range(int(h1)):
            dm[ind_map((x - offset_x, y - offset_y))] = 1

    for x in range(int(w2), int(w1)):
        for y in range(int(h2), int(h1)):
            dm[ind_map((x - offset_x, y - offset_y))] = 0
    return dm


# checks if the inequality:
# 0 <= p1 + p2 < bound
# holds for each index
def check_if_in_bound(bound, p1, p2):
    for i in range(len(bound)):
        if bound[i] <= p1[i] + p2[i] or p1[i] + p2[i] < 0:
            return False
    return True


def fill_with_rand_shape(dm, n_iterations=10, blur=True):
    for i in range(n_iterations):
        add_random_shape(dm)
    if blur:
        import Noise
        dm = Noise.blur_filter(dm)
    return dm

def add_random_shape(dm):
    import numpy as np
    from numpy.random import randint as rnd
    s = dm.shape
    p = (rnd(s[0]), rnd(s[1]), rnd(s[2])) #pick a random point

    rnd_dim = rnd(2, 5)  #dim must be odd
    sub_shape = (2*rnd_dim + 1, 2*rnd_dim + 1, 2*rnd_dim + 1)
    sub_map = np.zeros(sub_shape)
    if rnd(2) == 0:
        sub_map = np.ones(sub_shape)  #sub_shape is a cube
    else:
        sub_map = fill_with_sphere(sub_map, rnd_dim - 1)
    #sub_map = np.ones((rnd_dim, rnd_dim, rnd_dim))
    for x in range(-rnd_dim, rnd_dim):
        for y in range(-rnd_dim, rnd_dim):
            for z in range(-rnd_dim, rnd_dim):
                if check_if_in_bound(s, p,(x, y, z)):
                    dm[x + p[0], y + p[1], z + p[2]] += sub_map[rnd_dim - x, rnd_dim - y, rnd_dim -z]
                    #dm[x + p[0], y + p[1], z + p[2]] += sub_map[x,y,z]






def rotate2d(dm, theta):
    rotated = scipy.ndimage.interpolation.rotate(dm, theta)
    rotated_dim = rotated.shape[0]
    original_dim = dm.shape[0]

    return rotated[rotated_dim//2-original_dim//2:rotated_dim//2-original_dim//2 + original_dim,rotated_dim//2-original_dim//2:rotated_dim//2-original_dim//2 + original_dim]


def generate_tilted_templates_2d():
    """
    :return: tuple of tuples of TiltedTemplates (each group has the same template_id)
    """

    #TODO use init_tilts instead
    EulerAngle.Tilts = []
    for theta in range(0,345,15):
        EulerAngle.Tilts.append(EulerAngle(theta,None,None))


    circle_dm = np.zeros(TEMPLATE_DIMENSIONS_2D)
    fill_with_circle(circle_dm[:,:,0], TEMPLATE_DIMENSION/4)
    circle_templates = []
    for tilt in enumerate(EulerAngle.Tilts):
         circle_templates.append(TiltedTemplate(rotate(circle_dm,tilt[1]), tilt[0], 1))

    square_templates = []
    square_dm = np.zeros(TEMPLATE_DIMENSIONS_2D)
    fill_with_square(square_dm[:, :, 0], TEMPLATE_DIMENSION/2)
    for tilt in enumerate(EulerAngle.Tilts):
        square_templates.append(TiltedTemplate(align_densitymap_to_COM(rotate(square_dm, tilt[1]), TEMPLATE_DIMENSIONS_2D_CONTAINER), tilt[0], 2))

    Lshaped_templates = []
    L_dm = np.zeros(TEMPLATE_DIMENSIONS_2D)
    x = 11
    if (TEMPLATE_DIMENSION-1)/2 < 11:
        x = 9
    fill_with_L(L_dm[:,:,0], x , 7, 3, 3)
    for tilt in enumerate(EulerAngle.Tilts):
        Lshaped_templates.append(TiltedTemplate(align_densitymap_to_COM(rotate(L_dm, tilt[1]), TEMPLATE_DIMENSIONS_2D_CONTAINER), tilt[0], 1))

    flipped_Lshaped_templates = []
    flipped_L_dm = np.zeros(TEMPLATE_DIMENSIONS_2D)
    fill_with_L(flipped_L_dm[:, :, 0], x, 7, 3, 3, True)
    for tilt in enumerate(EulerAngle.Tilts):
        flipped_Lshaped_templates.append(TiltedTemplate(align_densitymap_to_COM(rotate(flipped_L_dm, tilt[1]), TEMPLATE_DIMENSIONS_2D_CONTAINER), tilt[0], 1))

    return (circle_templates, square_templates, Lshaped_templates, flipped_Lshaped_templates)


# -------------------------------------------------------------------------------- #
# ------------------------------------ GENERAL ----------------------------------- #
# -------------------------------------------------------------------------------- #
def rotate(dm, eu_angle):
    return rotate2d(dm, eu_angle.Phi)


def generate_tilted_templates():
    """
    :return: tuple of tuples of TiltedTemplates (each group has the same template_id)
    """
    return generate_tilted_templates_2d()


def normalize(self, template):
    from math import sqrt
    for tilted_template in template:
        factor = sqrt(np.sum(np.square(tilted_template.density_map))) #calculate the L2 norm of the template
        if factor != 0:
            tilted_template.density_map /= factor
        else:
            print("Error normalizing template: L2 norm is zero")
    return template


def normalize_all(self, templates):
    return [normalize(template) for template in templates]


# -------------------------------------------------- Generators ------------------------------------------------------ #
# Enum containing all the supported generators
class TemplateGenerator(StringComperableEnum):
    LOAD = 'LOAD'
    SOLID = 'SOLID'
    LOAD_3D = 'LOAD_3D'


# TODO: Place holders for template generator
def template_loader(paths, save):
    if not save:
        for path in paths:
            with open(path, 'rb') as file:
                yield pickle.load(file)
    else:
        for path in paths:
            with open(path, 'wb') as file:
                yield lambda x: pickle.dump(x, file)


def template_generator_solid(paths):
    templates = generate_tilted_templates()
    for i, path in enumerate(paths):
        template = templates[i]
        with open(path, 'wb') as file:
            pickle.dump(template, file)
        yield template


def template_generator_3d_load(paths):
    templates = load_templates_3d(paths[0])
    for template in templates:
        yield template


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import VisualUtils

    '''
    fig1 = plt.figure(1)
    ax = plt.subplot()
    ax.imshow(dm[:,:,0])
    plt.show()
    '''

    '''
    templates = generate_tilted_templates()
    for i in range(len(templates[2])):
        fig = plt.figure(2)
        ax = plt.subplot(121)
        ax.imshow(templates[2][i].density_map[:, :, 0])

        ax = plt.subplot(122)
        ax.imshow(templates[3][i].density_map[:, :, 0])
        plt.show()
  
    d1 = np.zeros([25, 25, 1])
    fill_with_L(d1, 11, 7, 3, 3)

    fig, ax = plt.subplots()
    ax.imshow(d1[:, :, 0])
    plt.show()

    d1 = np.zeros([25, 25, 1])
    fill_with_L(d1, 11, 7, 3, 3, True)

    fig, ax = plt.subplots()
    ax.imshow(d1[:, :, 0])
    plt.show()
    '''

    #tilted_templates, template_ids, tilt_ids = load_templates_3d(r'C:\Users\Matan\PycharmProjects\Workshop\Chimera\Templates\\')
    #print('Done!')


    # templates = generate_tilted_templates()
    #
    # fig, ax = plt.subplots()
    # ax.imshow(templates[0][0].density_map)
    #
    #
    # fig, ax = plt.subplots()
    # ax.imshow(templates[1][3].density_map)
    #
    # templates_2d = generate_tilted_templates_2d()
    # print(templates_2d[0][0].density_map.shape)
    #
    # fig, ax = plt.subplots()
    # ax.imshow(templates_2d[1][3].density_map[:,:,0])
    #
    # plt.show()


    #square_dm = np.zeros(TEMPLATE_DIMENSIONS_2D)
    #fill_with_square(square_dm[:, :, 0], TEMPLATE_DIMENSION / 2)
    #show3d(rotate3d(square_dm, EulerAngle(0, 0, 0)))
    #show3d(rotate3d(square_dm, EulerAngle(0, 0, 0)))
    #show3d(rotate3d(square_dm, EulerAngle(0, 40, 0)))
    #cube_dm = fill_with_cube(c, TEMPLATE_DIMENSION / 2)
    #show3d(rotate3d(cube_dm,EulerAngle(45,30,0)))
    #sphere_dm = fill_with_sphere(np.zeros(TEMPLATE_DIMENSIONS), TEMPLATE_DIMENSION // 3)
    #show3d(sphere_dm)

    #a = np.load(r'C:\Users\Matan\PycharmProjects\Workshop\Chimera\tmp_330_150_90.npy')
    #show3d(a)
    #plt.show()







