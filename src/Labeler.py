

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

    # make abstract method
    def label(self, candidate):
        return None


class SvmLabeler(Labeler):
    def __init__(self, svm):
        self.svm = svm

    def label(self, candidate):
        return svm.predict(candidate.features)