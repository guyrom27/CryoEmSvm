import time
import numpy as np
import matplotlib.pyplot as plt

from TemplateGenerator import generate_tilted_templates_2d, generate_templates_3d, TemplatesType
from TomogramGenerator import generate_random_tomogram_set
from Configuration import CONFIG
from SvmTrain import svm_train

project_path = 'C:\\dev\\Anaconda\\CryoEmSvm\\'


def time_train(templates, tomograms):
    start = time.time()
    svm_train(templates, tomograms)
    end = time.time()
    return end - start


def time_all(start_template_dim, step_template_dim, stop_template_dim, start_tomogram_dim, step_tomogram_dim,
             stop_tomogram_dim,  dim, angel_res, templates_type, criteria, noise, save, path):
    result_matrix = np.zeros(((stop_template_dim - start_template_dim) // step_template_dim + 1,
                              (stop_tomogram_dim - start_tomogram_dim) // step_tomogram_dim + 1))
    for i, template_dim in enumerate(range(start_template_dim, stop_template_dim + 1, step_template_dim)):
        CONFIG.TEMPLATE_DIMENSION = template_dim
        print('Template size: {0}'.format(template_dim))
        if dim == 2:
            templates = generate_tilted_templates_2d(angel_res)
        else:
            templates = generate_templates_3d(project_path + 'Chimera\\Templates\\', angel_res, templates_type)
        for j, tomogram_dim in enumerate(range(start_tomogram_dim, stop_tomogram_dim + 1, step_tomogram_dim)):
            CONFIG.TOMOGRAM_DIMENSION = tomogram_dim
            print('Tomogram size: {0}'.format(tomogram_dim))
            if dim == 2:
                tomograms = generate_random_tomogram_set(templates, criteria, 10, dim, None, noise)
            else:
                tomograms = generate_random_tomogram_set(templates, criteria, 1, dim, None, noise)
            result_matrix[i, j] = time_train(templates, tomograms)
            print('Finished after: {0} sec'.format(result_matrix[i, j]))
        if save:
            np.save(path, result_matrix)
    return result_matrix


if __name__ == '__main__':
    print('2D')
    result = time_all(15, 10, 35, 100, 10, 140, 2, 15, None, [1,1,1], False, False, None)
    np.save('time_tomograms_2d_15_10_35_100_10_140.npy', result)
    print('3D')
    result = time_all(15, 10, 35, 100, 10, 140, 3, 60, TemplatesType.ALL_3D, [2,2,2], False, True, 'time_tomograms_3d_15_10_35_100_10_14')
    np.save('time_tomograms_3d_15_10_35_100_10_14.npy', result)

    # result = np.load('time_tomograms_2d_15_10_35_100_10_140.npy')
    # plt.plot(result[:,3])
    # plt.ylabel('Time [sec]')
    # plt.xlabel('(Template size - 15)/10')
    # plt.title('2D Time vs Template size')
    # plt.show()
