from Constants import JUNK_ID, DISTANCE_THRESHOLD

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

    def label(self, candidate):
        candidate.set_label(JUNK_ID)
        candidate.set_ground_truth(None)

        for real_candidate in self.composition:
            dist_squared = np.linalg.norm(np.array(candidate.six_position.COM_position) - np.array(real_candidate.six_position.COM_position))
            if dist_squared <= DISTANCE_THRESHOLD**2:
                candidate.set_label(real_candidate.label)
                candidate.set_ground_truth(real_candidate)
        return candidate.label


class SvmLabeler(Labeler):
    def __init__(self, svm):
        self.svm = svm

    def label(self, candidate):
        candidate_label = self.svm.predict(np.array([candidate.features]))
        candidate.set_label(candidate_label[0]) #for some reason candidate label is an array
        return candidate_label
