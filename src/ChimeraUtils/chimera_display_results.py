import chimera
from VolumeViewer import volume_from_grid_data
from VolumeData import Array_Grid_Data
import numpy as np
import sys


def display(matPaths):
    """
    Places list of density maps (supplied as paths to numpy matrices)
    in chimera session.

    :param matPaths: list of paths of numpy matrices
    :return: list of chimera models (one for each matrix)
    """

    # clear previous sessions
    chimera.closeSession()

    models = [];
    for i,matPath in enumerate(matPaths):
        # load numpy matrix
        matrix = np.load(matPath)
        # place density map matrix in chimera session
        v = volume_from_grid_data(Array_Grid_Data(matrix))
        # grab new model
        models.append(chimera.specifier.evalSpec('#' + str(i)).models()[0])
        # name model
        models[-1].name = matPath.split('.')[-2].split('/')[-1]
    return models
    

if __name__ == '__main__':
    # usage example:
    # "C:\Program Files\Chimera 1.11.2\bin\chimera" --debug --script ".\chimera_display_results.py eval.npy rec.npy"
    display(sys.argv[1:])


