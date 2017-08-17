import numpy as np
import scipy.signal

def gauss_noise(dmap, sigma = None, mu = 0):
    if sigma is None:
        sigma = 0.3 * dmap.max()
    noisy = dmap + 0.2 * sigma * np.random.randn(*dmap.shape) + mu
    return noisy

def linear_noise(dmap, a = 0.4):
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
    from CandidateSelector import create_kernel
    KERNEL_GAUSSIAN = 'GAUSSIAN'
    kernel = create_kernel(KERNEL_GAUSSIAN, dim)
    dm = scipy.signal.fftconvolve(dmap, kernel, mode='same')
    return dm



def add_noise(dmap, dim = 2):
    noise = gauss_noise(dmap)
    noise = linear_noise(noise)
    noise = blur_filter(noise, dim)
    return noise

def make_noisy_tomogram(tomogram, dim = 2):
    import CommonDataTypes
    noisy_dmap = add_noise(tomogram.density_map, dim)
    noisy_tomogram = CommonDataTypes.Tomogram(noisy_dmap, tomogram.composition)
    return noisy_tomogram




if __name__ == '__main__':
    from TomogramGenerator import *
    from TemplateGenerator import generate_tilted_templates
    import CommonDataTypes
    from VisualUtils import compare_reconstruced_tomogram

    templates = generate_tilted_templates()

    criteria = [4, 3, 0, 0]
    tomogram = generate_random_tomogram(templates, criteria)
    noisy_tomogram = make_noisy_tomogram(tomogram)

    compare_reconstruced_tomogram(tomogram, noisy_tomogram, True)


