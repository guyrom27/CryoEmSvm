import sys
import argparse
from TemplateGenerator import TemplateGenerator
from TomogramGenerator import TomogramGenerator
from TemplateFactory import TemplateFactory
from TomogramFactory import TomogramFactory
from SvmTrain import svm_train
from SvmEval import svm_eval

# TODO: Add generate subcommand
SUPPORTED_COMMANDS = ('generate', 'train', 'eval')
GENERETABLES = ('templates', 'tomograms')

# Generate wrapper functions
def _generate_templates(generator, out_path):
    templates = TemplateFactory(generator).build()
    save_generator = TemplateFactory(TemplateGenerator.LOAD).set_paths([out_path]).set_save(True).build()
    for template, save in zip(templates, save_generator):
        save(template)

def _generate_tomograms(generator, template_paths, out_path):
    templates = TemplateFactory(TemplateGenerator.LOAD).set_paths(template_paths).build()
    tomograms = TomogramFactory(generator).set_templates(templates).build()
    save_generator = TomogramFactory(TemplateGenerator.LOAD).set_paths([out_path]).set_save(True).build()
    for tomogram, save in zip(tomograms, save_generator):
        save(tomogram)

# Train wrapper function
def _train(svm_path, template_paths, tomogram_paths, tomogram_generator):
    # Load the templates and the tomograms
    templates_generator = TemplateFactory(TemplateGenerator.LOAD).set_paths(template_paths).build()
    tomograms_generator = TomogramFactory(
        tomogram_generator if tomogram_generator else TomogramGenerator.LOAD).set_paths(tomogram_paths).build()

    # Create and train the SVM
    svm = svm_train(templates_generator, tomograms_generator)

    # Save the SVM
    # TODO: Make some better way to save the svm
    import pickle
    with open(svm_path, 'wb') as file:
        pickle.dump(svm, file)


# Eval wrapper function
def _eval(svm_path, tomogram_paths, out_path):
    # Load the SVM
    # TODO: Make some better way to load the svm
    import pickle
    with open(svm_path, 'rb') as file:
        svm_and_templates = pickle.load(file)

    # Load the tomograms
    tomograms = TomogramFactory(TomogramGenerator.LOAD).set_paths(tomogram_paths).build()

    # Evaluate the tomograms
    eval_result = svm_eval(svm_and_templates, tomograms)

    # Do something with the result
    # TODO: Do something meaningful with the result
    with open(out_path, 'wb') as file:
        pickle.dump(eval_result, file)


def main(argv):
    parser = argparse.ArgumentParser(description='Train or evaluate an SVM to classify electron density maps.')
    subparsers = parser.add_subparsers(dest='command', help='Command to initiate.')

    # TODO: fine-tune the generate commands to support all generation methods. That's including accepting required parameters
    # Define generate sub-command
    generator_parser = subparsers.add_parser(SUPPORTED_COMMANDS[0])
    generator_subparser = generator_parser.add_subparsers(dest='generetable', help='Type of object to generate.')

    # Define generate templates sub-sub-command
    template_parser = generator_subparser.add_parser(GENERETABLES[0])
    template_parser.add_argument('generator', choices=TemplateGenerator.keys(), nargs=1,
                                 help='The kind of generator to use when creating the templates')
    template_parser.add_argument('out_path', nargs=1, help='Path to save in the generated template')

    # Define generate tomogram sub-sub-command
    tomogram_parser = generator_subparser.add_parser(GENERETABLES[1])
    tomogram_parser.add_argument('generator', choices=TomogramGenerator.keys(), nargs=1,
                                 help='The kind of generator to use when creating the tomograms')
    tomogram_parser.add_argument('template_paths', help='Path to the templates to be used in the generation')
    tomogram_parser.add_argument('out_path', nargs=1, help='Path to save in the generated tomograms')

    # Define train sub-command
    train_parser = subparsers.add_parser(SUPPORTED_COMMANDS[1])
    train_parser.add_argument('svm_path', metavar='svm', nargs=1, type=str,
                              help='Path to save in the created svm.')
    train_parser.add_argument('-t', '--templatepath', metavar='templatepath', dest='template_paths', nargs='+',
                              type=str,
                              required=True,
                              help='Paths to the templates to be trained with.')
    train_parser.add_argument('-d', '--datapath', metavar='datapath', dest='tomogram_paths', nargs='+', type=str,
                              help='Paths to the tomograms to be trained on. If -g is supplied then datapath will be '
                                   'ignored.')
    train_parser.add_argument('-g', '--generator', choices=TomogramGenerator.keys(), dest='tomogram_generator', nargs=1,
                              type=str,
                              help='The generator to be used in generation of the tomograms. Default is LOAD. If '
                                   'datapath is also supplied it will be ignored.')

    # Define eval sub-command
    eval_parser = subparsers.add_parser(SUPPORTED_COMMANDS[2])
    eval_parser.add_argument('svm_path', metavar='svm', nargs=1, type=str,
                             help='Path to the pickle of the svm to use. (As returned by the train subcommand)')
    eval_parser.add_argument('-d', '--datapath', metavar='datapath', dest='tomogram_paths', nargs='+', type=str,
                             required=True,
                             help='Path to the tomograms to be evaluated.')
    eval_parser.add_argument('-o', '--outpath', dest='out_path', nargs=1, type=str, required=True,
                             help='Path to which the results will be saved.')


    # Parse the arguments
    args = parser.parse_args(argv)

    # Run the appropriate command
    if args.command == SUPPORTED_COMMANDS[0]:
        if args.generetable == GENERETABLES[0]:
            _generate_templates(args.generator, args.out_path)
        elif args.generetable == GENERETABLES[1]:
            _generate_tomograms(args.generator, args.template_paths, args.out_path)
    elif args.command == SUPPORTED_COMMANDS[1]:
        _train(args.svm_path[0], args.template_paths, args.tomogram_paths, args.tomogram_generator)
    elif args.command == SUPPORTED_COMMANDS[2]:
        _eval(args.svm_path[0], args.tomogram_paths, args.out_path)
    else:
        raise NotImplementedError('Command %s is not implemented.' % args.command)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # TODO: Add simple test (e.g. The original main test case)
        pass
    else:
        main(None)
