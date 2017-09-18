The timings are save in the following way:
    Each file is a two dimensional matrix of the time as a function of the size of the templates and the tomograms.
    The first dimension of the array is the template and the second is the tomogram.
The name of the file:
    Starts with 'time_tomograms'
    Dimention '2d' or '3d'
    Then information about the sizes used:
        15 - Start template size
        10 - template jump size
        35 - template max size
        100 - Start tomogram size
        10 - tomogram jump size
        140 - tomogram max size
        in other words, all the combinations of template size in [15, 25, 35] and tomogram in [100, 110, 120, 130, 140]

    easy way to translate index to size: start + i * step

Other information:
    In 2D the criteria used is [1, 1, 1]
    In 3D the criteria used is [2, 2, 2] and template type is ALL_3D