import CommonDataTypes


import numpy as np
import scipy.ndimage.interpolation


#The non zero density must lie inside a centered sphere of radius TEMPLATE_DIMENSION/2 so that rotations do not exceed the template size
TEMPLATE_DIMENSION = 20
TEMPLATE_DIMENSIONS = (TEMPLATE_DIMENSION,TEMPLATE_DIMENSION)



def create_cube(dim):
    return np.ones((dim,dim,dim))

def create_sphere(rad):
    dm = np.zeros((rad*2,rad*2,rad*2))
    for x in range(2*rad):
        for y in range(2*rad):
            for z in range(2*rad):
                if (x-rad)**2 + (y-rad)**2 + (z-rad)**2 <= rad**2:
                    dm[x,y,z] = 1
    return dm


def rotate3d(dm, phi, theta, psi):
    return dm

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

def rotate2d(dm, theta):
    rotated = scipy.ndimage.interpolation.rotate(dm, theta)
    rotated_dim = rotated.shape[0]
    original_dim = dm.shape[0]

    return rotated[rotated_dim//2-original_dim//2:rotated_dim//2+original_dim//2,rotated_dim//2-original_dim//2:rotated_dim//2+original_dim//2]

def rotate(dm, eu_angle):
    return rotate2d(dm, eu_angle.Phi)


def generate_tilted_templates():
    """
    :return: tuple of tuples of TiltedTemplates (each group has the same template_id)
    """
    tilts = []
    for theta in range(0,90,15):
        tilts.append(CommonDataTypes.EulerAngle(theta,None,None))


    circle_dm = np.zeros(TEMPLATE_DIMENSIONS)
    fill_with_circle(circle_dm, TEMPLATE_DIMENSION/4)
    circle_templates = []
    for tilt in tilts:
         circle_templates.append(CommonDataTypes.TiltedTemplate(rotate(circle_dm,tilt), tilt, 1))

    square_templates = []
    square_dm = np.zeros(TEMPLATE_DIMENSIONS)
    fill_with_square(square_dm, TEMPLATE_DIMENSION/2)
    for tilt in tilts:
        square_templates.append(CommonDataTypes.TiltedTemplate(rotate(square_dm, tilt), tilt, 2))

    return (circle_templates,square_templates)



if __name__ == '__main__':
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    templates = generate_tilted_templates()


    #ax.imshow(create_circle(100))
    ax.imshow(templates[0][0].density_map)


    fig, ax = plt.subplots()
    ax.imshow(templates[1][3].density_map)

    plt.show()






