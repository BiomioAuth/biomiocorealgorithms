from nearpy.hashes import RandomBinaryProjections, PCABinaryProjections, \
    RandomDiscretizedProjections, PCADiscretizedProjections

RANDOM_BINARY_PROJECTIONS = 'RandomBinaryProjections'
RANDOM_DISCRETIZED_PROJECTIONS = 'RandomDiscretizedProjections'
PCA_BINARY_PROJECTIONS = 'PCABinaryProjections'
PCA_DISCRETIZED_PROJECTIONS = 'PCADiscretizedProjections'

_PROJ_DICT = {
    RANDOM_BINARY_PROJECTIONS: RandomBinaryProjections,
    RANDOM_DISCRETIZED_PROJECTIONS: RandomDiscretizedProjections,
    PCA_BINARY_PROJECTIONS: PCABinaryProjections,
    PCA_DISCRETIZED_PROJECTIONS: PCADiscretizedProjections
}

def get_projection_by_type(proj_type):
    return _PROJ_DICT.get(proj_type, None)
