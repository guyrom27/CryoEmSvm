class EulerAngle:
    """
    This represents the angles of a rotated rigid body.
    alpha is ...
    """
    def __init__(self, Phi, Theta, Psi):
        self.Phi = Phi
        self.Theta = Theta
        self.Psi = Psi


class SixPosition:
    def __init__(self, COM_position, orientation):
        self.COM_position = COM_position
        self.orientation = orientation




class Candidate:
    """
    This is the result of candidate selection from a tomogram
    """

    def __init__(self, six_position, suggested_label=None, label = None):
        self.six_position = six_position
        self.suggested_label = suggested_label
        self.label = label
        self.features = None

    def set_featers(self, features):
        self.features = features

    def set_label(self, label):
        self.label = label




class TiltedTemplate:
    def __init__(self, density_map, orientation, template_id):
        self.template_id = template_id
        self.density_map = density_map
        self.orientation = orientation





class Tomogram:
    """
    composition is a list of labeled candidates, that represents the ground truth
    """
    def __init__(self, density_map, composition):
        self.density_map = density_map
        self.composition = composition

