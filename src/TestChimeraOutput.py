# import numpy as np
# import matplotlib.pyplot as plt
#
# m = np.load(r'../Chimera/tmp.npy')
# for i in range(0, m.shape[0], 10):
#     fig, ax = plt.subplots()
#     ax.imshow(m[i])
#
# com = [np.dot(np.array(range(m.shape[i])),np.sum(np.sum(m,max((i+1)%3,(i+2)%3)),min((i+1)%3,(i+2)%3))) for i in range(3)] / sum(sum(sum(m)))
#
# #plt.show()


import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def show3d(dm):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    d = int(dm.shape[2]**0.5)+1
    fig, axarr = plt.subplots(d,d)
    for z in range(dm.shape[2]):
        zdm = np.copy(dm[:,:,z])
        zdm[0,0] = 1
        axarr[z//d, z%d].imshow(zdm)
    plt.show()

def slider3d(dm):
    ax = plt.subplot()
    plt.subplots_adjust(left=0.25, bottom=0.25)

    zdm = np.copy(dm[:, :, 0])
    zdm[0, 0] = 1
    l = plt.imshow(zdm)

    axframe = plt.axes([0.25, 0.1, 0.65, 0.03])
    sframe = Slider(axframe, 'Frame', 0, dm.shape[0]-1, valinit=0)

    def update(val):
        zdm = np.copy(dm[:, :, int(np.around(sframe.val))])
        zdm[0, 0] = 1
        l.set_data(zdm)

    sframe.on_changed(update)
    plt.show()

#data1 = np.load(r'../Chimera/tmp_model.npy')
#slider3d(data1 / np.max(data1))
#data2 = np.load(r'../Chimera/tmp_tilted.npy')
#slider3d(data2 / np.max(data2))

data = np.load(r'../Chimera/Templates/0_100.npy')
slider3d(data / np.max(data))
print(data.shape)
#print(np.min(data1-data2))
#print(np.max(data1-data2))
#show3d(data)

