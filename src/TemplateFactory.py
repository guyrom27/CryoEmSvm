from TemplateGenerator import TemplateGenerator, template_loader, template_generator_solid, template_generator_3d_load


class TemplateFactory:
    def __init__(self, kind):
        assert TemplateGenerator.contains(kind)
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
        if self.kind == TemplateGenerator.LOAD:
            return template_loader(self.paths, self.save)
        elif self.kind == TemplateGenerator.SOLID:
            return template_generator_solid(self.paths)
        elif self.kind == TemplateGenerator.LOAD_3D:
            return template_generator_3d_load(self.paths)
        else:
            raise NotImplementedError('The generator %s is not implemented' % str(self.kind))


if __name__ == '__main__':
    print(TemplateGenerator.SOLID.value)
    print(TemplateGenerator.SOLID == 'SOLID')
    print('SOLID' == TemplateGenerator.SOLID)
    print(TemplateGenerator.keys())
    print('LOAD' in TemplateGenerator.keys())
    print(TemplateGenerator.contains('LOAD'))
    print(TemplateGenerator.contains(TemplateGenerator.LOAD))
    print('HOLLOW' in TemplateGenerator.keys())
    print(TemplateGenerator.contains('HOLLOW'))
