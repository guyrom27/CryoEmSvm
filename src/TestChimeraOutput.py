import numpy as np
import VisualUtils

#data1 = np.load(r'../Chimera/tmp_model.npy')
#slider3d(data1 / np.max(data1))
#data2 = np.load(r'../Chimera/tmp_tilted.npy')
#slider3d(data2 / np.max(data2))

data = np.load(r'../Chimera/Templates/1_50.npy')
VisualUtils.slider3d(data / np.max(data))
data = np.load(r'../Chimera/Templates/0_50.npy')
VisualUtils.slider3d(data / np.max(data))
#print(np.min(data1-data2))
#print(np.max(data1-data2))
#show3d(data)

