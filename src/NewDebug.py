from TemplateGenerator import template_generator_solid_2d
from TomogramGenerator import ???
from SvmTrain import svm_train
from SvmEval import svm_eval


template_generator = template_generator_solid_2d('')
tomogram_geneartor = ???

(svm_and_templates,tomograms) =  svm_train(template_generator, tomogram_generator, True)

tomogram = ???
output_candidates, output_tomogram = svm_eval(svm_and_templates, tomogram, True)