from colorthief import ColorThief as cf
import matplotlib.pyplot as plt
import sys
imagepath = sys.argv[1]

# instantiate colourthief
color_thief = cf(imagepath)
pltcolours = []
hex = []
# get palette
palette = color_thief.get_palette(color_count=6)
# convert to hex 
for colour in palette:
	hex.append('#%02x%02x%02x' % colour)
	pltcolours.append([colour])
returnstring = ""
for colour in hex:
	returnstring += colour + " "

sys.exit(returnstring)
# plt.imshow(pltcolours)
# plt.show()