#!/usr/bin/python
"""
 * Demo_Minimap.py
 * Created on: 20 Jan 2025
 * Author:     Guy Soffer
 * Copyright (C) 2025 Guy Soffer
"""
from Data import Data
from GSOF_Cockpit.Generic import Map as MAP

from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

size = (600, 300)
pos = (0, 0)
init()
screen = getScreen(size)
fillScreen( screen, COLOR.WHITE )

Telemetry = Data(size)
clock = Clock()

background = Text( screen=screen, pos=pos, size=size, color=COLOR.DARK, name='' )
minimap = MAP.Map( screen, pos=pos, size=size,
                    kp = 0.9,
                    bodyImage   = imageLoad("../skin/Frame_Rect600x300.png"),
                    mapImage    = imageLoad("../skin/Grid_BackgroundWhite600x300.png"),
                    markerImage = imageLoad("../skin/car.png"),
                    )

while True:
    data = Telemetry.getData()

    x,y,heading = data["RX_mouseX"], data["RX_mouseY"], data["RX_heading"]
    minimap.update( x=x, y=y, deg=heading )
    background.draw()
    minimap.draw()
    update()
    clock.tick(Fs=25)
