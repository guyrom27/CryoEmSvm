from TomogramGenerator import tomogram_generator, tomogram_loader

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
