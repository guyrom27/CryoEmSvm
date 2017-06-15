class EulerAngle:
    """
    This represents the angles of a rotated rigid body.
    alpha is ...
    """
    def __init__(self, alpha, beta, gamma):

class SixPosition:
    def __init__(self, COM_position, orientation):
        self.COM_position = COM_position
        self.orientation = orientation




class Candidate:
    """
    This is the result of candidate selection from a tomogram
    """

    def __init__(self, six_position, label = None):
        self.six_position = six_position
        self.label = label
        self.features = None

    def set_featers(self, features):
        self.features = features

    def set_label(self, label):
        self.label = label





class Template:
    def __init__(self, label, density_map):
        self.label = label
        self.density_map = density_map

class TiltedTemplate (Template):
    def __init__(self,  label, density_map, orientation):
        super.__init__(self,label,density_map)
        self.orientation = orientation





class Tomogram:
    """
    This is either a self generated tomogram with composition set to the ground truth
    or a tomogram after identification with the compisition as the identified components
    composition is a list of labeled candidates
    """
    def __init__(self, density_map, composition):
        self.density_map = density_map
        self.composition = composition

