import chimera
from chimera import runCommand
from VolumeViewer import open_volume_file
from Matrix import euler_xform
from chimera import specifier
import numpy as np

def create_dm(pdbname, outputname):
	chan = chimera.openModels.open(pdbname)[0]
	# center structure
	com = [sum([c[i] for c in chan.coordSets[0].coords()]) / len(chan.coordSets[0].coords()) for i in range(3)]
	for j in range(len(chan.atoms)):
		p = chan.atoms[j].coord()
		for i in range(3):
			p[i] -= com[i]
		chan.atoms[j].setCoord(p)

	# create density map
	runCommand('molmap #0 5 modelId 1')
	dm = specifier.evalSpec('#1').models()[0]
	chan.destroy()

	# rotate
	euler_angles = [0,0,0]
	translation = [0,0,0]
	xf = euler_xform(euler_angles, translation)
	dm.openState.localXform(xf)

	np.save(outputname,dm.matrix())
	dm.close()


pdbname = r'C:\Users\Matan\Dropbox\Study\S-3B\Workshop\Tutotrial\1k4c.pdb'
outputname = r'C:\Users\Matan\PycharmProjects\Workshop\Chimera\tmp'
create_dm(pdbname,outputname)
#execfile(r'C:\Users\Matan\PycharmProjects\Workshop\Chimera\create_templates.py')