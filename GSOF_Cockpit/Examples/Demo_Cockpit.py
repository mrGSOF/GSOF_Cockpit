#!/usr/bin/python
"""
 * Demo_Cockpit.py
 * Created on: 10 Mar 2023
 * Author:     Guy Soffer
 * Copyright (C) 2023 Guy Soffer
"""

import sys, math, random, time, os
import pygame
from GSOF_Cockpit.Automotive import SteeringWheel as SW
from GSOF_Cockpit.Aerospace import ArtificialHorizon as AH
from GSOF_Cockpit.Aerospace import TurnCoordinator_Analog as TC
from GSOF_Cockpit.Aerospace import AltMeter_Analog as ALT
from GSOF_Cockpit.Aerospace import GMeter_Analog as G
from GSOF_Cockpit.Aerospace import AirSpeedMeter_Analog as AS
from GSOF_Cockpit.Aerospace import VsiMeter_Analog as VSI
from GSOF_Cockpit.Aerospace import Heading_Analog as HEAD
from GSOF_Cockpit.Generic import Battery as BAT
from GSOF_Cockpit.Generic import Completion as COMP
from GSOF_Cockpit.Generic import SetPointVsFeedback as SPFB
from GSOF_Cockpit.Generic import Map as MAP

try:
   from GSOF_Cockpit.Wireframe3D import World3D as WORLD
   from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
   from GSOF_3dWireFrame.Lib3D import Object_base as OB
   from GSOF_3dWireFrame.Lib3D import Objects
   _3D_active = True
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't instlled")

from GSOF_Cockpit.Button import Button_Rect
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import getMouse, imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import SinglePlot as SP
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

