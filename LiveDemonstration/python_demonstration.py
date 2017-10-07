from TemplateGenerator import generate_tilted_templates_2d
from TomogramGenerator import generate_random_tomogram_set, generate_random_tomogram
from SvmTrain import svm_train
from SvmEval import svm_eval
from SvmView import svm_view

templates = generate_tilted_templates_2d(33)

train_tomograms = generate_random_tomogram_set(templates, [2,3,4,1], 5, 2)

svm_and_templates = svm_train(templates, train_tomograms)

eval_tomogram = generate_random_tomogram(templates, [4,2,5,5], 2)

eval_result = svm_eval(svm_and_templates, [eval_tomogram])

svm_view([eval_tomogram], templates, eval_result)

if __name__ == '__main__':
    pass
