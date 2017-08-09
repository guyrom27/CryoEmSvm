import sys

if 'chimera' not in sys.modules:
    print("No chimera in environment! Exiting...")
    exit(0)

# No actual need to import anything
import chimera
from VolumeViewer import open_volume_file
from Matrix import euler_xform
import numpy as np

RESOULTION = 10
ANGLE_RES = 30


def center_strcture(chan):
    com = [sum([c[i] for c in chan.coordSets[0].coords()]) / len(chan.coordSets[0].coords()) for i in range(3)]
    for j in range(len(chan.atoms)):
        p = chan.atoms[j].coord()
        for i in range(3):
            p[i] -= com[i]
        chan.atoms[j].setCoord(p)


def matrix_com(m):
    return [np.dot(np.array(range(m.shape[i])),
                   np.sum(np.sum(m, max((i + 1) % 3, (i + 2) % 3)), min((i + 1) % 3, (i + 2) % 3))) for i in
            range(3)] / sum(sum(sum(m)))


def create_dm(pdbname, outputname):
    # create density map
    chan = chimera.openModels.open(pdbname)[0]
    chimera.runCommand('molmap #0 %s modelId 1' % str(RESOULTION))
    dm = chimera.specifier.evalSpec('#1').models()[0]
    chan.destroy()

    # rotate and save
    translation = [0, 0, 0]
    rot_phi = euler_xform([ANGLE_RES, 0, 0], translation)
    rot_theta = euler_xform([0, ANGLE_RES, 0], translation)
    rot_psi = euler_xform([0, 0, ANGLE_RES], translation)
    for theta in range(0, 181, ANGLE_RES):
        for phi in range(0, 360, ANGLE_RES):
            for psi in range(0, 360, ANGLE_RES):
                dm.openState.localXform(rot_psi)
                angle_str = ''.join(['_' + str(angle) for angle in [phi, theta, psi]])
                np.save(outputname + angle_str, dm.matrix())
            dm.openState.localXform(rot_psi)
            dm.openState.localXform(rot_phi)
        dm.openState.localXform(rot_phi)
        dm.openState.localXform(rot_theta)

    dm.close()

print("The code was compiled")
# pdbname = r'C:\Users\Matan\Dropbox\Study\S-3B\Workshop\Tutotrial\1k4c.pdb'
# outputname = r'C:\Users\Matan\PycharmProjects\Workshop\Chimera\tmp'
# create_dm(pdbname, outputname)
# execfile(r'C:\Users\Matan\PycharmProjects\Workshop\Chimera\create_templates.py')
