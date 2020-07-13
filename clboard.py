#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

from alphabet import *

import time
import random
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 990      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

colorWhite = Color(255,255,255)
colorBlack = Color(0,0,0)

# CL centered 
def cl(strip):
    clrow = [4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,11,11,11,11,11,12,12,12,12,12,12,13,13,13,13,13,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17]
    clcol = [13,14,15,16,17,18,25,26,27,28,29,30,12,13,14,15,16,17,18,19,27,28,12,13,14,15,16,17,18,19,20,27,28,11,12,13,14,19,20,27,28,11,12,13,27,28,10,11,12,13,27,28,10,11,12,27,28,10,11,12,27,28,10,11,12,13,27,28,11,12,13,27,28,11,12,13,14,19,20,27,28,11,12,13,14,15,16,17,18,19,20,27,28,33,34,12,13,14,15,16,17,18,19,27,28,29,30,31,32,33,34,13,14,15,16,17,18,25,26,27,28,29,30,31,32,33,34]
    fillBoard(strip,colorBlack)
    for i in range(len(clrow)):
        setColorAt(strip,colorWhite,clcol[i],clrow[i])
    strip.show()

# Scroll Message on given row 
def scrollMessage(strip,message,row):
    for i in range(51 + len(message)*6):  # enough to get all chars across screen
        putStringAt(strip,message,45-i,row-6)
        time.sleep(.05)
        


# Put STRING at loops through the chars and calls putCharAt
def putStringAt(strip,theString,theX,theY):
    for i in range(len(theString)):
        putCharAt(strip,theString[i],theX,theY)
        theX += 6
    strip.show()

#  Put character at uses a, b, c, defined in alphabet.py
def putCharAt(strip,theChar,theX,theY):
    fgColor = Color(128,128,0)
    bgColor = colorBlack
    letters = "abcdefghijklmnopqrstuvwxyz "
    mystring = []
    letterIndex = letters.index(theChar)
    pattern = alphabet[letterIndex]
    for x in range(6):
        for y in range(7):
            if pattern[y][x] == 1:
                setColorAt(strip,fgColor,x+theX,y+theY)
            else:
                setColorAt(strip,bgColor,x+theX,y+theY)
    #strip.show()

# Marquee Border
def marqueeBorder(strip):
    for cycle in range(50):
        for col in range(22):
            setColorAt(strip,colorWhite,col*2,0)
            setColorAt(strip,colorBlack,col*2+1,0)
            setColorAt(strip,colorWhite,col*2+1,21)
            setColorAt(strip,colorBlack,col*2,21)
        for row in range(11):
            setColorAt(strip,colorWhite,0,row*2)
            setColorAt(strip,colorBlack,0,row*2+1)
            setColorAt(strip,colorWhite,44,row*2)
            setColorAt(strip,colorBlack,44,row*2+1)
        strip.show()
        time.sleep(.1)
        for col in range(22):
            setColorAt(strip,colorBlack,col*2,0)
            setColorAt(strip,colorWhite,col*2+1,0)
            setColorAt(strip,colorBlack,col*2+1,21)
            setColorAt(strip,colorWhite,col*2,21)
        for row in range(11):
            setColorAt(strip,colorBlack,0,row*2)
            setColorAt(strip,colorWhite,0,row*2+1)
            setColorAt(strip,colorBlack,44,row*2)
            setColorAt(strip,colorWhite,44,row*2+1)
        strip.show()
        time.sleep(.1)
        

# Make a centered rectangle filled with color
#   upper left corner (x,y), width and height of rec
def makeRec(strip,color,x,y,w,h):
    for row in range(h):
        for col in range(w):
            setColorAt(strip,color,col+y,row+x)
    #strip.show()

