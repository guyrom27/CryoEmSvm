from Labeler import JUNK_ID
from TemplateGenerator import generate_tilted_templates_2d, load_templates_3d, generate_templates_3d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates, generate_random_tomogram_set
from CommonDataTypes import EulerAngle
from SvmTrain import svm_train
from SvmEval import svm_eval
from Noise import make_noisy_tomogram
from MetricTester import MetricTester
from ResultsMetrics import ResultsMetrics
from Metrics import Metrics
import VisualUtils
import pickle
import configparser

# load configuration
config_path = 'testing_2d.config'
config = configparser.ConfigParser()
config.read(config_path)
to_int_list = lambda string: [int(val) for val in string.replace('[','').replace(']','').split(',')]

# general
dim = config['DEFAULT'].getint('dim')
angle_res = config['DEFAULT'].getint('angle_res')
seed = config['DEFAULT'].get('seed')
add_noise = config['DEFAULT'].getboolean('add_noise')
svm_path = config['DEFAULT'].get('svm_path')
template_file_path = config['DEFAULT'].get('template_file_path')

# training
training_criteria = to_int_list(config['train']['criteria'])
number_of_training_tomograms = config['train'].getint('number_of_tomograms')
train = config['train'].getboolean('train')
generate_templates = config['train'].getboolean('generate_templates')
templates_type = config['train'].get('templates_type')

#evaluation
test_criteria = to_int_list(config['evaluate']['criteria'])
number_of_test_tomograms = config['evaluate'].getint('number_of_tomograms')
metrics_input_file = config['evaluate'].get('metrics_input_file')
metrics_output_file = config['evaluate'].get('metrics_output_file')

# train
#seed = 1909615246

# create templates
if dim == 2:
    templates = generate_tilted_templates_2d(angle_res)
elif dim == 3:
    if generate_templates:
        templates = generate_templates_3d(template_file_path, angle_res, templates_type)
    else:
        templates = load_templates_3d(template_file_path)
else:
    assert(False)

# train
print("Training")
training_tomograms = generate_random_tomogram_set(templates, training_criteria, number_of_training_tomograms, dim, seed, add_noise)
training_analyzers = []

if train:
    svm_and_templates = svm_train(templates, training_tomograms, training_analyzers)
    with open(svm_path, 'wb') as file:
        pickle.dump(svm_and_templates, file)
else:
    with open(svm_path, 'rb') as file:
        svm_and_templates = pickle.load(file)
    # compatibilty with saar's code
    if isinstance(svm_and_templates,tuple):
        svm = svm_and_templates[0]
    svm_and_templates = (svm, (EulerAngle.Tilts, templates))


# eval
print("Evaluating")

aggregated_metrics = Metrics()
event_metrics = Metrics()
if metrics_input_file is not None:
    with open(metrics_input_file, 'rb') as file:
        aggregated_metrics = pickle.load(file)

print_each_event = False

for i in range(number_of_test_tomograms):
    evaluation_tomograms = [generate_random_tomogram(templates, test_criteria, dim, noise=add_noise)]
    output_candidates = svm_eval(svm_and_templates, evaluation_tomograms)
    evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0], dim)
    metric_tester = MetricTester(evaluation_tomograms[0].composition, output_candidates[0])
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
else:
    VisualUtils.slider3d(evaluated_tomogram.density_map)
    VisualUtils.slider3d(evaluation_tomograms[0].density_map)
    VisualUtils.slider3d(evaluation_tomograms[0].density_map - evaluated_tomogram.density_map)
print("Done")
