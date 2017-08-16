import numpy as np
from scipy.optimize import linear_sum_assignment
from Constants import DISTANCE_THRESHOLD


def find_best_match(candidate, compostion):
    min_dist = DISTANCE_THRESHOLD
    match = None
    for c in compostion:
        dist2 = calculate_L2_dist(c, candidate)
        if(min_dist > dist2):
            min_dist = dist2
            match = c
    return match

def calculate_L2_dist(c1 ,c2):
    return np.linalg.norm(np.array(c1.get_position()) - np.array(c2.get_position()))

def short_candidate_print(c, message = None):
    string = "Pos = " + str(c.six_position) + "\tLabel = " + str(c.label)
    if message is not None:
        string = message + string
    print(string)



class MetricTester:
    """
    This will compare the ground truth compostion to the reconstucted compostion
    and will calculate ....
    """
    def __init__(self, true_composition, reco_composition, gt_tomogram=None, tomogram= None):
        self.gt_comp = true_composition             # The composition of the 'true' tomogram
        self.reco_comp = reco_composition           # The compostion of the reconstructed tomogram
        self.matches = {}
        self.match_gt_to_reco()
        self.statistics = {}
        #candidate -> list of (value, string)
        #each (value,string) represents a metric
        #where value is the result of the metric
        #and string is the message/name associated to it
        for c in reco_composition:
            self.statistics[c] = []
        self.COM_position()


        #add tomograms if needed


    def match_gt_to_reco(self):
        #if ambigious matchings are ever a problem, than
        #we can use scipy.optimize_linear_sum_assignment which
        #solves minimal matching in bipartite graph (n^3 time instead of n^2)

        for c in self.reco_comp:
            self.matches[c] = find_best_match(c, self.gt_comp) #None if no match is found
        for c in self.gt_comp:
            self.matches[c] = find_best_match(c, self.reco_comp) #None if no match is found

        #for debug: make sure that the mapping is consistant
        #i.e. if x is matched to y, then y should also be matched to x
        for c in self.reco_comp:
            match = self.matches[c]
            if match is not None and self.matches[match] != c:
                print("Warning: ambiguous match in Metric Tester")
        for c in self.gt_comp:
            match = self.matches[c]
            if match is not None and self.matches[match] != c:
                print("Warning: ambiguous match in Metric Tester")

    def print(self):
        for c in self.gt_comp:
            short_candidate_print(c,"====\nGround Truth:\n")
            print("=====\nGround Truth:\nPos= " + str(c.six_position) + "\tLabel = " + str(c.label))
            match = self.matches[c]
            if match is not None:
                short_candidate_print(c,"Reconstructed:\n")
                #print("Reconstructed:\nPos = " + str(match.six_position) + "\tLabel = " + str(match.label))
            else:
                print("No match")


    def COM_position(self):
        for c in self.reco_comp:
            match = self.matches[c]
            if match is not None:
                dist = calculate_L2_dist(c, match)
                self.statistics[c].append((dist, "Distance between centers"))


    def print_metrics(self):
        for c in self.reco_comp:
            print("=================")
            short_candidate_print(c, "Metrics for candidate ")
            for metric in self.statistics[c]:
                print(metric[1] + " = " + str(metric[0]) + "\t")

    def num_matched(self):
        n_gt = len(self.gt_comp)
        n_reco = len(self.reco_comp)