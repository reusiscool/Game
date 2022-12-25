import csv
import os
import numpy


with open(os.path.join('levels', '1layout.csv')) as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
