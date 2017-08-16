from Constants import TEMPLATE_DIMENSION, JUNK_ID
from TemplateGenerator import generate_tilted_templates_2d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates,\
    tomogram_example_generator_random
from SvmTrain import svm_train
from SvmEval import svm_eval
from MetricTester import MetricTester

import VisualUtils

# train
templates = generate_tilted_templates_2d()
training_tomograms = [generate_random_tomogram(templates, TEMPLATE_DIMENSION, [2,2]) for i in range(5)]
# Using the example generator, we pass the required parameters
#training_tomograms = tomogram_example_generator_random(templates, TEMPLATE_DIMENSION, [2,2], 2, num_tomograms=1)
svm_and_templates = svm_train(templates, training_tomograms)

# The generator can be used here as well but since generators are not subscribtable the indexing would not work.
# If we were to use a custom object that supports the indexing as well as lazy generation the we could get the best of
# both worlds (Even though this sounds improbable because to use indexing we need to keep the yielded tomograms and by
# doing so we negate the advantage of lazy generation that enables us to discard used values).
# A way in which this could be used is for example
#evaultaion_tomograms = list(
#    tomogram_example_generator_random(templates, TEMPLATE_DIMENSION, [2,2], 2, num_tomograms=1))

# eval
evaluation_tomograms = [generate_random_tomogram(templates, TEMPLATE_DIMENSION, [2,2])]
output_candidates = svm_eval(svm_and_templates, evaluation_tomograms)
evaluated_tomogram = generate_tomogram_with_given_candidates(templates, output_candidates[0])

# test results
metrics = MetricTester(evaluation_tomograms[0].composition, [c for c in evaluated_tomogram.composition if c.label != JUNK_ID])
metrics.print_metrics()
VisualUtils.compare_reconstruced_tomogram(evaluation_tomograms[0], evaluated_tomogram)
VisualUtils.plt.show()


