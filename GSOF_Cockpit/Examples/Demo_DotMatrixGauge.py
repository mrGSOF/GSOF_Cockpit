#!/usr/bin/python
"""
 * Demo_DotMatrixGauge.py
 * Created on: 20 Jan 2025
 * Author:     Guy Soffer
 * Copyright (C) 2025 Guy Soffer
"""

from GSOF_Cockpit.Generic import DotMatrixDisplay as DISP

from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(768,384)
pos = (0, 0)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
#Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=6.0, folder=path)
background = Text( screen=screen, pos=pos, size=screen_size, color=BG_color, name='' )
disp = DISP.DotMatrixDisplay( screen, bodyImage=None,
                              pos=pos, size=screen_size,
                              bgColor=COLOR.BLACK,
                              pxColor=COLOR.CYAN,
                              rows=8, cols=21
                            )

clock = Clock()
i = 0
while True:
    ###Loop to update gauges
    i += 1
    string = "Hello World! %d"%i
    disp.printAt( col=0, row=0, s="+-------------------+", X2=False )
    disp.printAt( col=0, row=1, s="|                   |", X2=False )
    disp.printAt( col=0, row=2, s="|                   |", X2=False )
    disp.printAt( col=0, row=3, s="|                   |", X2=False )
    disp.printAt( col=0, row=4, s="|                   |", X2=False )
    disp.printAt( col=0, row=5, s="|                   |", X2=False )
    disp.printAt( col=0, row=6, s="|                   |", X2=False )
    disp.printAt( col=0, row=7, s="+-------------------+", X2=False )
    disp.printCenter(row=1, s=string, clrLine=False )
    disp.printRight( row=3, s=string, clrLine=False )
    disp.printLeft(  row=5, s=string, clrLine=True )
    disp.printAt( col=4, row=6, s=string, X2=False )
    disp.printAt( col=1, row=2, s="X2", X2=True )

    background.draw()
    disp.draw()
    update()
    clock.tick(Fs=25)
