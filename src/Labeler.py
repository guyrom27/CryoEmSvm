

class Labeler:
    #make abstract method
    def label(self, candidate):
        return None


class PositionLabeler:
    def __init__(self, composition):
        self.composition = composition

    # make abstract method
    def label(self, candidate):
        #how is label defined?
        return None


class SvmLabeler(Labeler):
    def __init__(self, svm):
        self.svm = svm

    def label(self, candidate):
        return svm.predict(candidate.features)