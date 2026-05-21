#!/usr/bin/python
"""
 * Demo_AltGauge.py
 * Created on: 19 May 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from Data import Data
from GSOF_Cockpit.Plot import Plot as PLOT
from GSOF_Cockpit.DualPlot import DualPlot as DPLOT

from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(600,600)
pos = (0, 0)
size = (600,300)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
path = '../'
background = Text(  screen=screen, pos=pos, size=size, color=BG_color, name='' )

plot1 = PLOT( screen=screen, pos=pos, size=size,
              bodyImage=imageLoad('%s/skin/oldOscilloscope.png'%path),
              A_MinMax = (-50, 50),
              leftMargin=205, topMargin=42, rightMargin=165, botMargin=75,
              style = 'dot', colors = (COLOR.RED, COLOR.GREEN)
            ) 

plot2 = DPLOT( screen=screen, pos=(pos[0], pos[1] +size[1]), size=size,
              bodyImage=imageLoad('%s/skin/Frame_Rect.png'%path),
              A_MinMax = (-50, 50), B_MinMax = (-50, 50),
              leftMargin=10, topMargin=10, rightMargin=10, botMargin=10,
              style = 'filled', colors = (COLOR.GRAY, COLOR.DARK)
            )

Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    newData = Telemetry.getData()
    plot1.update( newData['RX_posX'], newData['RX_posY'] )
    plot2.update( newData['RX_posX'], newData['RX_posY'] )
    plot1.draw()
    plot2.draw()
    update()
    clock.tick(Fs=25)
