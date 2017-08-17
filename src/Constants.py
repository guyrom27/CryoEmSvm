from math import ceil

DISTANCE_THRESHOLD = 2
JUNK_ID = -1

TOMOGRAM_DIMENSION = 120
TOMOGRAM_DIMENSIONS_2D = (TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION,1)
TOMOGRAM_DIMENSIONS_3D = (TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION,TOMOGRAM_DIMENSION)

TEMPLATE_DIMENSION = 25
TEMPLATE_DIMENSIONS_2D = (TEMPLATE_DIMENSION,TEMPLATE_DIMENSION,1)

DEFAULT_COMPOSITION_TUPLES_2D = ((1, 0, 52, 32), (1, 2, 37, 28), (0, 0, 70, 23))
DEFAULT_COMPOSITION_TUPLES_3D = ((1, 0, 52, 32,35), (1, 2, 37, 28,45), (0, 0, 70, 23,45), (0, 9, 70, 23,72))

NEIGHBORHOOD_HALF_SIDE_SIZE = 5
NEIGHBORHOOD_HALF_SIDE_2D = (NEIGHBORHOOD_HALF_SIDE_SIZE, NEIGHBORHOOD_HALF_SIDE_SIZE, 0)
NEIGHBORHOOD_HALF_SIDE_3D = (NEIGHBORHOOD_HALF_SIDE_SIZE, NEIGHBORHOOD_HALF_SIDE_SIZE, NEIGHBORHOOD_HALF_SIDE_SIZE)