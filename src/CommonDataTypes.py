class EulerAngle:
    """
    This represents the angles of a rotated rigid body.
    alpha is ...
    """
    def __init__(self, Phi, Theta, Psi):
        self.Phi = Phi
        self.Theta = Theta
        self.Psi = Psi

    def __str__(self):
        return str(tuple([self.Phi, self.Theta, self.Psi]))



class SixPosition:
    def __init__(self, COM_position, orientation):
        self.COM_position = COM_position    # 3 tuple
        self.orientation = orientation      # EulerAngle

    def __str__(self):
        return str(self.COM_position) + " " + str(self.orientation)




class Candidate:
    """
    This is the result of candidate selection from a tomogram
    """

    def __init__(self, six_position, suggested_label=None, label = None):
        self.six_position = six_position            # SixPosition
        self.suggested_label = suggested_label      # int
        self.label = label                          # int
        self.features = None                        # list

    def __str__(self):
        return "Position: " + str(self.six_position) + "\n" +\
               "Suggested Label: " + str(self.suggested_label) + "\n" +\
               "Label: " + str(self.label) + "\n" +\
               "Features: " + str(self.features) + "\n"

    def set_features(self, features):
        self.features = features

    def set_label(self, label):
        self.label = label



class TiltedTemplate:
    def __init__(self, density_map, orientation, template_id):
        self.template_id = template_id      # int
        self.density_map = density_map      # numpy 3d array
        self.orientation = orientation      # EulerAngle





class Tomogram:
    """
    composition is a list of labeled candidates, that represents the ground truth
    """
    def __init__(self, density_map, composition):
        self.density_map = density_map      # numpy 3d array
        self.composition = composition      # list of labeled candidates

