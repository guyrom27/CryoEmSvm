import numpy as np

class EulerAngle:
    """
    This represents the angles of a rotated rigid body.
    alpha is ...
    """
    Tilts = []

    def __init__(self, Phi, Theta, Psi):
        self.Phi = Phi
        self.Theta = Theta
        self.Psi = Psi

    @classmethod
    def init_tilts(cls, phi_n, tht_n, psi_n):
        """
        initialize the Tilts array so that we can associate an ID to a tilt
        :param x_n: is how many sample points x will have
        """
        from math import pi
        from numpy import linspace
        cls.Tilts = []
        MAX_PHI = 2*pi
        MAX_THT = pi
        MAX_PSI = 2*pi
        for phi in linspace(0, MAX_PHI, phi_n):
            for tht in linspace(0, MAX_THT, tht_n):
                for psi in linspace(0, MAX_PSI, psi_n):
                    cls.Tilts.append(EulerAngle(phi,tht,psi))

    @classmethod
    def fromTiltId(cls, tilt_id):
        return cls.Tilts[tilt_id]

    def __str__(self):
        return str(tuple([self.Phi, self.Theta, self.Psi]))

    @classmethod
    def rand_tilt_id(cls):
        import random
        return random.randint(0, len(cls.Tilts)-1 )

#DEFAULT
EulerAngle.init_tilts(15,15,15)



class SixPosition:
    def __init__(self, COM_position, tilt_id):
        """
        :param COM_position: 3 tuple
        :param tilt_id:  id that corresponds to EulerAngle's tilt_id
        """
        self.COM_position = COM_position    # 3 tuple
        self.tilt_id = tilt_id              # tilt id

    def __str__(self):
        return str(self.COM_position) + " " + str(self.tilt_id)




class Candidate:
    """
    This is a way to associate metadata to a posistion:
    label, suggested label, and feature vector
    """

    def __init__(self, six_position, suggested_label=None, label = None):
        self.six_position = six_position            # SixPosition
        self.label = label                          # int
        self.suggested_label = suggested_label      # int
        self.features = None                        # list

    @classmethod
    def fromTuple(cls, label, tilt_id, x, y, z = 0):
        return cls(SixPosition((x,y,z), tilt_id), label=label)

    def __str__(self):
        return "Position: " + str(self.six_position) + "\n" +\
               "Suggested Label: " + str(self.suggested_label) + "\n" +\
               "Label: " + str(self.label) + "\n" +\
               "Features: " + str(self.features) + "\n"

    def set_features(self, features):
        self.features = features

    def set_features(self, features):
        self.features = features

    def set_label(self, label):
        self.label = label



class TiltedTemplate:
    def __init__(self, density_map, tilt_id, template_id):
        self.template_id = template_id      # int
        self.density_map = density_map      # numpy 3d array
        self.tilt_id = tilt_id              # EulerAngle

    @classmethod
    def fromFile(cls, path, tilt_id, template_id):
        return cls(np.load(path), tilt_id, template_id)





class Tomogram:
    """
    composition is a list of labeled candidates, that represents the ground truth
    """
    def __init__(self, density_map, composition):
        self.density_map = density_map      # numpy 3d array
        self.composition = composition      # list of labeled candidates

