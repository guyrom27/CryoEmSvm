from Constants import TEMPLATE_DIMENSION
from TemplateGenerator import template_generator_solid_2d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates,\
    tomogram_example_generator_random
from SvmTrain import svm_train
from SvmEval import svm_eval

import VisualUtils


templates = list(template_generator_solid_2d(''))
training_tomograms = [generate_random_tomogram(templates, TEMPLATE_DIMENSION, [2,2])]

# Using the example generator, we pass the required parameters
#training_tomograms = tomogram_example_generator_random(templates, TEMPLATE_DIMENSION, [2,2], 2, num_templates=1)

svm_and_templates =  svm_train(templates, training_tomograms)

# The generator can be used here as well but since generators are not subscribtable the indexing would not work.
# If we were to use a custom object that supports the indexing as well as lazy generation the we could get the best of
# both worlds (Even though this sounds improbable because to use indexing we need to keep the yielded tomograms and by
# doing so we negate the advantage of lazy generation that enables us to discard used values).
evaultaion_tomograms = [generate_random_tomogram(templates, TEMPLATE_DIMENSION, [2,2])]
# A way in which this could be used is for example
#evaultaion_tomograms = list(
#    tomogram_example_generator_random(templates, TEMPLATE_DIMENSION, [2,2], 2, num_templates=1))

VisualUtils.show_tomogram(evaultaion_tomograms[0],[])
output_candidates = svm_eval(svm_and_templates, evaultaion_tomograms)

JUNK_ID = -1
non_junk_candidates = [c for c in output_candidates[0] if c.label != JUNK_ID]
evaluated_tomogram = generate_tomogram_with_given_candidates(templates, non_junk_candidates)
VisualUtils.show_tomogram(evaluated_tomogram,[])


VisualUtils.plt.show()