#!/usr/bin/python
"""
 * Demo_Minimap.py
 * Created on: 20 Jan 2025
 * Author:     Guy Soffer
 * Copyright (C) 2025 Guy Soffer
"""
import math
from Data import Data
from GSOF_Cockpit.Generic import Map as MAP

from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import getMouse, imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

class DemoCockpit():
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        map_size = (int(600*scale), int(300*scale))
        background_size = (int(600*scale), int(300*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        map_pos = (X0 +gap, Y0 +gap)

        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
        self.map = MAP.Map( self.screen, pos=map_pos, size=map_size,
                            kp = 0.7,
                            bodyImage   = imageLoad('%s/skin/Frame_Rect600x300.png'%folder),
                            mapImage    = imageLoad('%s/skin/Grid_BackgroundWhite600x300.png'%folder),
                            markerImage = imageLoad('%s/skin/car.png'%folder),
                            
                            )

    def update(self, newData):
        """
        Update all the dials. Usually done in a different rate then the actual display refresh.
        Also each dial can have a behavior model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        x,y     = -newData["RX_est_x"], -newData["RX_est_y"]
        dtx,dty =  newData["RX_mouseDtX"], -newData["RX_mouseDtY"]
        head = -180*math.atan2(dty, dtx)/math.pi +90
        self.map.update( x=x, y=y, deg=head )
         
    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.map.draw()

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(600,300)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
#path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
path = '../'
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=1.0, folder=path)
Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    Cockpit.update( Telemetry.getData() )
    Cockpit.draw()
    update()
    clock.tick(Fs=25)
