from numba import njit

conversion_matrix = [[1, 0.5],
                     [-1, 0.5]]
back_matrix = [[0.5, -0.5],
               [1, 1]]


@njit
def mum_convert(x: float, y: float):
    return x - y, x / 2 + y / 2


@njit
def back_convert(x: float, y: float):
    return x / 2 + y, -x / 2 + y
