from Labeler import JUNK_ID
from Configuration import CONFIG
from TemplateGenerator import generate_tilted_templates_2d, load_templates_3d, generate_templates_3d, GEOMETRIC_3D, PDBS_3D, ALL_3D
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates, generate_random_tomogram_set
from SvmTrain import svm_train
from SvmEval import svm_eval
from MetricTester import MetricTester
from ResultsMetrics import ResultsMetrics
import VisualUtils

# general settings
dim = 2
angle_res = 60
generate_3D_tempaltes_type = GEOMETRIC_3D # None if we do not want to generate
template_path = CONFIG.CHIMERA_UTILS_PATH + 'Templates\\'


# training set settings
criteria = [2,3,5,2]
number_of_tomograms = 1
seed = 1909615246
#seed = 1909615
noise = True


# create templates
if dim == 2:
    templates = generate_tilted_templates_2d(angle_res)
elif dim == 3:
    # generate or load existing
    if generate_3D_tempaltes_type:
        print("Generating Templates")
        templates = generate_templates_3d(template_path,angle_res, generate_3D_tempaltes_type)
    else:
        templates = load_templates_3d(template_path)
else:
    assert(False)

# train
print("Training")
training_tomograms = generate_random_tomogram_set(templates, criteria, number_of_tomograms, dim, seed, noise)
training_analyzers = [] # required only for debugging
svm_and_templates = svm_train(templates, training_tomograms, training_analyzers)

# eval
print("Evaluating")
evaluation_tomograms = [generate_random_tomogram(templates, criteria, dim, noise)]
evaluation_analyzers = [] # required only for debugging
output_candidates = svm_eval(svm_and_templates, evaluation_tomograms, evaluation_analyzers)
evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], dim)

# show results
print('Results')
metrics = MetricTester(evaluation_tomograms[0].composition, [c for c in evaluated_tomogram.composition if c.label != JUNK_ID])
metrics.print_metrics()
print('')
result_metrics = ResultsMetrics(evaluation_tomograms[0].composition, output_candidates[0])
result_metrics.print_full_stats(short = False)
if dim == 2:
    VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram)
    VisualUtils.plt.show()

print("Done")

