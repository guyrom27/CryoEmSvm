from Constants import NOISE_GAUSS_PARAM, NOISE_LINEAR_PARAM, NOISE_GAUSSIAN_SIZE, NOISE_GAUSSIAN_STDEV
from CommonDataTypes import Tomogram
from TemplateUtil import create_kernel, KERNEL_GAUSSIAN

import numpy as np
import scipy.signal


"""
Add different types  of noise to the density maps 
"""

def gauss_noise(dmap, sigma = None, mu = 0):
    if sigma is None:
        sigma = 0.3 * dmap.max()
    noisy = dmap + NOISE_GAUSS_PARAM * sigma * np.random.randn(*dmap.shape) + mu
    return noisy

def linear_noise(dmap, a = NOISE_LINEAR_PARAM):
    noisy = dmap + a * dmap.std() * np.random.random(dmap.shape)
    return noisy

def blur_filter(dmap, gauss_size = 1, stdev = 1, dim= 2 ):
    """
    :param dmap:
    :param gauss_size:
    :param stdev:
    :param dim:
    :return:
    """

    kernel = create_kernel(KERNEL_GAUSSIAN, dim, NOISE_GAUSSIAN_SIZE, NOISE_GAUSSIAN_STDEV)
    dm = scipy.signal.fftconvolve(dmap, kernel, mode='same')
    return dm



def add_noise(dmap, dim = 2):
    noise = gauss_noise(dmap)
    noise = linear_noise(noise)
    noise = blur_filter(noise, dim)
    return noise

def make_noisy_tomogram(tomogram, dim = 2):
    noisy_dmap = add_noise(tomogram.density_map, dim)
    noisy_tomogram = Tomogram(noisy_dmap, tomogram.composition)
    return noisy_tomogram




if __name__ == '__main__':
    from TomogramGenerator import *
    from TemplateGenerator import generate_tilted_templates
    import CommonDataTypes
    from VisualUtils import compare_reconstruced_tomogram

    templates = generate_tilted_templates()

    criteria = [4, 3, 0, 0]
    tomogram = generate_random_tomogram(templates, criteria, 2)
    noisy_tomogram = make_noisy_tomogram(tomogram)

    compare_reconstruced_tomogram(tomogram, noisy_tomogram, True)


