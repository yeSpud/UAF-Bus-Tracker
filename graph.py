import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('./exported/Nenana/Eielson Building/tuesday.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')

    for row in plots:
        x.append(row[0])
        y.append(int(row[1]))

plt.bar(x, y)

plt.show()