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
