import csv
import os

with open(os.path.join('levels', 'player.csv')) as f:
    reader = csv.reader(f)
    stat_line = next(reader)
    w1 = next(reader)
    w2 = next(reader)
    abl = next(reader)
    items = []
    for item in reader:
        items.append(item)

print(stat_line, w1, w2, abl, items)
