from Constants import TEMPLATE_DIMENSION
from TemplateGenerator import template_generator_solid_2d
from TomogramGenerator import generate_random_tomogram, generate_tomogram_with_given_candidates
from SvmTrain import svm_train
from SvmEval import svm_eval

import VisualUtils


templates = list(template_generator_solid_2d(''))
training_tomograms = [generate_random_tomogram(templates, TEMPLATE_DIMENSION, [2,2])]

svm_and_templates =  svm_train(templates, training_tomograms)


evaultaion_tomograms = [generate_random_tomogram(templates, TEMPLATE_DIMENSION, [2,2])]
VisualUtils.show_tomogram(evaultaion_tomograms[0],[])
output_candidates = svm_eval(svm_and_templates, evaultaion_tomograms)

JUNK_ID = -1
non_junk_candidates = [c for c in output_candidates[0] if c.label != JUNK_ID]
evaluated_tomogram = generate_tomogram_with_given_candidates(templates, non_junk_candidates)
VisualUtils.show_tomogram(evaluated_tomogram,[])


VisualUtils.plt.show()