#!/usr/bin/python
"""
 * Demo_Cockpit.py
 * 
 * Created on: 10 Mar 2023
 * Author:     Guy Soffer
 * 
 *      Copyright (C) 2023 Guy Soffer
"""

import sys, math, random
import pygame
from GSOF_Cockpit import ArtificialHorizon as AH
from GSOF_Cockpit import TurnCoordinator as TC
from GSOF_Cockpit import Battery as BAT
from GSOF_Cockpit import SingleIndicator as SI
from GSOF_Cockpit import DualIndicator as DI
from GSOF_Cockpit import SinglePlot as SP
from GSOF_Cockpit import DualPlot as DP
from GSOF_Cockpit import Text_Widget as TEXT
#from GSOF_Cockpit import Button_Widget as BTN
from GSOF_Cockpit import Pygame_Colors as COLOR

class DemoCockpit():
   def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=(0,0,0), gap=0, folder='./'):
      
      self.screen = screen
      self.colorBG = colorBG

      #Scaling the indicators
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
      background_size = (int(600*scale), int(450*scale))

      #Positioning the gauges
      X0, Y0 = pos
      turn_pos = (X0 +gap, Y0 +gap)
      horizon_pos = (turn_pos[0] +turn_size[0] +gap, turn_pos[1])
      engine_pos = [0]*4
      eGap = 0
      engine_pos[1] = (horizon_pos[0] +horizon_size[0] +gap, horizon_pos[1])          #Arangment
      engine_pos[0] = ((engine_pos[1])[0] +engine_size[0]+ eGap, (engine_pos[1])[1])  #[1] [0]
      engine_pos[2] = ((engine_pos[1])[0], (engine_pos[1])[1] +engine_size[1] +eGap)  #   X
      engine_pos[3] = ((engine_pos[0])[0], (engine_pos[2])[1])                        #[2] [3]

      rfSignal_pos = (turn_pos[0], turn_pos[1] +turn_size[1] +gap)
      BattTitle_pos = ((engine_pos[2])[0], (engine_pos[2])[1] +engine_size[1] +10)
      rxBatt_pos = (BattTitle_pos[0], BattTitle_pos[1] +BattTitle_size[1] +gap)
      txBatt_pos = (rxBatt_pos[0] +battLevel_size[0] +eGap, rxBatt_pos[1])
      
      alt_pos = (rfSignal_pos[0], rfSignal_pos[1] +rfSignal_size[1] +gap)
      vsi_pos = (alt_pos[0] +alt_size[0] +gap, alt_pos[1])
      head_pos = (vsi_pos[0] +vsi_size[0] +gap, vsi_pos[1])
      g_pos = (head_pos[0] +head_size[0] +gap, head_pos[1])

      # Initialise the gauges.
      self.background = TEXT.TextCtrl( GUIobj=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
      self.horizon = AH.ArtificialHorizon( self.screen, pos=horizon_pos, size=horizon_size,
                                   coefList={'RollToDeg':1,   #< Use 360.0/6.28, #When input is in (Rad)
                                             'RollOffset':1,  #< Use 360.0/6.28, #when input is in (Rad)
                                             'PitchToDeg':1,  #< Use 360.0/6.28, #when input is in (Rad)
                                             'PitchOffset':1, #< Use 360.0/6.28, #when input is in (Rad)
                                             'Kp':0.5,        #< Filter coefficiant
                                             }
                                   )
      self.turn = TC.TurnCoord( self.screen, pos=turn_pos, size=turn_size,
                                  coefList={'Turn_Kp':0.2,                #< Filter coefficiant
                                            'TurnRateDegMinMax':(-45,45), #< deg
                                            'TurnRateToDeg':1,            #< Use 360.0/6.28, #When input is in (Rad)
                                            'SideAcc_Kp':0.3,             #< Filter coefficiant
                                            'SlipDegMinMax':(-14,14),     #< deg
                                            'SlipToDeg':1,                #< Use 360.0/6.28, #When input is in (Rad)
                                            }
                                  )
      self.engine = [0]*4
      self.engine[0] = SI.SingleIndicator( self.screen, pos=engine_pos[0], size=engine_size,
                                     imgList={'Frame':pygame.image.load('%s/resources/EngineIndicator_Background.png'%folder),
                                              'Ind':pygame.image.load('%s/resources/EngineIndicator_Needle.png'%folder),
                                              },
                                     coefList={
                                              'InToDeg':-180.0/100,  #< Input value to degrees factor applied after offset
                                              'InOffset':0,          #< Input offeset is added to input value before scale factor
                                              'Kp':0.8,              #< Filter coefficiant
                                              'DegMinMax':(-180,0),  #< Indicator angle min/max (deg)
                                              'DegOffset':0,         #< Angle of indicator at zero input (deg)
                                              'DegModulu':360,       #< Modulu for indicator angle (deg)
                                              }
                                     )
      self.engine[1] = DI.DualIndicator( self.screen, pos=engine_pos[1], size=engine_size,
                                           imgList={'Frame':pygame.image.load('%s/resources/EngineIndicator_Background.png'%folder),
                                                    'IndA':pygame.image.load('%s/resources/EngineIndicator_Needle.png'%folder),
                                                    'IndB':pygame.image.load('%s/resources/AirSpeedNeedle.png'%folder),
                                                    #'Mark':pygame.image.load('resources/Alt_Meter200_Null.png')
                                                    },
                                          coefList={
                                                  'A_ToDeg':-180.0/100, #< Input value to degrees factor applied after offset
                                                  'A_DegOffset':0,      #< Input offeset is added to input value before scale factor
                                                  'A_DegModulu':180,    #< Modulu for indicator angle (deg)
                                                  'A_MinMax':(0,99),    #< Indicator angle min/max (deg)
                                                  'A_Kp':0.8,           #< Filter coefficiant (0-no filter)

                                                  'B_ToDeg':-180.0/100, #< Input value to degrees factor applied after offset
                                                  'B_DegOffset':180,    #< Input offeset is added to input value before scale factor
                                                  'B_DegModulu':180,    #< Modulu for indicator angle (deg)
                                                  'B_MinMax':(0,99),    #< Indicator angle min/max (deg)
                                                  'B_Kp':0.1,           #< Filter coefficiant (0-no filter)
                                           }
                                  )

      self.engine[2] = SI.SingleIndicator( self.screen, pos=engine_pos[2], size=engine_size )
      self.engine[3] = SI.SingleIndicator( self.screen, pos=engine_pos[3], size=engine_size )

      self.battTitle = TEXT.TextCtrl( GUIobj=self.screen,
                                        pos=BattTitle_pos, size=-1,
                                        color=colorBG, textColor=COLOR.WHITE,
                                        name='<--[V] Batt [A]-->' )
      self.Vbat = BAT.Battery( self.screen, pos=rxBatt_pos, size=battLevel_size,
                                                                             #Coefficiants for 3S-LiPo
                                     coefList={'DegMinMax':(-270,0),         #Limits of indicator before applying offset
                                               'DegOffset':135,              #Resting point
                                               'DegModulu':360,
                                               'InToDeg':-270/(3*(4.2-3.0)), #Voltage to degree
                                               'InOffset':-9,                #Lowest input voltage indication
                                               'Kp':0.8,
                                               }
                                     )
      self.Ibat = BAT.Battery( self.screen, pos=txBatt_pos, size=battLevel_size,
                                                                             #Coefficiants current up to 6A
                                     coefList={'DegMinMax':(-270,0),         #Limits of indicator before applying offset
                                               'DegOffset':135,              #Resting point
                                               'DegModulu':360,
                                               'InToDeg':-270/6.0,           #Current to degree
                                               'InOffset':0,                 #Lowest current indication
                                               'Kp':0.8,
                                               }
                                     )
      self.alt = DI.DualIndicator( self.screen, pos=alt_pos, size=alt_size,
#                                  imgList={'Frame':pygame.image.load('skin/Alt_Meter200.png'),
#                                           'IndA':pygame.image.load('skin/Alt_Meter200_L_Needle.png'),
#                                           'IndB':pygame.image.load('skin/Alt_Meter200_S_Needle.png'),
#                                           #'Mark':pygame.image.load('skin/Alt_Meter200_Null.png'),
#                                           },
                                  coefList={'A_DegModulu':360,
                                            'B_DegModulu':360,
                                            'A_DegOffset':0,
                                            'B_DegOffset':0,
                                            'A_ToDeg':-360.0/1000,
                                            'B_ToDeg':-36.0/1000,
                                            'A_MinMax':None,
                                            'B_MinMax':None,
                                            'A_Kp':1,
                                            'B_Kp':1,
                                            }
                                  )
                                 
      self.vsi = SI.SingleIndicator( self.screen, pos=vsi_pos, size=vsi_size,
                               imgList={'Frame':pygame.image.load('%s/resources/VerticalSpeedIndicator_Background.png'%folder),
                                        'Ind':pygame.image.load('%s/resources/VerticalSpeedNeedle.png'%folder),
                                        },
                               coefList={
                                        'InToDeg':-25,
                                        'InOffset':0,
                                        'Kp':0.8,
                                        'DegMinMax':(-180,180),
                                        'DegOffset':90,
                                        'DegModulu':180,
                                        }
                               )

      self.head = DI.DualIndicator( self.screen, pos=head_pos, size=head_size,
                                  imgList={'Frame':pygame.image.load('%s/resources/HeadingIndicator_Background.png'%folder),
                                           'IndA':pygame.image.load('%s/resources/HeadingWheel.png'%folder),
                                           'IndB':pygame.image.load('%s/resources/AirSpeedNeedle.png'%folder),
                                           'Mark':pygame.image.load('%s/resources/HeadingIndicator_Aircraft.png'%folder),
                                           },
                                  coefList={'A_DegModulu':360,
                                            'B_DegModulu':360,
                                            'A_DegOffset':0,
                                            'B_DegOffset':0,
                                            'A_ToDeg':-1,
                                            'B_ToDeg':-1,
                                            'A_MinMax':None,
                                            'B_MinMax':None,
                                            'A_Kp':0.5,
                                            'B_Kp':1,
                                            }
                                  )

      self.g = SI.SingleIndicator( self.screen, pos=g_pos, size=g_size,
                             imgList={'Frame':pygame.image.load('%s/skin/G_Meter200.png'%folder),
                                      'Ind':pygame.image.load('%s/skin/G_Meter_Ind200.png'%folder),
                                   },
                             coefList={
                                       'InToDeg':4.6,
                                       'InOffset':9.8,
                                       'Kp':0.8,
                                       'DegMinMax':(-270,270),
                                       'DegOffset':90,#129,
                                       'DegModulu':270,
                                       }
                            )

##      self.steeringWheel = SI.SingleIndicator( self.screen, pos=g_pos, size=g_size,
##                             imgList={'Frame':pygame.image.load('%s/skin/Indicator_Background.png'%folder),
##                                      'Frame_':pygame.image.load('%s/skin/G_Meter200.png'%folder),
##                                      'Ind':pygame.image.load('%s/skin/SteeringWheel300.png'%folder),
##                                   },
##                             coefList={
##                                       'InToDeg':10.0,
##                                       'InOffset':9.8,
##                                       'Kp':0.8,
##                                       'DegMinMax':(-270,270),
##                                       'DegOffset':0,
##                                       'DegModulu':360,
##                                       }
##                            )

#      #self.rfSignal = DP.DualPlot( self.screen, pos=rfSignal_pos,  size=rfSignal_size )
      self.rfSignal = SP.SinglePlot( self.screen, pos=rfSignal_pos,  size=rfSignal_size )

   def update(self, data_stream):
         """
         Update all the dials. Usually done in a different rate then the actuale display refresh.
         Also each dial can have a behaviour model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
         """
         # Update dials.
         self.horizon.update(rf_data['RX_est_x'], data_stream['RX_est_y'] )
         self.turn.update((-rf_data['RX_est_x'])/2, (rf_data['RX_accel_x'])/4)
         self.engine[0].update(data_stream['RX_eng'])
         self.engine[1].update(data_stream['RX_eng']+random.randrange(-10,10), data_stream['RX_eng'] +random.randrange(-5,5))
         self.engine[2].update(data_stream['RX_eng'])
         self.engine[3].update(data_stream['RX_eng'])
         self.Vbat.update(data_stream['RX_batt_volt'])
         self.Ibat.update(data_stream['RX_batt_cur'])
         #self.rfSignal.update(data_stream['RX_fr_sucsess'], data_stream['TX_fr_sucsess'],a)
         self.rfSignal.update(data_stream['TX_fr_sucsess'],t)
         self.alt.update(rf_data['RX_alt'], rf_data['RX_alt'])
         self.vsi.update(rf_data['RX_head']/10.0)
         self.head.update( data_stream['RX_head']+random.randrange(-5,5), data_stream['RX_head'] +random.randrange(-5,5) )
         self.g.update( data_stream['RX_G'] )
##         self.steeringWheel.update( data_stream['RX_G'] )
         
   def draw(self):
         """
         Draw all the dials. Usually done every 100 to 30 [ms].
         The update method should be called before this method inorder to update the dials values.
         """
         self.background.draw()
         self.horizon.draw()
         self.turn.draw()
         self.engine[0].draw()
         self.engine[1].draw()
         self.engine[2].draw()
         self.engine[3].draw()
         self.battTitle.draw()
         self.Vbat.draw()
         self.Ibat.draw()
         self.rfSignal.draw()
         self.alt.draw()
         self.vsi.draw()
         self.head.draw()
         self.g.draw()
##         self.steeringWheel.draw()

# Initialise screen.
BG_color = (0x22,0x22,0x22)
screen_size=(600,450)
pygame.init()
screen = pygame.display.set_mode(screen_size)
screen.fill((0xff,0xff,0xff))
   
# Initialise Dials.
#path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
path = './GSOF_Cockpit'
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=1.0, folder=path)

