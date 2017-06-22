DISTANCE_THRESHOLD = 0.5
JUNK_ID = 0

import numpy as np

class Labeler:
    #make abstract method
    #find out the appropriate label
    def label(self, candidate):
        return None

class PositionLabeler:
    def __init__(self, composition):
        self.composition = composition
        #elements of composition who were found during labeling
        self.associated_composition = []

    def label(self, candidate, set_label = True):
        candidate_label = JUNK_ID
        candidate.set_label(JUNK_ID)
        for real_candidate in self.composition:
            dist_squared = np.linalg.norm(np.array(candidate.six_position.COM_position) - np.array(real_candidate.six_position.COM_position))
            if dist_squared <= DISTANCE_THRESHOLD**2:
                candidate_label = real_candidate.label

        if set_label:
            candidate.set_label(candidate_label)
        return candidate_label


class SvmLabeler(Labeler):
    def __init__(self, svm):
        self.svm = svm

    def label(self, candidate, set_label = True):
        candidate_label = self.svm.predict(np.array([candidate.features]))
        if set_label:
            candidate.set_label(candidate_label)
        return candidate_label
