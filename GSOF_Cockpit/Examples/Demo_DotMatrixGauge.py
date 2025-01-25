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

class DemoCockpit():
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        alt_size = (int(128*scale), int(64*scale))
        background_size = (int(128*scale), int(64*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        alt_pos = (X0 +gap, Y0 +gap)

        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
        self.disp = DISP.DotMatrixDisplay( self.screen, bodyImage=None,
                                           pos=alt_pos, size=alt_size,
                                           bgColor=COLOR.BLACK,
                                           pxColor=COLOR.CYAN,
                                           rows=8, cols=21
                                          )    
    def update(self, newData):
        """
        Update all the dials. Usually done in a different rate then the actual display refresh.
        Also each dial can have a behavior model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        self.disp.printAt( col=0, row=0, s="+-------------------+", X2=False )
        self.disp.printAt( col=0, row=1, s="|                   |", X2=False )
        self.disp.printAt( col=0, row=2, s="|                   |", X2=False )
        self.disp.printAt( col=0, row=3, s="|                   |", X2=False )
        self.disp.printAt( col=0, row=4, s="|                   |", X2=False )
        self.disp.printAt( col=0, row=5, s="|                   |", X2=False )
        self.disp.printAt( col=0, row=6, s="|                   |", X2=False )
        self.disp.printAt( col=0, row=7, s="+-------------------+", X2=False )
        self.disp.printCenter(row=1, s=newData, clrLine=False )
        self.disp.printRight( row=3, s=newData, clrLine=False )
        self.disp.printLeft(  row=5, s=newData, clrLine=True )
        self.disp.printAt( col=4, row=6, s=newData, X2=False )
        
         
    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.disp.draw()

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(768,384)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
#path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
path = "../"
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=6.0, folder=path)
clock = Clock()
i = 0
while True:
    ###Loop to update gauges
    i += 1
    Cockpit.update( newData="Hello World! %d"%i)
    Cockpit.draw()
    update()
    clock.tick(Fs=25)
