from TemplateGenerator import Generator, template_loader, template_generator_solid, template_generator_3d_load


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
        elif self.kind == Generator.LOAD_3D:
            return template_generator_3d_load(self.paths)
        else:
            raise NotImplementedError('The generator %s is not implemented' % str(self.kind))


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