class DemoCockpit():
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        turn_size = (int(150*scale), int(150*scale))
        horizon_size = (int(300*scale), int(300*scale))
        engine_size = (int(75*scale), int(75*scale))
        rfSignal_size = (int(150*scale), int(150*scale))
        BattTitle_size = (int(150*scale), int(25*scale))
        battLevel_size = (int(75*scale), int(75*scale))
        alt_size = (int(150*scale), int(150*scale))
        vsi_size = (int(150*scale), int(150*scale))
        head_size = (int(150*scale), int(150*scale))
        g_size = (int(150*scale), int(150*scale))
        as_size = (int(150*scale), int(150*scale))
        steeringWheel_size = (int(150*scale), int(150*scale))
        map_size = (int(150*scale), int(150*scale))
        world_size = (int(150*scale), int(150*scale))
        background_size = (int(600*scale), int(600*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        turn_pos = (X0 +gap, Y0 +gap)
        horizon_pos = (turn_pos[0] +turn_size[0] +gap, turn_pos[1])
        engine_pos = [0]*4
        eGap = 0
        engine_pos[0] = (horizon_pos[0] +horizon_size[0] +gap, horizon_pos[1])          #Arangment
        engine_pos[3] = ((engine_pos[0])[0] +engine_size[0]+ eGap, (engine_pos[0])[1])  #[0] [3]
        engine_pos[1] = ((engine_pos[0])[0], (engine_pos[0])[1] +engine_size[1] +eGap)  #   X
        engine_pos[2] = ((engine_pos[3])[0], (engine_pos[1])[1])                        #[1] [2]

        rfSignal_pos  = (turn_pos[0], turn_pos[1] +turn_size[1] +gap)
        BattTitle_pos = ((engine_pos[1])[0], (engine_pos[1])[1] +engine_size[1] +10)
        rxBatt_pos    = (BattTitle_pos[0], BattTitle_pos[1] +BattTitle_size[1] +gap)
        txBatt_pos    = (rxBatt_pos[0] +battLevel_size[0] +eGap, rxBatt_pos[1])
        testBtn_pos   = (rxBatt_pos[0] +10, rxBatt_pos[1] +battLevel_size[1] +10)

        alt_pos = (rfSignal_pos[0], rfSignal_pos[1] +rfSignal_size[1] +gap)
        vsi_pos = (alt_pos[0] +alt_size[0] +gap, alt_pos[1])
        head_pos = (vsi_pos[0] +vsi_size[0] +gap, vsi_pos[1])
        g_pos = (head_pos[0] +head_size[0] +gap, head_pos[1])
        as_pos = (alt_pos[0], alt_pos[1] +alt_size[1] +gap)
        steeringWheel_pos =  (as_pos[0] +as_size[0] +gap, as_pos[1])
        map_pos =  (steeringWheel_pos[0] +steeringWheel_size[0] +gap, steeringWheel_pos[1])
        world_pos =  (map_pos[0] +map_size[0] +gap, map_pos[1])

        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
        self.horizon = AH.ArtificialHorizon( self.screen, pos=horizon_pos, size=horizon_size)

        self.turn = TC.TurnCoord( self.screen, pos=turn_pos, size=turn_size,
                                  turnRateToDeg      = 1.0,      #< Use 180.0/3.14 when input is in (Rad)
                                  turnRateKp         = 0.2,      #< Filter coefficiant
                                  turnRateMinMax_deg = (-45,45), #< deg
                                  slipToDeg          = 1.0,      #< Use 180.0/3.14 when input is in (Rad)
                                  slipKp             = 0.3,      #< Filter coefficiant
                                  slipMinMax_deg     = (-14,14), #< deg
                                )
        self.engine = [0]*4
        self.engine[0] = COMP.Percentage(self.screen, pos=engine_pos[0], size=engine_size)
        self.engine[1] = SPFB.SetPointVsFeedbackFill(self.screen, pos=engine_pos[1], size=engine_size)
        self.engine[2] = COMP.PercentageFill(self.screen, pos=engine_pos[2], size=engine_size)
        self.engine[3] = COMP.PercentageFill(self.screen, pos=engine_pos[3], size=engine_size)

        self.battTitle = Text( screen=self.screen,
                               pos=BattTitle_pos, size=None,
                               color=colorBG, textColor=COLOR.WHITE,
                               name="<--[V] Batt [A]-->" )

        self.testBtn = Button_Rect( screen=self.screen,
                                    pos=testBtn_pos, size=None,
                                    color=COLOR.RED, textColor=COLOR.WHITE,
                                    name="testButton" )

        self.Vbat = BAT.Battery( self.screen, pos=rxBatt_pos, size=battLevel_size,
                                 inputMin = 3*3.0,             #< Lowest voltage of 3S-Lipo
                                 inputMax = 3*4.2              #< Maximum voltageof 3S-Lipo pack
                                )
        self.Ibat = BAT.Battery( self.screen, pos=txBatt_pos, size=battLevel_size,
                                 inputMin = 0,
                                 inputMax = 6
                                 )
        self.alt = ALT.AltMeter( self.screen, pos=alt_pos, size=alt_size,
                                 digitsColor=COLOR.WHITE,
                                 bodyImage  = imageLoad('%s/skin/Alt_Meter200.png'%folder),
                                 handAImage = imageLoad('%s/skin/Alt_Meter200_L_Needle.png'%folder),
                                 handBImage = imageLoad('%s/skin/Alt_Meter200_S_Needle.png'%folder),
                                )    
        self.vsi = VSI.VsiMeter( self.screen, pos=vsi_pos, size=vsi_size)
        self.head = HEAD.Heading( self.screen, pos=head_pos, size=head_size)
        self.g = G.GMeter_Analog( self.screen, pos=g_pos, size=g_size )
        self.airSpd = AS.AirSpeedMeter( self.screen, pos=as_pos, size=as_size )
        self.steeringWheel = SW.SteeringWheel( self.screen, pos=steeringWheel_pos, size=steeringWheel_size,
                                               wheelImage = imageLoad('%s/skin/SteeringWheel.png'%folder) )
        self.map = MAP.Map( self.screen, pos=map_pos, size=map_size )

        axis  = OWF.Object_wireFrame(filename="%s/objects/axis.json"%folder, color=(10,10,10 )).translate(V=(0, 0, 0), initShape=True).scale(1.5, initShape=True)
        plane = OWF.Object_wireFrame(filename="%s/objects/F16.stl"%folder,   color=( 0, 0,255)).translate(V=(0, 0, 0), initShape=True)
        plane.setOrigin( origin=plane.getOrigin(origin="arithCenter"), initShape=True ).scale(0.015, initShape=True)
        world = OB.Object_container(objList=(axis, plane))

        self.world = WORLD.World( self.screen, pos=world_pos, size=world_size, world = world)

##        self.rfSignal = DP.DualPlot( self.screen, pos=rfSignal_pos,  size=rfSignal_size )
        self.rfSignal = SP.SinglePlot( self.screen, pos=rfSignal_pos,  size=rfSignal_size )

    def update(self, data_stream):
        """
        Update all the dials. Usually done in a different rate then the actuale display refresh.
        Also each dial can have a behaviour model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        # Update dials.
        self.horizon.update( -rf_data['RX_est_x'], -data_stream['RX_est_y'] )
        self.turn.update( (rf_data['RX_est_x'])/2, (rf_data['RX_accel_x'])/4 )
        self.engine[0].update( data_stream['RX_eng'] )
        self.engine[1].update( val=data_stream['RX_eng']+random.randrange(-5,5), valB=data_stream['RX_eng'] )
        self.engine[2].update( data_stream['RX_eng'] )
        self.engine[3].update( data_stream['RX_eng'] )
        self.Vbat.update( data_stream['RX_batt_volt'] )
        self.Ibat.update( data_stream['RX_batt_cur'] )
        #self.rfSignal.update( data_stream['RX_fr_sucsess'], data_stream['TX_fr_sucsess'], a )
        self.rfSignal.update( data_stream['TX_fr_sucsess'],t )
        self.alt.update( rf_data['RX_alt'] )
        self.vsi.update( rf_data['RX_vsi'] )
        self.head.update( data_stream['RX_head']+random.randrange(-5,5), data_stream['RX_head']+random.randrange(-5,5) )
        self.g.update( data_stream['RX_G'] )
        self.airSpd.update( data_stream['RX_airSpd'] )
        self.steeringWheel.update( data_stream['RX_G'] )
        self.map.update( x=data_stream['RX_posX'], y=data_stream['RX_posY'], deg=data_stream['RX_head'] )
        self.world.update( x=data_stream['RX_worldX'], y=data_stream['RX_worldY'], z=data_stream['RX_worldZ'],
                           yaw=data_stream['RX_worldYaw'], pitch=data_stream['RX_worldPitch'], roll=data_stream['RX_worldRoll'] )
        self.testBtn.action( mouse=getMouse() )
         
    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.horizon.draw()
        self.turn.draw()
        self.engine[0].draw()
        self.engine[1].draw()
        self.engine[2].draw()
        self.engine[3].draw()
        self.battTitle.draw()
        self.testBtn.draw()
        self.Vbat.draw()
        self.Ibat.draw()
        self.rfSignal.draw()
        self.alt.draw()
        self.vsi.draw()
        self.head.draw()
        self.g.draw()
        self.airSpd.draw()
        self.steeringWheel.draw()
        self.map.draw()
        self.world.draw()

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(600,600)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
#path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
path = '../'
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=1.0, folder=path)

t=0
b=0
c=-100
Vbat = 9
Ibat = 0
test = 1
alt = 0
g = 9.8
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
        Vbat += 0.1
        if Vbat >13:
            Vbat = 9
        Ibat += 0.1
        Ibat %= 6.5
        alt += 10
        airSpd += 5.0
        if airSpd > 800.0:
            airSpd = 0.0

        head_r = 6.24*0.5*t*0.01
        posY   = 40*math.sin(head_r)
        posX   = 40*math.cos(head_r)
        head_d = head_r*180/3.14 +180

        rf_data = {'RX_eng':50+50*math.sin(6.28*0.01*t), 'RX_fr_sucsess':b, 'RX_alt':alt, 'RX_batt_volt':Vbat,
                   'RX_batt_cur':Ibat, 'TX_fr_sucsess':posX, 'RX_accel_x':50*math.sin(6.28*0.01*t), 'RX_G':g*(math.sin(6.28*0.01*t)),
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
