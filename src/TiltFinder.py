from Constants import JUNK_ID

class TiltFinder:
    def __init__(self, max_correlations):
        """
        :param max_correlations: a data structure of type TemplateMaxCorrelations initialized according to the relevant tomogram and templates
        """
        self.max_correlations = max_correlations

    def find_best_tilt(self, candidate):
        if candidate.label == JUNK_ID:
            return #what should we return in case of junk? does it matter?
        candidate.six_position.tilt_id = self.max_correlations.best_tilt_ids[candidate.label][candidate.six_position.COM_position]


if __name__ == '__main__':
    from TemplateGenerator import generate_tilted_templates
    from TomogramGenerator import *
    from CommonDataTypes import Candidate
    from DebugMain import show_tomogram

    templates = generate_tilted_templates()

    criteria = [0, 2, 2, 1]
    tomogram = generate_random_tomogram(templates, criteria)
    show_tomogram(tomogram,None)
    composition = tomogram.composition
    candidates = []
    for c in composition:
        p = c.six_position.COM_position
        c_new = Candidate.fromTuple(c.label,c.six_position.tilt_id,p[0],p[1],p[2])
        candidates.append(c_new)
    from TemplateMaxCorrelations import TemplateMaxCorrelations
    max_correlations = TemplateMaxCorrelations(tomogram, templates)
    tilt_finder = TiltFinder(max_correlations)

    accuracy = 0.0
    for i in range(len(candidates)):
        #candidates[i].six_position.tilt_id = 0
        tilt_finder.find_best_tilt(candidates[i])
        if candidates[i].six_position.tilt_id == composition[i].six_position.tilt_id:
            accuracy += 1
    accuracy /= float(len(candidates))
    accuracy *= 100
    print("accuracy is " + str(accuracy) + "%")
    reco_tomogram = generate_tomogram_with_given_candidates(templates,candidates, 2)

    import DebugMain
    DebugMain.compare_reconstruced_tomogram(reco_tomogram,tomogram,plot_dif_map=True)
    '''
    for i in range(len(candidates)):
        candidates[i].set_label(1)

        #candidates[0].six_position.tilt_id = -1
        tilt_finder.find_best_tilt(candidates[i])
        print("value from find tilt: " + str(candidates[i].six_position.tilt_id))
        print("truth value: " + str(rand_tilts[i]))
    '''

