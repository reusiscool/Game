import matplotlib.pyplot as plt
from layout import Layout

box_size = 40

lk = Layout('haha', 10, box_size)
lk.generate()

# Pathways
for y, row in enumerate(lk.map_):
    for x, val in enumerate(row):
        if val:
            plt.plot(x, y, marker='o')

# Borders
plt.plot((0, 0), (box_size - 1, 0))
plt.plot((0, box_size - 1), (0, 0))
plt.plot((box_size - 1, 0), (box_size - 1, box_size - 1))
plt.plot((box_size - 1, box_size - 1), (0, box_size - 1))

plt.show()
