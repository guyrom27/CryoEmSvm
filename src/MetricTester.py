import numpy as np
from Constants import DISTANCE_THRESHOLD
from Labeler import JUNK_ID
from CommonDataTypes import EulerAngle

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


'''
eval,global/local, eval_error, name
'''




#todo: add option to save data to a log
#maybe add the option to write some of the data to a global log file for statistics?
#That way we can keep statistics over multiple tomograms

#Maybe add a mode where we only print the outliers? reletive to some tolerance levels?

class MetricTester:
    """
    This will compare the ground truth composition to the reconstructed composition
    and will calculate ....
    """
    def __init__(self, true_composition, reco_composition, gt_tomogram=None, tomogram= None):
        self.gt_comp = true_composition             # The composition of the 'true' tomogram
        self.reco_comp = []                         # The composition of the reconstructed tomogram
        self.junk_candidates = []                   #

        self.true_label = []
        self.wrong_label = []
        self.false_junk = []
        self.success_junk = []
        self.false_existence = []                   #no gt
        self.not_detected = []                      #gt but no detection in junk or id

        self.statistics = {}
        #candidate -> list of (value, string)
        #each (value,string) represents a metric
        #where value is the result of the metric
        #and string is the message/name associated to it
        self.global_statistics = []
        # a list of metrics that is not tied to a specific candidate
        # e.g. average center of mass distance, tilt success rate,
        # number of correct matches ect...

        self.gt_tomogram = gt_tomogram
        self.tomogram = tomogram
        self.matches = {}
        self.match_gt_to_reco(reco_composition)
        self.init_candidate_lists()


        for c in reco_composition:
            self.statistics[c] = []
        self.match_success_rates()
        self.COM_position()
        self.Tilt_comparison()
        self.correlation_comparison()
        #add tomograms if needed


    def match_gt_to_reco(self, reco_candidates):
        #if ambigious matchings are ever a problem, than
        #we can use scipy.optimize_linear_sum_assignment which
        #solves minimal matching in bipartite graph (n^3 time instead of n^
        for c in reco_candidates:
            if c.label == JUNK_ID:
                self.junk_candidates.append(c)
            else:
                self.reco_comp.append(c)

        for c in reco_candidates:
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


    def init_candidate_lists(self):
        for c in self.reco_comp:
            match = self.matches[c]
            if match is not None:
                if match.label == c.label:
                    self.true_label.append(c)   #matched truth and correct label
                else:
                    self.wrong_label.append(c)  #Found a candidate near truth, but it is mislabeled
            else:
                self.false_existence.append(c)  #False positive: detected a candidate which does not match the ground truth

        for c in self.junk_candidates:
            match = self.matches[c]
            if match is None:
                self.success_junk.append(c)     #Junk is not close to any gt
            elif self.matches[match] != c:
                self.success_junk.append(c)     #close junk candidate, but there is a closer non-junk candidate
            else:
                self.false_junk.append(c)       #False negative on SVM's end

        for c in self.gt_comp:
            if self.matches[c] is None:
                self.not_detected.append(c)     #False negetive on detection end:
                                                # ground truth candidate was not detected


    def print(self):
        for c in self.gt_comp:
            short_candidate_print(c, "====\nGround Truth:\n")
            #print("=====\nGround Truth:\nPos= " + str(c.six_position) + "\tLabel = " + str(c.label))
            match = self.matches[c]
            if match is not None:
                short_candidate_print(c, "Reconstructed:\n")
            else:
                print("No match")

    # TODO:
    # figure out exactly which cases we are interested in, and which
    # type of inconsistancy counts towards which case. When calculating
    # rates, we also need to consider what constitues a false case
    # (i.e. what do we need to divide by?)
    # Also consider what to do if we decide to include Junk Id
    def match_success_rates(self, print_all=True):
        n_label_match = len(self.true_label)
        n_mislabled = len(self.wrong_label)     #how many candidates were detected, but mislabeled
        n_svm_fn = len(self.false_junk)         #svm false negatives
        n_cd_fn = len(self.not_detected)        #candidate detector false negatives
        n_total = n_label_match + n_mislabled + n_svm_fn + n_cd_fn

        svm_success_rate = n_label_match*100.0/n_total
        message = ''
        message += "svm sucesss rate = {0:.2f}%".format(svm_success_rate)
        if n_mislabled != 0 or print_all:
            message += "\n\tnumber of mislabeled candidates = {}".format(n_mislabled)
        if n_svm_fn != 0 or print_all:
            message += "\n\tsvm false negatives = {}".format(n_svm_fn)
        if n_cd_fn != 0 or print_all:
            message += "\n\tundetected candidates = {}".format(n_cd_fn)
        self.global_statistics.append(("stat", (n_label_match, n_mislabled, n_svm_fn, n_cd_fn), message))

        #wrong_lable_rate = len(self.wrong_label)*100.0/(n_mislabled+n_label_match)

        '''
        n_cases = np.zeros((4,))
        n = 0.0
        for c in self.reco_comp:
            match = self.matches[c]
            n += 1
            if match is not None:
                if match.label == c.label:      #matched truth and correct label
                    n_cases[0] += 1
                else:
                    n_cases[1] += 1             #Found a candidate near truth, but it is mislabeled
            else:
                n_cases[2] += 1                 #False positive: detected a candidate which does not match the ground truth
        for c in self.gt_comp:
            if self.matches[c] is None:
                n_cases[3] += 1                 #False negative: ground truth candidate was not detected
                n += 1                          #Rejected a true candidates does this count as a label error?
        n_cases *= 100.0/n

        message = ""
        message += "match rate = {0:.2f}%".format(n_cases[0])
        if print_all:
            message += "," + "mislabel rate = {0:.2f}%".format(n_cases[1])
            message += ", " + "false positive rate = {0:.2f}%".format(n_cases[2])
            message += ", " + "false negative rate = {0:.2f}%".format(n_cases[3])
        self.global_statistics.append(message)
        '''
        return

    def COM_position(self):
        avg_dist = 0.0
        n = 0
        for c in self.reco_comp:
            match = self.matches[c]
            if match is not None:
                dist = calculate_L2_dist(c, match)
                self.statistics[c].append(("COM_dist", dist, "COM offset distance = {0:.3f}".format(dist)))
                avg_dist += dist
                n += 1
        if n > 0:
            avg_dist /= n
            if avg_dist != 0:
                self.global_statistics.append(("COM_dist", avg_dist, "Average COM offset  = {0:.3f}".format(avg_dist)))

    def correlation_comparison(self):
        from math import sqrt
        if self.gt_tomogram is None or self.tomogram is None:
            return
        dm1 = self.gt_tomogram.density_map.copy()
        dm2 = self.tomogram.density_map.copy()
        xcor = np.sum(np.multiply(dm1,dm2))
        xcor /= sqrt(np.sum(np.square(dm1)))
        xcor /= sqrt(np.sum(np.square(dm2)))
        self.global_statistics.append(("xcor",xcor , "Normalized xcor = {0:.3f}".format(xcor)))




    def Tilt_comparison(self):
        n_correct = 0
        n = 0.0
        for c in self.true_label:
            match = self.matches[c]
            if match is not None:
                a1 = EulerAngle.fromTiltId(c.get_tilt_id())
                a2 = EulerAngle.fromTiltId(match.get_tilt_id())
                a3 = (a1.Phi-a2.Phi, a1.Theta-a2.Theta, a1.Psi-a2.Psi)
                message = "Candidate Tilt = " + str(a1)
                message += ", True Tilt = " + str(a2)
                message += ", Difference = " + str(a3)
                n += 1
                if c.get_tilt_id() == match.get_tilt_id():
                    n_correct += 1
                self.statistics[c].append(("Tilt", (a1, a2), message))
        if n > 0:
            n = 100 * n_correct/n
            self.global_statistics.append(("Tilt", n, "Tilt Match Rate = {0:.2f}%".format(n)))


    def get_tilt_candidate_list(self, get_tolerated=False, tolerance_function=None):
        accepted_candidates = []
        rejected_candidates = []
        if tolerance_function is None:
            tolerance_function = lambda x: x[0] == x[1]
        for c in self.true_label:
            for metric in self.statistics[c]:
                if metric[0] == "Tilt":
                    if tolerance_function(metric[1]):
                        accepted_candidates.append(c)
                    else:
                        rejected_candidates.append(c)

        if get_tolerated:
            return accepted_candidates
        return rejected_candidates



    def print_metrics(self):
        for c in self.reco_comp:
            print("=================")
            short_candidate_print(c, "Metrics for candidate ")
            for metric in self.statistics[c]:
                print("\t" + metric[2])
        print("======Global Statistics======")
        for metric in self.global_statistics:
            print("\t" + metric[2])

    def print_to_file(self, path="Logger.txt"): #what should the default path be?
        file = open(path,'w')
        for c in self.reco_comp:
            file.write("=================\n")
            file.write("Metrics for Pos = {} Label = {}\n".format(str(c.get_six_position()),str(c.label)))
            for message in self.statistics[c]:
                file.write("\t" + message +"\n")
        file.write("======Global Statistics======\n")
        for message in self.global_statistics:
            file.write("\t" + message + "\n")
        file.close()

'''
    def match_success_rate(self):
        false_positive = 0.0
        false_negative = 0.0
        for c in self.reco_comp:
            if self.matches[c] is None:
                false_positive += 1
        for c in self.gt_comp:
            if self.matches[c] is None:
                false_negative += 1
        #if false_positive == 0 and false_negative == 0
'''