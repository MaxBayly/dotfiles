import matplotlib.pyplot as plt
import sys

colours = []
pltcolours = []
for line in sys.stdin:
	lines = line.split(" ")
	for sub in lines:
		if sub == "\n":
			continue
		colours.append(tuple(map(int, sub.strip("\n").split(","))))
		pltcolours.append([tuple(map(int, sub.strip("\n").split(",")))])

plt.imshow(pltcolours)
plt.show()