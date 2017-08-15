import sys
import argparse
from TemplateFactory import Generator
from SvmTrain import svm_train
from SvmEval import svm_eval

# TODO: Add generate subcommand
SUPPORTED_COMMANDS = ('train', 'eval')  # , 'generate_templates', 'generate_tomograms')


def main(argv):
    parser = argparse.ArgumentParser(description='Train or evaluate an SVM to classify electron density maps.')
    subparsers = parser.add_subparsers(dest='command', help='Command to initiate.')

    train_parser = subparsers.add_parser(SUPPORTED_COMMANDS[0])
    train_parser.add_argument('svm_path', metavar='svm', nargs=1, type=str,
                              help='Path to save in the created svm.')
    train_parser.add_argument('-t', '--templatepath', metavar='templatepath', dest='template_paths', nargs='+',
                              type=str,
                              required=True,
                              help='Paths to the templates to be trained with.')
    train_parser.add_argument('-d', '--datapath', metavar='datapath', dest='tomogram_paths', nargs='+', type=str,
                              required=True,
                              help='Paths to the tomograms to be trained on. If used with -g only the first path will be '
                                   'used and it will be used to save the generated tomograms into.')
    train_parser.add_argument('-g', '--generator', choices=Generator.keys(), dest='template_generator', nargs=1,
                              type=str,
                              help='The generator to be used in generation of the templates. Default is LOAD.')
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

    # generator_parser = subparsers.add_parser(SUPPORTED_COMMANDS[2])
    # generator_parser.add_argument('generator', choices=SUPPORTED_GENERATORS, nargs=1, type=str,
    #                               help='The generator to use.')
    # generator_parser.add_argument()

    # Parse the arguments
    args = parser.parse_args(argv)

    if args.command == SUPPORTED_COMMANDS[0]:
        svm_train(args.svm_path[0], args.template_paths, args.tomogram_paths,
                  source_svm=args.source_svm[0] if args.source_svm is not None else None,
                  template_generator=args.template_generator[0] if args.template_generator is not None else None,
                  generate_tomograms=True)
        pass
    elif args.command == SUPPORTED_COMMANDS[1]:
        svm_eval(args.svm_path[0], args.template_paths, args.tomogram_paths, args.out_path)
        pass
    else:
        raise NotImplementedError('Command %s is not implemented.' % args.command)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        from TemplateGenerator import Generator
        from TemplateFactory import TemplateFactory
        from TomogramFactory import TomogramFactory
        from CandidateSelector import CandidateSelector
        from FeaturesExtractor import FeaturesExtractor
        from TiltFinder import TiltFinder
        from SvmEval import analyze_tomogram
        import Labeler

        print('Starting test...')

        main('train svm.pkl -t tmpl1.pkl tmpl2.pkl -d tmgrm.pkl -g SOLID'.split())

        main('eval svm.pkl -t tmpl1.pkl tmpl2.pkl -d tmgrm.pkl -o out.pkl'.split())

        # Load the templates and the tomogram and reevaluate the ground truth
        gf_templates = TemplateFactory(Generator.LOAD)
        gf_templates.set_paths(['tmpl1.pkl', 'tmpl2.pkl'])
        templates = list(gf_templates.build())

        gf_tomograms = TomogramFactory(None)
        gf_tomograms.set_paths(['tmgrm.pkl'])
        tomogram = list(gf_tomograms.build())[0]

        candidate_selector = CandidateSelector(templates)
        features_extractor = FeaturesExtractor(templates)
        tilt_finder = TiltFinder(templates)

        labeler = Labeler.PositionLabeler(tomogram.composition)

        (candidates, feature_vectors, labels) = \
            analyze_tomogram(tomogram, labeler, features_extractor, candidate_selector, tilt_finder)

        # Load the svm evaluation result
        gf_svm_tomograms = TomogramFactory(None)
        gf_svm_tomograms.set_paths(['out.pkl'])
        svm_tomogram = list(gf_svm_tomograms.build())[0]


        # Get the labels
        suggested_labels = [candidate.label for candidate in svm_tomogram.composition]

        JUNK_ID = -1
        true_rejection = 0
        false_positive = 0
        true_identification = 0
        false_negative = 0
        false_identification = 0

        for true_label, predicted_label in zip(labels, suggested_labels):
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

        # print SVM statistics
        print("SVM error rate = " + str((len(candidates) - success) / len(candidates)))

        print("Test finished!")
    else:
        main(None)
