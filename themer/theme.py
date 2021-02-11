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

NCMPCPP_MAIN_COLOUR_INDEX = 0

def main(theme=None, image_path=None):
    if theme is None:
        if is_light():
            light_level = "light"
        else:
            light_level = "dark"
        print("It's", light_level, "outside")
        image_path, filename = get_random_image_filename(light_level)
        theme = filename[:-4]

    print("Changing theme to", theme, "...")
    set_background(image_path)
    colour_hexes = get_palette(image_path)
    colour_hexes[NCMPCPP_MAIN_COLOUR_INDEX] = get_contrast_colours(colour_hexes)
    write_configs(colour_hexes)
    print("Reloading termite...")
    subprocess.run("killall -USR1 termite", shell=True)
    print("Done!")
    glavaPID = glava_running()
    relaunch_glava(glavaPID)
    relaunch_polybar()
    exit(0)

def is_light():
    """is_light returns True if the sun is up and False otherwise"""
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

def get_random_image_filename(light_level):
    """Returns the image path and name"""
    filenameCommand = "ls ~/Pictures/" + light_level + " | shuf -n 1" #construct shell command. Finds the folder relevant to light level, then shuffles the ls result
    filename = str(subprocess.check_output(filenameCommand, shell=True))
    # crop name into useful string
    filename = filename[2:]
    filename = filename[:-3]
    image_path = light_level + "/" + str(filename)
    return image_path, filename


def set_background(image_path):
    """Uses feh to set the background to the passed image"""
    backgroundCommand = "feh -q --bg-fill ~/Pictures/" + image_path
    subprocess.run(backgroundCommand, shell=True)

def get_palette(image_path):
    """Constructs a palette of hexes based on the selected image"""
    fullimage_path = "/home/rroche/Pictures/" + image_path
    colourThief = cf(fullimage_path)
    colour_hexes = []
    palette = colourThief.get_palette(color_count=COLOUR_COUNT)
    for colour in palette:
	    colour_hexes.append('#%02x%02x%02x' % colour) # format for hex
    return colour_hexes

def write_configs(colour_hexes):
    """sed the selected colours into the relevant config files"""
    # construct sed commands

    hexValue = colour_hexes[2].lstrip('#')
    rgbValue = list(int(hexValue[i:i+2], 16) for i in (0,2, 4)) # convert to rgb for analysis
    brightness =get_brightness_from_rgb(rgbValue)
    #print("Brightness is " + str(brightness))
    if brightness > 128:
        textcolour = "#333333"
    else:
        textcolour = "#FFFFFF"

  
    sedGlava = 'sed -i "s/#define COLOR.*/#define COLOR mix(' + colour_hexes[1] + ', ' + colour_hexes[4] + ', clamp(d\/80, 0, 1))/g" ' + '$HOME/.config/glava/radial.glsl'
    sedPolybar = 'sed -i "s/under = .*/under = ' + colour_hexes[5] + '/g" ' + '$HOME/.config/polybar/colors.ini'
    sedPolybarBackground = 'sed -i "s/mf = .*/mf = ' + colour_hexes[2] + '/g" ' + '$HOME/.config/polybar/colors.ini'
    sedPolybarForeground = 'sed -i "s/light-mode-font = .*/light-mode-font = ' + textcolour + '/g" ' + '$HOME/.config/polybar/colors.ini'
    sedNcmpcppMain = 'sed -i "s/' + NCMPCPP_MAIN + ' = .*/' + NCMPCPP_MAIN + ' = ' + colour_hexes[NCMPCPP_MAIN_COLOUR_INDEX] + '/g" ' + "$HOME/.config/termite/config"
    sedNcmpcppHeadings = 'sed -i "s/' + NCMPCPP_HEADINGS + ' = .*/' + NCMPCPP_HEADINGS + ' = ' + colour_hexes[2] + '/g" ' + "$HOME/.config/termite/config"
    sedPolybari3 = 'sed -i "s/i3colour = .*/i3colour = ' + colour_hexes[3] + '/g" ' + '$HOME/.config/polybar/colors.ini'

    commands = [sedGlava, sedPolybar, sedNcmpcppHeadings, sedNcmpcppMain, sedPolybari3, sedPolybarBackground, sedPolybarForeground]

    for command in commands:
        subprocess.run(command, shell=True)
   

