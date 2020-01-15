import subprocess
import sys
from skyfield import api
from skyfield import almanac
from datetime import timedelta
from skyfield.api import utc, Loader
import datetime
from colorthief import ColorThief as cf

COLOUR_COUNT = 6
NCMPCPP_MAIN = "color3"
NCMPCPP_HEADINGS = "color11"
NCMPCPP_ELAPSED = "color21"

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

def getImageFilename(lightLevel):
    filenameCommand = "ls ~/Pictures/" + lightLevel + " | shuf -n 1"
    filename = str(subprocess.check_output(filenameCommand, shell=True))
    filename = filename[2:]
    filename = filename[:-3]
    imagePath = lightLevel + "/" + str(filename)
    return imagePath, filename


def setBackground(imagePath):
    backgroundCommand = "feh -q --bg-fill ~/Pictures/" + imagePath
    subprocess.run(backgroundCommand, shell=True)

def getPalette(imagePath):
    fullImagePath = "/home/rroche/Pictures/" + imagePath
    colourThief = cf(fullImagePath)
    colourHexes = []
    palette = colourThief.get_palette(color_count=COLOUR_COUNT)
    for colour in palette:
	    colourHexes.append('#%02x%02x%02x' % colour)
    return colourHexes

def writeConfigs(colourHexes):
    sedGlava = 'sed -i "s/#define COLOR.*/#define COLOR mix(' + colourHexes[4] + ', ' + colourHexes[1] + ', clamp(d\/80, 0, 1))/g" ' + '$HOME/.config/glava/radial.glsl'
    sedPolybar = 'sed -i "s/under = .*/under = ' + colourHexes[5] + '/g" ' + '$HOME/.config/polybar/colors.ini'
    sedNcmpcppMain = 'sed -i "s/' + NCMPCPP_MAIN + ' = .*/' + NCMPCPP_MAIN + ' = ' + colourHexes[5] + '/g" ' + "$HOME/.config/termite/config"
    sedNcmpcppHeadings = 'sed -i "s/' + NCMPCPP_HEADINGS + ' = .*/' + NCMPCPP_HEADINGS + ' = ' + colourHexes[2] + '/g" ' + "$HOME/.config/termite/config"
    
    subprocess.run(sedGlava, shell=True)
    subprocess.run(sedPolybar, shell=True)
    subprocess.run(sedNcmpcppMain, shell=True)
    subprocess.run(sedNcmpcppHeadings, shell=True)

def glavaRunning():
    try:
        pid = str(subprocess.check_output("pgrep glava", shell=True))
        pid = pid[2:]
        pid = pid[:-3]
        pid = int(pid)
        return pid
    except:
        return 0

def relaunchGlava(glavaPID):
    if glavaPID:
        print("Relaunching glava...")
        killString = "kill -9 " + str(glavaPID)
        subprocess.run(killString, shell=True)
        subprocess.run("exec glava &", shell=True)
        print("Done!")
    else:
        pass

def relaunchPolybar():
    print("Relaunching polybar...")
    subprocess.run("pkill polybar", shell=True)
    subprocess.run("$HOME/.config/polybar/launch.sh 2>/dev/null", shell=True)
    print("Done!")



def main():
    if isLight():
        lightLevel = "light"
    else:
        lightLevel = "dark"
    print("It's", lightLevel, "outside")
    imagePath, filename = getImageFilename(lightLevel)
    theme = filename[:-4]
    print("Changing theme to", theme, "...")
    setBackground(imagePath)
    colourHexes = getPalette(imagePath)
    writeConfigs(colourHexes)
    print("Reloading termite...")
    subprocess.run("killall -USR1 termite", shell=True)
    print("Done!")
    glavaPID = glavaRunning()
    relaunchGlava(glavaPID)
    relaunchPolybar()



main()

    
