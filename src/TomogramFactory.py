import pickle
import TomogramGenerator
from CommonDataTypes import Candidate
from Constants import DEFAULT_COMPOSITION_TUPLES_2D


# TODO: place holders for the tomogram generators
# TODO: move to other file
def tomogram_generator(paths, templates):
    composition = [Candidate.fromTuple(t) for t in DEFAULT_COMPOSITION_TUPLES_2D]
    for path in paths:
        tomogram = TomogramGenerator.generate_tomogram_with_given_candidates(templates, composition)
        with open(path, 'wb') as file:
            pickle.dump(tomogram, file)
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


class TomogramFactory:
    def __init__(self, templates):
        self.templates = templates
        self.save = False
        self.paths = None

    def set_paths(self, paths):
        self.paths = paths
        return self

    def set_save(self, value):
        self.save = value
        return self

    def build(self):
        # Assert that all the required values are set
        assert self.paths is not None

        # build the appropriate generator
        if self.templates is None:
            return tomogram_loader(self.paths, self.save)
        else:
            return tomogram_generator(self.paths, self.templates)
