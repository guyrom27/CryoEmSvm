from TomogramGenerator import generate_tomogram_with_given_candidates
from Configuration import CONFIG
from MetricTester import MetricTester
from Metrics import Metrics
from ResultsMetrics import ResultsMetrics
from Labeler import JUNK_ID
import VisualUtils


def svm_view(evaluation_tomograms, templates, output_candidates):
    """
    Prints a summery of the results.
    :param evaluation_tomograms:    The tomograms that have been evaluated
    :param templates:               The templates with which the tomograms where evaluated
    :param output_candidates:       The output candidates of the tomograms
    """
    evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], CONFIG.DIM)

    metric_tester = MetricTester(evaluation_tomograms[0].composition,
                           [c for c in evaluated_tomogram.composition if c.label != JUNK_ID])
    metrics = Metrics()
    metrics.init_from_tester(metric_tester)

    metric_tester.print()
    print('')
    metric_tester.print_metrics()
    print('')

    # print metrics
    metrics.print_stat()
    print('')

    # result_metrics = ResultsMetrics(evaluation_tomograms[0].composition, output_candidates[0])
    # result_metrics.print_full_stats(short=False)
    if CONFIG.DIM == 2:
        VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram)
        VisualUtils.plt.show()
    else:
        ground_truth_tomogram = generate_tomogram_with_given_candidates(templates, evaluation_tomograms[0].composition, 3)
        VisualUtils.chimera_display(evaluation_tomograms[0], evaluated_tomogram, ground_truth_tomogram)