import subprocess
import sys
from skyfield import api
from skyfield import almanac
from datetime import timedelta
from skyfield.api import utc, Loader
import datetime


def isLight():
    # load in data directory to avoid redownloading
    loader = Loader('~/skyfield_data')
    ts = loader.timescale()
    e = loader('de421.bsp')

    # set current location (melbourne does not appear in the default list)
    melbourne = api.Topos('37.951910 S', '145.152080 E')
    # get current time in UTC format
    now = datetime.datetime.utcnow()
    now = now.replace(tzinfo=utc)
    # set the interval for now and 24 hours from now
    t0 = ts.utc(now)
    t1 = ts.utc(now + timedelta(hours=24))

    # find the times and types of event (sunrise/sunset)
    t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, melbourne))

    #y[0] = True for sunrise (which means it is currently dark)

    light = not y[0]

    return light

if 