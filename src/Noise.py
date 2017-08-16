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

def blur_filter(dmap, gauss_size = 1, stdev = 0.1, dim = 2 ):
    from CandidateSelector import create_kernel
    KERNEL_GAUSSIAN = 'GAUSSIAN'
    kernel = create_kernel(KERNEL_GAUSSIAN, dim)
    dm = scipy.signal.fftconvolve(dmap, kernel, mode='same')
    return dm



def add_noise(dmap):
    noise = gauss_noise(dmap)
    noise = linear_noise(noise)
    noise = blur_filter(noise)
    return noise

def make_noisy_tomogram(tomogram):
    import CommonDataTypes
    noisy_dmap = add_noise(tomogram.density_map)
    noisy_tomogram = CommonDataTypes.Tomogram(noisy_dmap, tomogram.composition)
    return noisy_tomogram




if __name__ == '__main__':
    from TomogramGenerator import *
    from TemplateGenerator import generate_tilted_templates
    import CommonDataTypes
    from DebugMain import compare_reconstruced_tomogram

    templates = generate_tilted_templates()

    criteria = [4, 3, 0, 0]
    tomogram = generate_random_tomogram(templates, templates[0][0].density_map.shape[0], criteria)
    noisy_tomogram = make_noisy_tomogram(tomogram)

    compare_reconstruced_tomogram(tomogram, noisy_tomogram, True)


