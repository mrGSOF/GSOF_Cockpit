#!/usr/bin/python
"""
* Demo_AltGauge.py
* Created on: 20 Jan 2025
* Author:     Guy Soffer
* Copyright (C) 2025 Guy Soffer
"""

from Data import Data
from GSOF_Cockpit.Aerospace import AltMeter_Analog as ALT

from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

# Initialise screen.
BG_color = COLOR.DARK
screen_size = (300, 300)
pos = (0, 0)
init()
screen = getScreen(screen_size)
fillScreen(screen, COLOR.WHITE)

# Initialise Dials.
path = "../"
background = Text(screen=screen, pos=pos, size=screen_size, color=BG_color, name="")
alt = ALT.AltMeter(
    screen=screen,
    pos=pos,
    size=screen_size,
    digitsColor=COLOR.WHITE,
    bodyImage=imageLoad("%s/skin/Alt_Meter200.png" % path),
    handAImage=imageLoad("%s/skin/Alt_Meter200_L_Needle.png" % path),
    handBImage=imageLoad("%s/skin/Alt_Meter200_S_Needle.png" % path),
)

Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    newData = Telemetry.getData()
    alt.update(newData["RX_alt"])
    alt.draw()
    update()
    clock.tick(Fs=25)
