from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy
from math import dist
import matplotlib.pyplot as plt
from level import Level

lk = Level('haha', 10, 20)

print(lk.generate())

# points = numpy.array([[0, 0], [0, 1.1], [1, 0], [1, 1], [2, 1], [0, -2], [1, -1], [-1, 0], [0, 3]])
# tri = Delaunay(points)
#
# plt.triplot(points[:, 0], points[:, 1], tri.simplices)
# plt.plot(points[:, 0], points[:, 1], 'o')
# plt.show()
#
# mtrx = numpy.array([numpy.zeros(tri.npoints) for _ in range(tri.npoints)])
#
# for con in tri.simplices:
#     a, b, c = con
#     mtrx[a, b] = mtrx[b, a] = dist(points[a], points[b])
#     mtrx[c, b] = mtrx[b, c] = dist(points[c], points[b])
#     mtrx[a, c] = mtrx[c, a] = dist(points[a], points[c])
#
# min_tri = minimum_spanning_tree(mtrx).toarray()
# print(min_tri)
#
# for i, row in enumerate(min_tri):
#     for j, val in enumerate(row):
#         if val:
#             x1, y1 = points[i]
#             x2, y2 = points[j]
#             plt.plot([x1, x2], [y1, y2])
#
# plt.plot(points[:, 0], points[:, 1], 'o')
# plt.show()
