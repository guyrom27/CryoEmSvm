from Labeler import JUNK_ID
from TemplateGenerator import generate_tilted_templates_2d, load_templates_3d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates, generate_random_tomogram_set
from CommonDataTypes import Tomogram
from SvmTrain import svm_train
from SvmEval import svm_eval
from Noise import make_noisy_tomogram
from MetricTester import MetricTester
from ResultsMetrics import ResultsMetrics
from Metrics import Metrics
import VisualUtils
import pickle

# train
#criteria = [2, 2, 4, 4]     #2D
criteria = [5, 5, 5]          #3D
number_of_training_tomograms = 15
number_of_test_tomograms = 1
dim = 3
#seed = 1909615246
seed = 897652943
train = True
add_noise = True
svm_path = r'..\TrainedSVM\15_Noise_Geo_3D_333.pkl'
metrics_input_file = None
metrics_output_file = r'..\SVM_Metrics_Results\15_Noise_Geo_3D_333.pkl'
#metrics_output_file = r'..\SVM_Metrics_Results\100_Noise_2D_2342.pkl'
#metrics_input_file = r'..\SVM_Metrics_Results\1_Noise_3D.pkl'
#metrics_output_file = r'..\SVM_Metrics_Results\1_Noise_3D.pkl'

# create templates
if dim == 2:
    templates = generate_tilted_templates_2d()
elif dim == 3:
    templates = load_templates_3d(r'..\Chimera\GeometricTemplates' + '\\')
else:
    assert(False)

# train
print("Training")
training_tomograms = generate_random_tomogram_set(templates, criteria, number_of_training_tomograms, dim, seed, add_noise)
training_analyzers = []

if dim == 2:
    if train:
        svm_and_templates = svm_train(templates, training_tomograms, training_analyzers)
        with open(svm_path, 'wb') as file:
            pickle.dump(svm_and_templates, file)
    else:
        with open(svm_path, 'rb') as file:
            svm_and_templates = pickle.load(file)
else:
    if train:
        svm_and_templates = svm_train(templates, training_tomograms, training_analyzers)
        with open(svm_path, 'wb') as file:
            pickle.dump(svm_and_templates[0], file)
    else:
        with open(svm_path, 'rb') as file:
            svm = pickle.load(file)
            svm_and_templates = (svm, templates)

#criteria = [2, 3, 4, 2]
#criteria = [6, 6, 0, 0]
criteria = [3, 3, 3]
# eval
print("Evaluating")

aggregated_metrics = Metrics()
event_metrics = Metrics()
if metrics_input_file is not None:
    with open(metrics_input_file, 'rb') as file:
        aggregated_metrics = pickle.load(file)

print_each_event = True

for i in range(number_of_test_tomograms):
    evaluation_tomograms = [generate_random_tomogram(templates, criteria, dim, noise=add_noise)]
    output_candidates = svm_eval(svm_and_templates, evaluation_tomograms)
    #evaluated_tomogram = Tomogram(None, output_candidates[0])
    evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], dim)
    metric_tester = MetricTester(evaluation_tomograms[0].composition, evaluated_tomogram.composition)
    event_metrics.init_from_tester(metric_tester)
    if print_each_event:
        print("===================")
        event_metrics.print_stat()
        print("===================")
        #VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram, True)
    aggregated_metrics.merge(event_metrics)

'''
if add_noise:
    evaluation_tomograms = [make_noisy_tomogram(generate_random_tomogram(templates, criteria, dim), dim)]
else:
    evaluation_tomograms = [generate_random_tomogram(templates, criteria, dim)]

evaluation_analyzers = []
output_candidates = svm_eval(svm_and_templates, evaluation_tomograms, evaluation_analyzers)
'''


#evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], dim)

# show results
print('Results')



if metrics_output_file is not None:
    with open(metrics_output_file, 'wb') as file:
        pickle.dump(aggregated_metrics, file)

metric_tester = MetricTester(evaluation_tomograms[0].composition, [c for c in evaluated_tomogram.composition if c.label != JUNK_ID])
#metrics.print_metrics()
metric_tester.print()
print('')
metric_tester.print_metrics()
print('')
aggregated_metrics.print_stat()


print('')
#result_metrics = ResultsMetrics(evaluation_tomograms[0].composition, output_candidates[0])
#result_metrics.print_full_stats()
if dim == 2:
    VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram)
    VisualUtils.plt.show()

print("Done")
