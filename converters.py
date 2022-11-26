from numba import njit

conversion_matrix = [[1, 0.5], [-1, 0.5]]


@njit
def mum_convert(x: int, y: int):
    return [x - y, x / 2 + y / 2]
