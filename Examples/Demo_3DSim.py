#!/usr/bin/python
"""
 * Demo_Cockpit.py
 * Created on: 10 Mar 2023
 * Author:     Guy Soffer
 * Copyright (C) 2023 Guy Soffer
"""

import sys, math, random, time
import pygame
from GSOF_Cockpit.Aerospace import ArtificialHorizon as AH
from GSOF_Cockpit.Aerospace import TurnCoordinator_Analog as TC
from GSOF_Cockpit.Aerospace import AltMeter_Analog as ALT
from GSOF_Cockpit.Aerospace import AirSpeedMeter_Analog as AS
from GSOF_Cockpit.Aerospace import VsiMeter_Analog as VSI
from GSOF_Cockpit.Aerospace import Heading_Analog as HEAD

try:
   from GSOF_Cockpit.Wireframe3D import World3D as WORLD
   from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
   from GSOF_3dWireFrame.Lib3D import Object_base as OB
   from GSOF_3dWireFrame.Lib3D import Objects
   _3D_active = True
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't instlled")

##from GSOF_Cockpit.Button import Button_Rect
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import getMouse, imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

class DemoCockpit():
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        world_size = (int(600*scale), int(300*scale))
        turn_size = (int(150*scale), int(150*scale))
        horizon_size = (int(150*scale), int(150*scale))
        alt_size = (int(150*scale), int(150*scale))
        vsi_size = (int(150*scale), int(150*scale))
        head_size = (int(150*scale), int(150*scale))
        as_size = (int(150*scale), int(150*scale))
        background_size = (int(600*scale), int(600*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        world_pos   = (X0 +gap, Y0 +gap)
        as_pos      = (world_pos[0] +75, world_pos[1] +world_size[1] +gap)
        horizon_pos = (as_pos[0] +as_size[0] +gap, as_pos[1])
        alt_pos     = (horizon_pos[0] +horizon_size[0] +gap, horizon_pos[1])

        turn_pos = (as_pos[0], as_pos[1] +as_size[1] +gap)
        head_pos = (turn_pos[0] +turn_size[0] +gap, turn_pos[1])
        vsi_pos  = (head_pos[0] +head_size[0] +gap, head_pos[1])

##        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
        PI = math.pi
        net   = OWF.Object_wireFrame(obj=Objects.net(25,25), color=(0,100,0)).rotate(x=PI/2, y=0, z=0).translate(V=(-1000, -2000, -1000), initShape=True).scale(0.2, initShape=True)
        axis  = OWF.Object_wireFrame(filename="%s/objects/axis.json"%folder, color=(10,10,10 )).translate(V=(0, 0, 0), initShape=True).scale(1.5, initShape=True)
        plane = OWF.Object_wireFrame(filename="%s/objects/c172.stl"%folder,   color=( 0, 0,255)).rotate(x=-PI/2, y=0, z=0).translate(V=(0, 0, 0), initShape=True)
        plane.setOrigin( origin=plane.getOrigin(origin="arithCenter"), initShape=True ).scale(0.035, initShape=True)
        world = OB.Object_container(objList=(net, axis, plane))
        self.world = WORLD.World( self.screen, pos=world_pos, size=world_size, world=world,
                                  bodyImage=imageLoad('%s/skin/Frame_Rect600x300.png'%folder))

        self.airSpd = AS.AirSpeedMeter( self.screen, pos=as_pos, size=as_size )
        self.horizon = AH.ArtificialHorizon( self.screen, pos=horizon_pos, size=horizon_size)
        self.alt = ALT.AltMeter( self.screen, pos=alt_pos, size=alt_size )    

        self.turn = TC.TurnCoord( self.screen, pos=turn_pos, size=turn_size,
                                  turnRateToDeg      = 1.0,      #< Use 180.0/3.14 when input is in (Rad)
                                  turnRateKp         = 0.2,      #< Filter coefficiant
                                  turnRateMinMax_deg = (-45,45), #< deg
                                  slipToDeg          = 1.0,      #< Use 180.0/3.14 when input is in (Rad)
                                  slipKp             = 0.3,      #< Filter coefficiant
                                  slipMinMax_deg     = (-14,14), #< deg
                                )
        self.head = HEAD.Heading( self.screen, pos=head_pos, size=head_size)
        self.vsi = VSI.VsiMeter( self.screen, pos=vsi_pos, size=vsi_size)

    def update(self, data_stream):
        """
        Update all the dials. Usually done in a different rate then the actuale display refresh.
        Also each dial can have a behaviour model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        # Update dials.
        self.world.update( x=data_stream['RX_worldX'], y=data_stream['RX_worldY'], z=data_stream['RX_worldZ'],
                           yaw=data_stream['RX_worldYaw'], pitch=data_stream['RX_worldPitch'], roll=data_stream['RX_worldRoll'] )
        self.horizon.update( -rf_data['RX_est_x'], -data_stream['RX_est_y'] )
        self.turn.update( (rf_data['RX_est_x'])/2, (rf_data['RX_accel_x'])/4 )
        self.alt.update( rf_data['RX_alt'] )
        self.vsi.update( rf_data['RX_vsi'] )
        self.head.update( data_stream['RX_head']+random.randrange(-5,5), data_stream['RX_head']+random.randrange(-5,5) )
        self.airSpd.update( data_stream['RX_airSpd'] )
         
    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.world.draw()

        self.horizon.draw()
        self.turn.draw()
        self.alt.draw()
        self.vsi.draw()
        self.head.draw()
        self.airSpd.draw()

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(600,600)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
#path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
path = '../GSOF_Cockpit'
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=1.0, folder=path)

t=0
b=0
c=-100
test = 1
alt = 0
airSpd = 0.0
vsi = 5
clock = Clock()

while True:
    # Main program loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Exiting....')
            sys.exit()   # end program.

    if(test):
        # Use dummy test data
        curPos = (getMouse())["pos"]

        # We have data.
        t+=1
        b+=1
        c+=2
        alt += 10
        airSpd += 5.0
        if airSpd > 800.0:
            airSpd = 0.0

        head_r = 6.24*0.5*t*0.01
        posY   = 40*math.sin(head_r)
        posX   = 40*math.cos(head_r)
        head_d = head_r*180/3.14 +180

        rf_data = {'RX_alt':alt, 'RX_accel_x':50*math.sin(6.28*0.01*t),
                   'RX_est_x':(screen_size[0]/2 -curPos[0]), 'RX_est_y':(screen_size[1]/2 -curPos[1]),
                   'RX_vsi':vsi*math.sin(6.28*0.01*t), 'RX_airSpd':airSpd,
                   'RX_posX':posX, 'RX_posY':posY, 'RX_head':head_d,
                   'RX_worldX':0, 'RX_worldY':0, 'RX_worldZ':-600.0,
                   'RX_worldYaw':-head_d +180, 'RX_worldPitch':0.0, 'RX_worldRoll':45.0}

        # Update gauges
        Cockpit.update(rf_data)
        Cockpit.draw()
        update()
        clock.tick(Fs=25)
