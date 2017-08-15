from scipy import signal
from Constants import JUNK_ID

class TiltFinder:
    def __init__(self, max_correlations):
        self.max_correlations = max_correlations

    def find_best_tilt(self, candidate):
        if candidate.label == JUNK_ID:
            return #what should we return in case of junk? does it matter?
        candidate.six_position.tilt_id = self.max_correlations.best_tilt_ids[candidate.label][candidate.six_position.COM_position]

    #
    #
    #
    # def find_best_tilt(self, tomogram, candidate):
    #     if candidate.label == JUNK_ID:
    #         return #what should we return in case of junk? does it matter?
    #
    #     template = self.templates[candidate.label]
    #     max_correlation = 0
    #     best_tilt = -1
    #
    #     for tilted_template in template:
    #         #correlation = signal.correlate(tomogram.density_map, tilted_template.density_map, mode='same')
    #         correlation = signal.fftconvolve(tomogram.density_map, tilted_template.density_map, mode='same')
    #         #can't we just calculate the correlation? We dont need fft since
    #         #only want one position... seems kind of wasteful
    #         if max_correlation < correlation[candidate.six_position.COM_position]:
    #             max_correlation = correlation[candidate.six_position.COM_position]
    #             best_tilt = tilted_template.tilt_id
    #     if best_tilt == -1:
    #         print("weird behaviour in Tilt finder. No good tilt found. Max is smaller than 0")
    #         return
    #
    #     candidate.six_position.tilt_id = best_tilt

if __name__ == '__main__':
    from TemplateGenerator import generate_tilted_templates
    from TomogramGenerator import generate_tomogram_with_given_candidates
    from CommonDataTypes import Candidate
    import random
    from DebugMain import show_tomogram

    templates = generate_tilted_templates()
    rand_tilts = []
    for i in range(2):
        rand_tilts.append(random.randint(0, len(templates[1]) - 1))

    print(str(rand_tilts))
    candidates = (Candidate.fromTuple(1, rand_tilts[0], 15, 12), Candidate.fromTuple(1, rand_tilts[1], 23, 28))
    test_tomogram = generate_tomogram_with_given_candidates(templates, candidates)
    show_tomogram(test_tomogram,candidates)

    from TemplateMaxCorrelations import TemplateMaxCorrelations
    max_correlations = TemplateMaxCorrelations(test_tomogram, templates)
    tilt_finder = TiltFinder(max_correlations)

    for i in range(len(candidates)):
        candidates[i].set_label(1)

        #candidates[0].six_position.tilt_id = -1
        tilt_finder.find_best_tilt(candidates[i])
        print("value from find tilt: " + str(candidates[i].six_position.tilt_id))
        print("truth value: " + str(rand_tilts[i]))

