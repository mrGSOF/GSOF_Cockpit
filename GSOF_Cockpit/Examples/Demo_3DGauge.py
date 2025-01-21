#!/usr/bin/python
"""
 * Demo_3DGauge.py
 * Created on: 20 Jan 2025
 * Author:     Guy Soffer
 * Copyright (C) 2025 Guy Soffer
"""

import math
from Data import Data
try:
   from GSOF_Cockpit.Wireframe3D import World3D as WORLD
   from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
   from GSOF_3dWireFrame.Lib3D import Object_base as OB
   from GSOF_3dWireFrame.Lib3D import Objects
   _3D_active = True
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't installed")

##from GSOF_Cockpit.Button import Button_Rect
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

class DemoCockpit():
    """Constructs the gauges screen"""
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        world_size = (int(600*scale), int(600*scale))
        background_size = (int(600*scale), int(600*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        world_pos   = (X0 +gap, Y0 +gap)

        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
        PI = math.pi
        net   = OWF.Object_wireFrame(obj=Objects.net(25,25), color=(0,100,0)).rotate(x=PI/2, y=0, z=0).translate(V=(-1000, -2000, -1000), initShape=True).scale(0.2, initShape=True)
        axis  = OWF.Object_wireFrame(filename="%s/objects/axis.json"%folder, color=(10,10,10 )).translate(V=(0, 0, 0), initShape=True).scale(1.5, initShape=True)
        plane = OWF.Object_wireFrame(filename="%s/objects/c172.stl"%folder,   color=( 0, 0,255)).rotate(x=-PI/2, y=0, z=0).translate(V=(0, 0, 0), initShape=True)
        plane.setOrigin( origin=plane.getOrigin(origin="arithCenter"), initShape=True ).scale(0.035, initShape=True)
        world = OB.Object_container(objList=(net, axis, plane))
        self.world = WORLD.World( self.screen, pos=world_pos, size=world_size, world=world,
                                  bodyImage=imageLoad('%s/skin/Frame_Rect600x600.png'%folder))

    def update(self, newData):
        """
        Update all the dials. Usually done in a different rate then the actuale display refresh.
        Also each dial can have a behaviour model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        self.world.update( x=newData['RX_worldX'], y=newData['RX_worldY'], z=newData['RX_worldZ'],
                           yaw=newData['RX_worldYaw'], pitch=newData['RX_worldPitch'], roll=newData['RX_worldRoll'] )
         
    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.world.draw()

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(600,600)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
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
