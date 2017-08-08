SUPPORTED_GENERATORS = ('SOLID',)

def svm_train(svm_path, template_paths, tomogram_paths, source_svm=None, generator=None, generate_templates=False):
    """
    Train an SVM using the templates and tomograms specified. If generator is not None then the tomograms will be
    generated instead. If generated_templates is True the templates will also be generated
    The resulting will be saved in svm_path. The SVM can start from an existing one given in source_svm.
    :param svm_path: Path in which the SVM will be saved.
    :param template_paths: List of paths to the templates.
    :param tomogram_paths: List of paths to the tomograms.
    :param source_svm: Path to a source SVM to start with.
    :param generator: The generator to use. Choose from SUPPORTED_GENERATORS.
    :param generate_templates: Bool indicating whether to generate the templates too.
    """
    pass
