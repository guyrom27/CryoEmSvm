from enum import Enum, auto
import pickle
import numpy as np

import TemplateGenerator


# TODO: Place holders for template generator
# TODO: move to other file
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
    templates = TemplateGenerator.generate_tilted_templates()
    for i, path in enumerate(paths):
        template = templates[i]
        with open(path, 'wb') as file:
            pickle.dump(template, file)
        yield template


def template_generator_fuzzy(paths):
    yield NotImplementedError('Generator fuzzy not implemented')


class Generator(Enum):
    # Set auto value generation to the name of the key
    def _generate_next_value_(name, start, count, last_values):
        return name

    # Override equality checks to accept string
    def __eq__(self, other):
        if isinstance(other, Generator):
            return super(Generator, self).__eq__(other)
        else:
            return self.value == other

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is not NotImplemented:
            return not result
        return result

    # Shortcut to the keys
    @staticmethod
    def keys():
        return Generator.__members__.keys()

    # Define contains to enable sort of 'in' query for strings on the values in the enum
    @staticmethod
    def contains(item):
        if isinstance(item, Generator):
            return item in Generator
        else:
            return item in Generator.keys()

    LOAD = auto()
    SOLID = auto()
    FUZZY = auto()


class TemplateFactory:
    def __init__(self, kind):
        assert Generator.contains(kind)
        self.kind = kind
        self.paths = None
        self.save = False

    def set_paths(self, paths):
        self.paths = paths
        return self

    def set_save(self, paths):
        self.save = True
        return self

    def build(self):
        # Assert that all the required values are set
        assert self.paths is not None

        # build the appropriate generator
        if self.kind == Generator.LOAD:
            return template_loader(self.paths, self.save)
        elif self.kind == Generator.SOLID:
            return template_generator_solid(self.paths)
        elif self.kind == Generator.FUZZY:
            return template_generator_fuzzy(self.paths)
        else:
            raise NotImplementedError('The generator %s is not implemented' % str(self.kind))


class NormalizedTemplateFactory(TemplateFactory) :
    def __init__(self, kind):
        TemplateFactory.__init__(self, kind)

    def build(self):
        for template in TemplateFactory.build(self):
            yield self.normalize(template)


    def normalize(self, template):
        from math import sqrt
        factor = sqrt(np.sum(np.square(template.density_map))) #calculate the L2 norm of the template
        if factor != 0:
            template.density_map /= factor
        else:
            print("Error normalizing template: L2 norm is zero")
        return template


if __name__ == '__main__':
    print(Generator.SOLID.value)
    print(Generator.SOLID == 'SOLID')
    print('SOLID' == Generator.SOLID)
    print(Generator.keys())
    print('LOAD' in Generator.keys())
    print(Generator.contains('LOAD'))
    print(Generator.contains(Generator.LOAD))
    print('HOLLOW' in Generator.keys())
    print(Generator.contains('HOLLOW'))
