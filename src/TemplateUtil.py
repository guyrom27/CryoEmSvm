import numpy as np
from math import sqrt

#I think we should just call this function after generating the tomogram. Should this just be a module?
#I think we should also consider subtrackting the average first. That would make all the templates unit vectors
def normalize_template(template):
    factor = sqrt(np.sum(np.square(template.density_map)))
    if factor != 0:
        template.density_map /= factor
    else:
        print("Error normalizing template: L2 norm is zero")


if __name__ == '__main__':
    from TemplateGenerator import generate_tilted_templates

    templates = generate_tilted_templates()
    t = templates[1][2]
    norm = sqrt(np.sum(np.square(t.density_map)))
    print("norm before normalizing: " + str(norm))
    normalize_template(t)
    norm = sqrt(np.sum(np.square(t.density_map)))
    print("norm after normalizing: " + str(norm))