def glava_running():
    """Return pid if glava is running, 0 otherwise"""
    try:
        pid = str(subprocess.check_output("pgrep glava", shell=True))
        pid = pid[2:]
        pid = pid[:-3]
        pid = int(pid)
        return pid
    except:
        return 0

def relaunch_glava(glavaPID):
    """Relaunch glava so the configs are reloaded"""
    if glavaPID:
        print("Relaunching glava...")
        killString = "kill -9 " + str(glavaPID)
        subprocess.run(killString, shell=True)
        subprocess.run("exec glava &", shell=True)
        print("Done!")
    else:
        pass

def relaunch_polybar():
    """Relaunch polybar so the configs are reloaded"""
    print("Relaunching polybar...")
    subprocess.run("pkill polybar", shell=True)
    subprocess.run("$HOME/.config/polybar/launch.sh 2>/dev/null", shell=True)
    print("Done!")

def get_contrast_colours(colour_hexes):
    """Analyse text colours. If they're too dark for good viewing, brighten them"""
    hexValue = colour_hexes[NCMPCPP_MAIN_COLOUR_INDEX].lstrip('#')
    rgbValue = list(int(hexValue[i:i+2], 16) for i in (0,2, 4)) # convert to rgb for analysis
    brightness =get_brightness_from_rgb(rgbValue)
    difference = 128 - brightness
    
    if difference > 0:
        print("Colour 0 is too dark for terminal text. Brightening...")
        rgbBrightened = []
        for colour in colour_hexes:
            colourStripped = colour.lstrip('#')
            rgb = list(int(colourStripped[i:i+2], 16) for i in (0,2, 4))
            altBrightness = get_brightness_from_rgb(rgb)
            difference = 128-altBrightness
            if difference <= 0:
                print("Done! Using alternate palette hex:", colour)
                return colour
        for value in rgbValue:
            rgbBrightened.append(round(value * 128/brightness))
        newBrightness = get_brightness_from_rgb(rgbBrightened)
        rgbBrightened = tuple(rgbBrightened)
        hexBrightened = '#%02x%02x%02x' % rgbBrightened
        print("Done! New hex: ", hexBrightened)
        return hexBrightened
    else:
        return colour_hexes[NCMPCPP_MAIN_COLOUR_INDEX]

def get_brightness_from_rgb(rgbValues):
    """Calculates colour brightness based on rgb values"""
    brightness = (rgbValues[0] * 299 + rgbValues[1] * 587 + rgbValues[2] * 114) / 1000
    return brightness

def list_themes():
    print("\033[95mLight themes:\033[0m")
    filenameCommand = "ls ~/Pictures/light"
    filenames = subprocess.check_output(filenameCommand, shell=True).decode('ascii').split('\n')
    print_columns(filenames)

    print("\n\033[95mDark themes:\033[0m")
    filenameCommand = "ls ~/Pictures/dark"
    filenames = subprocess.check_output(filenameCommand, shell=True).decode('ascii').split('\n')
    print_columns(filenames)

def print_columns(filenames):
    if len(filenames) % 2 != 0:
        filenames.append("")

    for a, b, c in zip(filenames[::3], filenames[1::3], filenames[2::3]):
        print("{:<30}{:<30}{:<}".format(a[:-4], b[:-4], c[:-4])) # [:-4] strips file extensions for a cleaner look

def select_theme(theme_name):
    filenameCommand = "ls ~/Pictures/light"
    filenames = subprocess.check_output(filenameCommand, shell=True).decode('ascii').split('\n')
    for filename in filenames:
        if filename[:-4] == theme_name:
            image_path = "light/" + filename
            main(theme_name, image_path)
    
    filenameCommand = "ls ~/Pictures/dark"
    filenames = subprocess.check_output(filenameCommand, shell=True).decode('ascii').split('\n')
    for filename in filenames:
        if filename[:-4] == theme_name:
            image_path = "dark/" + filename
            main(theme_name, image_path)
    print("Error: Could not find theme: " + theme_name)


if len(sys.argv) > 1:
    if sys.argv[1] == "-l" or sys.argv[1] == "--list":
        list_themes()
    elif sys.argv[1] == "-t" or sys.argv[1] == "--theme":
        try:
            select_theme(sys.argv[2])
        except IndexError:
            print("Please specify a theme name with this option.")
    else:
        print("Unknown argument " + sys.argv[1] + ".")
else:
    main()


