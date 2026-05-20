#!/usr/bin/python
"""
 * Demo_AltGauge.py
 * Created on: 19 May 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from Data import Data
from GSOF_Cockpit.DualPlot import DualPlot as DPLOT

from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(300,300)
pos = (0, 0)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
path = '../'
background = Text(  screen=screen, pos=pos, size=screen_size, color=BG_color, name='' )
plot = DPLOT( screen=screen, pos=pos, size=screen_size,
              bodyImage=imageLoad('%s/skin/Frame_Rect.png'%path),
            )    

Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    newData = Telemetry.getData()
    plot.update( newData['RX_alt'] )
    plot.draw()
    update()
    clock.tick(Fs=25)