# Random Sparkle Fill
def randomSparkle(strip):
    fillBoard(strip,Color(155,155,155))
    for i in range (3000):  # How many random pixels to turn on
        strip.setPixelColor(random.randint(0,990), Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        if i%5 == 0:
            strip.show()

# Cascading Rectangles
def cascadeRecs(strip):
    fillBoard(strip,Color(0,0,0))
    mycolors = []
    for i in range (11):
        mycolors.append(Color(random.randint(0,128),random.randint(0,128),random.randint(0,128)))

    # How many times to cascade the recs
    for x in range(100):
        for i in range (11):
            makeRec(strip,mycolors[i],i,i,45-i*2,22-i*2)
        strip.show()
        time.sleep(0.1)
        mycolors.append(mycolors.pop(0))
        

# Strips for flag
def makeFlag(strip):
    # Fill screen with red
    fillBoard(strip,Color(0,255,0))
 
    # Place white stripes 
    for i in [2,5,8,11,14,17,20]:
        for j in range(45):
            setColorAt(strip,Color(255,255,255),j,i)

    # Fill in blue corner
    for row in range(11):
        for col in range(23):
            setColorAt(strip, Color(0,0,255),col,row)

    # Add stars
    for row in [1,3,5,7,9]:
        for col in [1,5,9,13,17,21]:
            setColorAt(strip, Color(255,255,255),col,row)

    for row in [2,4,6,8]:
        for col in [3,7,11,15,19]:
            setColorAt(strip, Color(255,255,255),col,row)

    # Turn off bottom two rows
    for row in [20,21]:
        for col in range(45):
            setColorAt(strip, Color(0,0,0), col, row)

    strip.show()


# Define function to map (x,y) to a pixel and give it a color
def setColorAt(strip, color, x, y):
    if x >= 0 and x <45 and y >= 0 and y < 22:
        if y%2 != 0:
            offset = x - 44
        else:
            offset = -x
        strip.setPixelColor(989-(y*45)+offset,color)

# Draw both diagonals with given color
def drawDiagonals(strip, color):
    for i in range(22):
        setColorAt(strip,color,i*2,i)
        setColorAt(strip,color,i*2,21-i)
        strip.show()

# Fill board with color
def fillBoard(strip,color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

# wipe a color across board left to right
def wipeLR(strip,color):
    for col in range(45):
        for row in range(22):
            setColorAt(strip,color,col,row)
        strip.show()
        time.sleep(0.05)
        

# wipe a color across down board top to bottom
def wipeTB(strip,color):
    for row in range(22):
        for col in range(45):
            setColorAt(strip,color,col,row)
        strip.show()
        time.sleep(0.05)
        

# Bouncy... make the ball bounce around the board
def bouncy(strip):
    row = 21
    col = 0
    deltaH = 2
    deltaV = -1
    for i in range (200):  #  just how long to bounce the ball
        setColorAt(strip,Color(128,128,0),col,row)
        row += deltaV
        if row < 0:
            row = 0
            deltaV = 2
        if row >= 22:
            row = 21
            deltaV = -1
        col += deltaH
        if col < 0:
            col = 0
            deltaH =2
        if col >= 45:
            col = 44
            deltaH = -1
        setColorAt(strip,Color(0,0,0),col,row)
        strip.show()
        time.sleep(0.025)





        

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=0):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        #time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=1, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=.5, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/9000.0)

def rainbowCycle(strip, wait_ms=2, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=1):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print ('Testing Code....')
            wipeLR(strip,Color(50,50,50))
            scrollMessage(strip,"welcome to the creativity lab",10)
            randomSparkle(strip)
            wipeLR(strip,Color(0,0,255))
            cl(strip)
            marqueeBorder(strip)
            #break

            makeFlag(strip)
            time.sleep(7)
            cascadeRecs(strip)
            time.sleep(1)
            fillBoard(strip,Color(255,0,255))
            wipeLR(strip,Color(0,0,255))
            drawDiagonals(strip,Color(0,0,0))
            wipeTB(strip,Color(128,128,0))
            bouncy(strip)
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            theaterChase(strip, Color(127, 127, 127))  # White theater chase
            theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print ('Rainbow animations.')
            rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