t=0
b=0
c=-100
Vbat = 9
Ibat = 0
test = 1
alt = 0
while 1:
   # Main program loop.
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           print('Exiting....')
           sys.exit()   # end program.

   if(test):
      # Use dummy test data
      curPos = pygame.mouse.get_pos()
      
      rf_data = {'RX_eng':50+50*math.sin(6.28*0.01*t), 'RX_fr_sucsess':b, 'RX_alt':alt, 'RX_batt_volt':Vbat,
                 'RX_batt_cur':Ibat, 'TX_fr_sucsess':c, 'RX_accel_x':50*math.sin(6.28*0.01*t), 'RX_G':-9.8*(1+1*math.sin(6.28*0.01*t)),
                 'RX_head':60*math.sin(6.28*0.01*t), 'RX_est_x':(screen_size[0]/2 -curPos[0]), 'RX_est_y':(screen_size[1]/2 -curPos[1])}
      
      pygame.time.delay(30)

      if(rf_data):
         # We have data.
         #print(rf_data)
         t+=1
         b+=1
         c+=2
         Vbat += 0.1
         if Vbat >13:
            Vbat = 9
         Ibat += 0.1
         Ibat %= 6.5
         alt += 10

         # Update dials.
         Cockpit.update(rf_data)
         Cockpit.draw()
         pygame.display.update()



