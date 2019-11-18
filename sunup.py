import sys
from skyfield import api
from skyfield import almanac
from datetime import timedelta
from skyfield.api import utc
import datetime

ts = api.load.timescale()
e = api.load('de421.bsp')

melbourne = api.Topos('37.951910 S', '145.152080 E')

now = datetime.datetime.utcnow()
now = now.replace(tzinfo=utc)

t0 = ts.utc(now)
t1 = ts.utc(now + timedelta(hours=24))

t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, melbourne))


if (y[0]):
	sys.exit("0")
else:
	sys.exit("1")