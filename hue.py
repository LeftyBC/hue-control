#!/usr/bin/env python

# to install phue:
#    sudo easy_install phue

# usage:
#    ./hue.py [light_num] [red_value] [green_value] [blue_value]

# example:
# to set light 3 to submarine-mode red:
#    ./hue.py 3 255 0 0

# to set light 3 to completely powered off:
#    ./hue.py 3 0 0 0

# to set light 3 to a nice yellow:
#    ./hue.py 3 128 255 0

# to set light 3 to brightest white:
#    ./hue.py 3 255 255 255

# 255 is the max for any one color.

import sys

import colorsys

from phue import Bridge
from math import floor

max_brightness = 255
max_saturation = 255
max_hue = 65535

b = Bridge('10.196.186.16')

b.connect()

l = int(sys.argv[1])

# ensure a bad light number doesn't make it through
l = 1 if l < 1 or l is None else l

raw_red = float(sys.argv[2])
raw_green = float(sys.argv[3])
raw_blue = float(sys.argv[4])

print "raw_red: %f, raw_green: %f, raw_blue: %f" % (raw_red,raw_green,raw_blue)

if raw_red < 1 and raw_green < 1 and raw_blue < 1:
    # special case:
    # if the user has entered 0 for each color
    # turn the light completely off
    print "Turning light %d off" % l
    b.set_light(l,'on',False)
    pass

else:
    # if the colors are non-zero,
    # convert the color to HSV and set the specified light
    # to the specified color

    raw_red = 255.0 if raw_red > 255.0 else raw_red
    raw_green = 255.0 if raw_green > 255.0 else raw_green
    raw_blue = 255.0 if raw_blue > 255.0 else raw_blue

    red = 1.0 / (255.0 / raw_red) if raw_red > 0.0 else 0.0
    green = 1.0 / (255.0 / raw_green) if raw_green > 0 else 0.0
    blue = 1.0/ (255.0 / raw_blue) if raw_blue > 0 else 0.0

    result = colorsys.rgb_to_hsv(red,green,blue)

    h = floor(result[0] * max_hue) #int(h) #* max_hue
    s = floor(result[1] * max_saturation) #int(s) #* max_saturation
    v = floor(result[2] * max_brightness) #int(v) #* max_brightness

    print ("light %d to h%f s%f v%f" % (l,h,s,v))
    b.set_light(l,'on',True)
    b.set_light(l,'bri',int(v))
    b.set_light(l,'hue',int(h))
    b.set_light(l,'sat',int(s))
