import argparse
from SvmTrain import SUPPORTED_GENERATORS, svm_train
from SvmEval import svm_eval

SUPPORTED_COMMANDS = ('train', 'eval')

parser = argparse.ArgumentParser(description='Train or evaluate an SVM to classify electron density maps.')
subparsers = parser.add_subparsers(dest='command', help='Command to initiate.')

train_parser = subparsers.add_parser(SUPPORTED_COMMANDS[0])
train_parser.add_argument('svm_path', metavar='svm', nargs=1, type=str,
                          help='Path to save in the created svm.')
train_parser.add_argument('-t', '--templatepath', metavar='templatepath', dest='template_paths', nargs='+', type=str,
                         required=True,
                         help='Paths to the templates to be trained with.')
train_parser.add_argument('-d', '--datapath', metavar='datapath', dest='tomogram_paths', nargs='+', type=str,
                         required=True,
                         help='Paths to the tomograms to be trained on. If used with -g only the first path will be '
                              'used and it will be used to save the generated tomograms into.')
train_parser.add_argument('-g', '--generate', choices=SUPPORTED_GENERATORS, dest='generator', nargs=1, type=str,
                          help='The generator to be used in generation of the data.')
train_parser.add_argument('-s', '--source', dest='source_svm', nargs=1, type=str,
                          help='An SVM pickle which will be used to start with.')

eval_parser = subparsers.add_parser(SUPPORTED_COMMANDS[1])
eval_parser.add_argument('svm_path', metavar='svm', nargs=1, type=str,
                         help='Path to the pickle of the svm to use.')
eval_parser.add_argument('-t', '--templatepath', metavar='templatepath', dest='template_paths', nargs='+', type=str,
                         required=True,
                         help='Path to the templates to be used by the SVM.')
eval_parser.add_argument('-d', '--datapath', metavar='datapath', dest='tomogram_paths', nargs='+', type=str,
                         required=True,
                         help='Path to the tomograms to be evaluated.')
eval_parser.add_argument('-o', '--outpath', dest='out_path', nargs='+', type=str, required=True,
                         help='Path to which the results will be saved. Should have the same number of elements as '
                         'datapath.')

args = parser.parse_args('train svm.sk -t template -d tomogram.map'.split())
print(args)

if args.command == SUPPORTED_COMMANDS[0]:
    svm_train(args.svm_path[0], args.template_paths, args.tomogram_paths,
              source_svm=args.source_svm[0] if args.source_svm is not None else None,
              generator=args.generator[0] if args.generator is not None else None)
elif args.command == SUPPORTED_COMMANDS[1]:
    svm_eval(args.svm_path[0], args.template_paths, args.tomogram_paths, args.out_path)
else:
    raise NotImplementedError('Command %s is not implemented.' % args.command)

'''
"""
Read
"""

TRAINING_SET_SIZE = 1

from CommonDataTypes import *
import CandidateSelector
import TemplateGenerator
import TomogramGenerator
import Labeler
import FeaturesExtractor
from Labeler import JUNK_ID


def analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector):
    candidates = candidate_selector.select(tomogram)
    feature_vectors = []
    labels = []

    for candidate in candidates:
        feature_vectors.append(features_extractor.extract_features(tomogram, candidate))
        # this sets each candidate's label
        labels.append(labeler.label(candidate))

    return (candidates, feature_vectors, labels)








#this is tuple of tuples of TiltedTemplates (each group has the same template_id)
templates = TemplateGenerator.generate_tilted_templates()
#save templates to files

candidate_selector = CandidateSelector.CandidateSelector(templates)
features_extractor = FeaturesExtractor.FeaturesExtractor(templates)


#Training

feature_vectors = []
#a label is a template_id, where 0 is junk
labels = []

criteria = (Candidate.fromTuple(1,0,10,10),Candidate.fromTuple(1,2,27,18),Candidate.fromTuple(0,0,10,28))

for i in range(TRAINING_SET_SIZE):
    # configuration for tomogram generation
    #with a set composition
    tomogram = TomogramGenerator.generate_tomogram_with_given_candidates(templates, criteria)

    labeler = Labeler.PositionLabeler(tomogram.composition)

    (candidates, single_iteration_feature_vectors, single_iteration_labels) = analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector)
    feature_vectors.extend(single_iteration_feature_vectors)
    labels.extend(single_iteration_labels)

import numpy as np
X = np.array(feature_vectors)
y = np.array(labels)
from sklearn.svm import SVC
svm = SVC()
print(X)
print(y)
if (len(np.unique(y)) == 1):
    print("SVM training must contain more than one label type (all candidates are the same label)")
    exit()
svm.fit(X, y)

#how to save to disk?
# TODO: Use pickle or sklearn.externals.joblib. See: http://scikit-learn.org/stable/modules/model_persistence.html


#identification

# configuration for tomogram generation
#with a set composition
tomogram = TomogramGenerator.generate_tomogram_with_given_candidates(templates, criteria)

labeler = Labeler.SvmLabeler(svm)

(candidates, feature_vectors, predicted_labels) = analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector)

#test results

ground_truth_labeler = Labeler.PositionLabeler(tomogram.composition)

#junk was identified as non junk
false_positive = 0
#non junk was identified as junk
false_negative = 0
#non junk was identified as a wrong template
false_identification = 0

#non junk was accurately identified
true_identification = 0
#junk was accurately identified
true_rejection = 0

for candidate in enumerate(candidates):
    print(candidate)
    true_label = ground_truth_labeler.label(candidate[1], False)
    predicted_label = labels[candidate[0]]
    if (true_label == JUNK_ID):
        if (predicted_label == JUNK_ID):
            true_rejection += 1
        else:
            false_positive += 1
    else:
        if (predicted_label == true_label):
            true_identification += 1
        elif (predicted_label == JUNK_ID):
            false_negative += 1
        else:
            false_identification += 1


success = true_identification + true_rejection

#print SVM statistics
print("SVM error rate= " + str((len(candidates) - success) / len(candidates)))



#save results

'''
