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

class DemoCockpit():
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        alt_size = (int(150*scale), int(150*scale))
        background_size = (int(150*scale), int(150*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        alt_pos = (X0 +gap, Y0 +gap)

        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
        self.alt = ALT.AltMeter( self.screen, pos=alt_pos, size=alt_size,
                                 digitsColor=COLOR.WHITE,
                                 bodyImage  = imageLoad('%s/skin/Alt_Meter200.png'%folder),
                                 handAImage = imageLoad('%s/skin/Alt_Meter200_L_Needle.png'%folder),
                                 handBImage = imageLoad('%s/skin/Alt_Meter200_S_Needle.png'%folder),
                                )    

    def update(self, newData):
        """
        Update all the dials. Usually done in a different rate then the actual display refresh.
        Also each dial can have a behavior model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        self.alt.update( newData['RX_alt'] )
         
    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.alt.draw()

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(300,300)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
#path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
path = '../'
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=2.0, folder=path)
Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    Cockpit.update( Telemetry.getData() )
    Cockpit.draw()
    update()
    clock.tick(Fs=25)
