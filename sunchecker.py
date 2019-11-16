import ephem
import sys

s = ephem.Sun()
melb = ephem.city('Melbourne')
s.compute(melb)
twilight = -12 * ephem.degree

light = s.alt>twilight
# print("start python\nLight is: " + str(light))
# print("end python\n")
#sys.exit(light)

if light:
	sys.exit("1")
else:
	sys.exit("0")

