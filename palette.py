#import colorgram
import matplotlib.pyplot as plt
import sys

colours = []
pltcolours = []
for line in sys.stdin:
	if line == "\n":
		pass
	else:
		colours.append(tuple(map(int, line.strip("\n").split(","))))
		pltcolours.append([tuple(map(int, line.strip("\n").split(",")))])
		

plt.imshow(pltcolours)
plt.show()