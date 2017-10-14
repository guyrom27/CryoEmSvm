from TemplateGenerator import generate_tilted_templates_2d, generate_templates_3d, TemplatesType, load_templates_3d
from TomogramGenerator import generate_random_tomogram_set, generate_random_tomogram
from SvmTrain import svm_train
from SvmEval import svm_eval
from SvmView import svm_view
from Configuration import CONFIG

CONFIG.load_config(r'../LiveDemonstration/config_2d.txt')

templates = generate_tilted_templates_2d(angle_res=33)

train_tomograms = generate_random_tomogram_set(templates=templates, criteria=[3,4,1,5], number_of_tomograms=10, dim=2, seed=1, noise=True)

svm_and_templates = svm_train(templates=templates, tomograms=train_tomograms)

eval_tomogram = [generate_random_tomogram(templates=templates, criteria=[4,2,5,5], dim=2, noise=True)]

eval_result = svm_eval(svm_and_templates=svm_and_templates, tomograms=eval_tomogram)

svm_view(evaluation_tomograms=eval_tomogram, templates=templates, output_candidates=eval_result)

if __name__ == '__main__':
    pass
