DISTANCE_THRESHOLD = 0.5

import numpy as np

class Labeler:
    #make abstract method
    #find out the appropriate label
    def label(self, candidate):
        return None

JUNK_ID = 0

class PositionLabeler:
    def __init__(self, composition):
        self.composition = composition
        #elements of composition who were found during labeling
        self.associated_composition = []

    # make abstract method
    def label(self, candidate):
        candidate.set_label(JUNK_ID)
        for real_candidate in self.composition:
            dist_vec = np.array(candidate.six_position.COM_position) - np.array(real_candidate.six_position.COM_position)
            if np.dot(dist_vec,dist_vec) <= DISTANCE_THRESHOLD**2:
                candidate.set_label(real_candidate.label)
        return candidate.label


class SvmLabeler(Labeler):
    def __init__(self, svm):
        self.svm = svm

    def label(self, candidate):
        print(candidate)
        return self.svm.predict(candidate.features)
