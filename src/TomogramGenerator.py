from Constants import JUNK_ID
from CommonDataTypes import Tomogram, Candidate, SixPosition, EulerAngle
from Constants import TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSIONS_2D, TOMOGRAM_DIMENSIONS_3D
from StringComperableEnum import StringComperableEnum
from TemplateUtil import put_template

import numpy as np
import pickle
import random


# Ways to get tomogram
# + generate_tomogram_with_given_candidates
# + generate_random_tomogram
# - load tomogram from file
#   - with known composition
#   - with unkown composition
#
# Ways to get training set (set of tomogrmas)
# - generate random tomograms from criteria and number
# - load tomograms from files

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
        if candidate.label != JUNK_ID:
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
    separation = template_side_len

    # we don't want COM points too close to the sides
    template_radius = (template_side_len - 1) // 2
    gap_shape = [template_radius] * 3

    # pad a bit so we won't have boundary issues during detection
    gap_shape = [(x + 3) for x in gap_shape]

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
    random.shuffle(flat_ids)
    return [Candidate(SixPosition(pos_id[0], EulerAngle.rand_tilt_id()), label=pos_id[1]) for pos_id in zip(points, flat_ids)]


def generate_random_tomogram(templates, criteria, dim=2):
    """
    :param templates:  list of lists: first dimension is different template_ids second dimension is tilt_id
    :param criteria: list of integers. criteria[i] means how many instances of template_id==i should appear in the resulting tomogram
    :param dim 2 for 2D 3 for 3D
    :return: a random Tomogram according to the criteria
    """
    template_side = templates[0][0].density_map.shape[0]
    candidates = generate_random_candidates(template_side, criteria, dim)
    return generate_tomogram_with_given_candidates(templates, candidates, TOMOGRAM_DIMENSIONS_3D if dim == 3 else TOMOGRAM_DIMENSIONS_2D )


def generate_random_tomogram_set(templates, criteria, number_of_tomograms, dim=2, seed=None):
    """
    :param templates:  list of lists: first dimension is different template_ids second dimension is tilt_id
    :param criteria: list of integers. criteria[i] means how many instances of template_id==i should appear in the resulting tomogram
    :param number_of_tomograms: number of tomograms to generate
    :param dim 2 for 2D 3 for 3D
    :param seed seed to use for random generation
    :return:
    """
    if (seed == None):
        seed = random.randint(0, 2 ** 31 - 1)
    print('Using random seed: ', seed)
    random.seed(seed)

    for i in range(number_of_tomograms):
        yield generate_random_tomogram(templates, criteria, dim)



# -------------------------------------------------- Generators ------------------------------------------------------ #
class TomogramGenerator(StringComperableEnum):
    LOAD = 'LOAD'
    OLD_GENERATOR = 'OLD_GENERATOR'

# TODO: place holders for the tomogram generators
def tomogram_generator(paths, templates):
    from Constants import DEFAULT_COMPOSITION_TUPLES_2D
    composition = [Candidate.fromTuple(*t) for t in DEFAULT_COMPOSITION_TUPLES_2D]
    for path in paths:
        tomogram = generate_tomogram_with_given_candidates(templates, composition)
        yield tomogram


def tomogram_loader(paths, save):
    if not save:
        for path in paths:
            with open(path, 'rb') as file:
                yield pickle.load(file)
    else:
        for path in paths:
            with open(path, 'wb') as file:
                yield lambda x: pickle.dump(x, file)


# An example for a generator:
#   The generator is initialized with the various parameters needed to generate the tomograms as well as the number of
#   tomograms we wish to generate.
#   In this case we will generate random tomograms using criteria. To do that we need to
#   supply our generator with the templates we wish to use in the generation, template_side parameter and the criteria
#   to use in the generation of the tomograms as well as a parameter indicating whether we wish to generate 2D or 3D
#   tomograms.
#   A different generator might have been one that only loads the tomograms from files specified by paths.
#   Note that the generator can be documented as a regular function.
#   The generator can also be replaced with any thing that is iterable including any custom object designed to be used
#   as iterable.
#   ** Enabling usage from shell **
#   To enable the usage of this generator trough the shell command we need to do the following:
#       1. Add the generator to the TomogramGenerator enum to let our main know that this generator is available.
#          This is done by adding a line to the enum, e.g. EXAMPLE = 'EXAMPLE'
#       2. Add the generator to the TomogramFactory.
#          This is done by initially adding to the factory all the new values that we wish to receive that it doesn't
#          already does. In this case, template_side, criteria, dim and num_tomograms.
#          Then we would like to enable the factory to set those values. We do so by adding a field for eah value within
#          the __init__ function but not to the header of the function, rather we add the values in the body of the
#          function with default values of our choise (Most often None to indicate that it is a required variable, i.e.
#          must be set before our generator can be used).
#
#               def __init__(self, kind):
#                   ...
#                   self.template_side = 50
#                   self.criteria = None
#                   self.dim = 2
#                   self.num_tomograms = 0  # 0 is asserted to be false so this being set to 0 indicate that it is a
#                                             required
#
#          Then we will add setter functions for each variable (or we could be lazy and set the values directly but this
#          is a bad practice). Notice than the setters should return the factory itself for then to be chainable (i.e.
#          tomograms = TomogramFactory(TomogramGenerator.EXAMPLE).set_templates(...)...set_num_tomograms(...).build() )
#
#               def set_template_side(template_side)
#                   self.template_side = template_side
#                   return self
#
#          And so on.
#          Lastly we add the generator to the switch case (if elif in python) of the factory.
#
#               def build():
#               ...
#               if self.kind == TomogramGenerator.LOAD:
#                   ...
#               elif self.kind == TomogramGenerator.EXAMPLE:
#                   # Here we assert that everything that we require is present
#                   assert self.templates is not None
#                   assert self.tempalte_side > 5
#                   assert self.criteria
#                   ...
#                   return tomogram_example_generator_random(self.templates, ..., self.dim, self.num_tomograms)
#               else:
#                   ...
#       3. Add any new values that the shell command didn't previously accept to the command.
#          This is done by adding the arguments to the correct parser. For more information about how to add an
#          argument look up argparse.
def tomogram_example_generator_random(templates, template_side, criteria, dim, num_tomograms):
    for _ in range(num_tomograms):
        yield generate_random_tomogram(templates, criteria, dim)


if __name__ == '__main__':
    pass
