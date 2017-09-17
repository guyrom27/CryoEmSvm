from CommonDataTypes import Tomogram
from Configuration import CONFIG
from TemplateUtil import create_kernel, KERNEL_GAUSSIAN

import numpy as np
import scipy.signal


"""
Add different types  of noise to the density maps 
"""

def gauss_noise(dmap, sigma = None, mu = 0):
    if sigma is None:
        sigma = 0.3 * dmap.max()
    noisy = dmap + CONFIG.NOISE_GAUSS_PARAM * sigma * np.random.randn(*dmap.shape) + mu
    return noisy

def linear_noise(dmap, a = CONFIG.NOISE_LINEAR_PARAM):
    noisy = dmap + a * dmap.std() * np.random.random(dmap.shape)
    return noisy

def blur_filter(dmap, dim):
    """
    :param dmap:
    :param gauss_size:
    :param stdev:
    :param dim:
    :return:
    """

    kernel = create_kernel(KERNEL_GAUSSIAN, dim, CONFIG.NOISE_GAUSSIAN_SIZE, CONFIG.NOISE_GAUSSIAN_STDEV)
    dm = scipy.signal.fftconvolve(dmap, kernel, mode='same')
    return dm

def add_noise(dmap, dim):
    noise = gauss_noise(dmap)
    noise = linear_noise(noise)
    noise = blur_filter(noise, dim)
    if dim == 2:
        noise = linear_noise(noise)
    return noise

def make_noisy_tomogram(tomogram, dim):
    noisy_dmap = add_noise(tomogram.density_map, dim)
    noisy_tomogram = Tomogram(noisy_dmap, tomogram.composition)
    return noisy_tomogram


if __name__ == '__main__':
    from TomogramGenerator import *
    from TemplateGenerator import generate_tilted_templates, load_templates_3d
    import CommonDataTypes
    from VisualUtils import compare_reconstruced_tomogram, slider3d

    #templates = generate_tilted_templates()
    templates = load_templates_3d(r'..\Chimera\Templates'+'\\')
    #criteria = [4, 3, 0, 0]
    criteria = [5, 6, 6]
    tomogram = generate_random_tomogram(templates, criteria, 3)
    slider3d(tomogram.density_map)
    noisy_tomogram = make_noisy_tomogram(tomogram, 3)
    slider3d(noisy_tomogram.density_map)

    #compare_reconstruced_tomogram(tomogram, noisy_tomogram, True)


