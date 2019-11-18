"""Deprecated in favour of sunup.py for extra accuracy"""

import ephem
import sys

s = ephem.Sun()
melb = ephem.city('Melbourne')
s.compute(melb)
twilight = -12 * ephem.degree

light = s.alt>twilight


if light:
	sys.exit("1")
else:
	sys.exit("0")

