from TomogramGenerator import TomogramGenerator, tomogram_generator, tomogram_loader

class TomogramFactory:
    def __init__(self, kind):
        self.kind = kind
        self.save = False
        self.paths = None
        self.templates = None

    def set_templates(self, templates):
        self.templates = templates
        return self

    def set_paths(self, paths):
        self.paths = paths
        return self

    def set_save(self, value):
        self.save = value
        return self

    def build(self):
        # Assert that all the required values are set

        # build the appropriate generator
        if self.kind == TomogramGenerator.LOAD:
            assert self.paths is not None
            return tomogram_loader(self.paths, self.save)
        elif self.kind == TomogramGenerator.OLD_GENERATOR:
            assert self.templates is not None
            return tomogram_generator(self.templates)
        else:
            raise NotImplementedError('The generator %s is not implemented' % str(self.kind))
