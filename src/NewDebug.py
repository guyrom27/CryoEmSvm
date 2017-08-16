from Constants import TEMPLATE_DIMENSION, JUNK_ID
from TemplateGenerator import generate_tilted_templates_2d, load_templates_3d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates, generate_random_tomogram_set
from SvmTrain import svm_train
from SvmEval import svm_eval
from MetricTester import MetricTester
import VisualUtils

# train
criteria = [1,2]
number_of_tomograms = 1
dim = 3

# create templates
if dim == 2:
    templates = generate_tilted_templates_2d()
elif dim == 3:
    templates = load_templates_3d(r'..\Chimera\Templates' + '\\')
else:
    assert(False)

# train
print("Training")
training_tomograms = generate_random_tomogram_set(templates, criteria, number_of_tomograms, dim)
svm_and_templates = svm_train(templates, training_tomograms)

# eval
print("Evaluating")
evaluation_tomograms = [generate_random_tomogram(templates, criteria, dim)]
output_candidates = svm_eval(svm_and_templates, evaluation_tomograms)
evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], dim)

# show results
print("Results")
metrics = MetricTester(evaluation_tomograms[0].composition, [c for c in evaluated_tomogram.composition if c.label != JUNK_ID])
metrics.print_metrics()
if dim == 2:
    VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram)
    VisualUtils.plt.show()


