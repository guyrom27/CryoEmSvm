# Detection and identification of macromolecular complexes in cryo-electron tomograms using support vector machines
## introduction
Reproduction challenge for the paper [Detection and identification of macromolecular complexes in cryo-electron tomograms using support vector machines](https://ieeexplore.ieee.org/document/6235823).

The paper deals with 3D electron microscopy scans (tomograms) of biological structures (e.g. proteins), and detecting the components using a library of 'puzzle pieces'- biological macromolecules (templates), in order to determined the arrangement and composition of the structure under investigation.
The process is based on finding points in the tomogram that have high correlation with library templates and using a Support Vector Machine (SVM) to choose the correct templates. 

The following demonstrates a 2D flow for generated tomograms from geometric shapes as templates

![candidate selection](https://github.com/guyrom27/CryoEmSvm/blob/master/figures_and_metrics/SlideshowFigures/CryoEMCorrelation.png)

Each such candidate such is translated to a vector of correlations with all the library templates and an SVM performs multi-class classification where each template in the library is a class. Post processing is performed to improve the location of the site, given the chosen template, and choose the optimal orientation of the template.

The SVM is trained using a generated data set, with added noise, and the training, prediction and evaluation flow are describes below

![Flow](https://github.com/guyrom27/CryoEmSvm/blob/master/figures_and_metrics/SlideshowFigures/CryoEMFlow.png)
## Results
Sample results in synthetic 2D cases are presented below (w. noise and w/o noise) 

![without noise](https://github.com/guyrom27/CryoEmSvm/blob/master/figures_and_metrics/2D/no_noise/truth%20vs%20reconstructed.png)

![with noise](https://github.com/guyrom27/CryoEmSvm/blob/master/figures_and_metrics/2D/noise/truth%20vs%20reconstructed.png)

