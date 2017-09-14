from Constants import JUNK_ID
from TemplateGenerator import generate_tilted_templates_2d, load_templates_3d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates, generate_random_tomogram_set
from SvmTrain import svm_train
from SvmEval import svm_eval
from Noise import make_noisy_tomogram
from MetricTester import MetricTester
from ResultsMetrics import ResultsMetrics
from Metrics import Metrics
import VisualUtils
import pickle

# train
criteria = [3, 3, 3, 3]     #2D
#criteria = [3, 3]          #3D
number_of_training_tomograms = 1
number_of_test_tomograms = 1
dim = 3
#seed = 1909615246
seed = None
train = False
add_noise = True
svm_path = r'..\TrainedSVM\100_Noise_2D.pkl'

# create templates
if dim == 2:
    templates = generate_tilted_templates_2d()
elif dim == 3:
    templates = load_templates_3d(r'..\Chimera\Templates' + '\\')
else:
    assert(False)

# train
print("Training")
training_tomograms = generate_random_tomogram_set(templates, criteria, number_of_training_tomograms, dim, seed, add_noise)
training_analyzers = []

if train:
    svm_and_templates = svm_train(templates, training_tomograms, training_analyzers)
    with open(svm_path, 'wb') as file:
        pickle.dump(svm_and_templates, file)
else:
    with open(svm_path, 'rb') as file:
        svm_and_templates = pickle.load(file)

criteria = [2, 3, 4, 2]

# eval
print("Evaluating")
evaluation_tomograms = generate_random_tomogram_set(templates, criteria, number_of_test_tomograms, dim, seed, add_noise)
'''
if add_noise:
    evaluation_tomograms = [make_noisy_tomogram(generate_random_tomogram(templates, criteria, dim), dim)]
else:
    evaluation_tomograms = [generate_random_tomogram(templates, criteria, dim)]
'''

evaluation_analyzers = []
output_candidates = svm_eval(svm_and_templates, evaluation_tomograms, evaluation_analyzers)


for i in range(len(evaluation_tomograms)):
    evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[i], dim)
    metrics = MetricTester(evaluation_tomograms[0].composition, evaluated_tomogram.composition)

evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], dim)

# show results
print('Results')
metrics = MetricTester(evaluation_tomograms[0].composition, [c for c in evaluated_tomogram.composition if c.label != JUNK_ID])
metrics.print_metrics()
print('')
#result_metrics = ResultsMetrics(evaluation_tomograms[0].composition, output_candidates[0])
#result_metrics.print_full_stats()
if dim == 2:
    VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram)
    VisualUtils.plt.show()

print("Done")

