#!/usr/bin/python
"""
 * Quad_Cockpit.py
 * 
 * Created on: 28 Mar 2017
 * Author:     Guy Soffer
 * 
 *      Copyright (C) 2017 Guy Soffer
"""

import sys, math, random
#import inspect
import pkg_resources
import pygame
#from GSOF_Pygame_Cockpit import Pygame_CockpitInstView as INST
from GSOF_Pygame_Cockpit import Pygame_CockpitInstView as INST
from GSOF_SmartSampler import Pygame_Widget as Widget
from GSOF_SmartSampler import Pygame_Colors as COLOR
##import Pygame_CockpitInstView as INST

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

      #Positioning the indicators
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

      # Initialise Dials.
      self.background = Widget.TextCtrl( GUIobj=self.screen, pos=pos, size=background_size, color=colorBG, name='' )
      self.horizon = INST.Horizon( self.screen, pos=horizon_pos, size=horizon_size,
                                   coefList={'RollToDeg':1, #360.0/6.28, #For [Rad]
                                             'PitchToDeg':1, #360.0/6.28, #For [Rad]
                                             'Kp':0.5,
                                             }
                                   )
      self.turn = INST.TurnCoord( self.screen, pos=turn_pos, size=turn_size,
                                  coefList={'Turn_Kp':0.2,
                                            'TurnRateDegMinMax':(-45,45),
                                            'TurnRateToDeg':1,
                                            'SideAcc_Kp':0.3,
                                            'SlipDegMinMax':(-14,14),
                                            'SlipToDeg':1,
                                            }
                                  )
      self.engine = [0]*4
      self.engine[0] = INST.Generic( self.screen, pos=engine_pos[0], size=engine_size,
                                     imgList={'Frame':'%s/resources/EngineIndicator_Background.png'%folder,
                                              'Ind':'%s/resources/EngineIndicator_Needle.png'%folder,
                                              },
                                     coefList={
                                              'InToDeg':-180.0/100,
                                              'InOffset':0,
                                              'Kp':0.8,
                                              'DegMinMax':(-180,0),
                                              'DegOffset':0,
                                              'DegModulu':360,
                                              }
                                     )
      self.engine[1] = INST.DualIndicator( self.screen, pos=engine_pos[1], size=engine_size,
                                           imgList={'Frame':'%s\\resources/EngineIndicator_Background.png'%folder,
                                                    'IndA':'%s\\resources/EngineIndicator_Needle.png'%folder,
                                                    'IndB':'%s\\resources/AirSpeedNeedle.png'%folder,
                                                   #'Mark':'resources/Alt_Meter200_Null.png'
                                                    },
                                          coefList={
                                                  'A_DegOffset':0,
                                                  'B_DegOffset':180,
                                                  'A_DegModulu':180,
                                                  'B_DegModulu':180,
                                                  'A_ToDeg':-180.0/100,
                                                  'B_ToDeg':-180.0/100,
                                                  'A_MinMax':(0,99),
                                                  'B_MinMax':(0,99),
                                                  'A_Kp':0.8,
                                                  'B_Kp':0.1,
                                           }
                                  )
#      self.engine[1] = INST.Generic( self.screen, pos=engine_pos[1], size=engine_size )
      self.engine[2] = INST.Generic( self.screen, pos=engine_pos[2], size=engine_size )
      self.engine[3] = INST.Generic( self.screen, pos=engine_pos[3], size=engine_size )

      self.battTitle = Widget.TextCtrl( GUIobj=self.screen,
                                        pos=BattTitle_pos, size=-1,
                                        color=colorBG, textColor=COLOR.WHITE,
                                        name='<--[V] Batt [A]-->' )
      self.Vbat = INST.Battery( self.screen, pos=rxBatt_pos, size=battLevel_size,
                                                                             #Coefficiants for 3S-LiPo
                                     coefList={'DegMinMax':(-270,0),         #Limits of indicator before applying offset
                                               'DegOffset':135,              #Resting point
                                               'DegModulu':360,
                                               'InToDeg':-270/(3*(4.2-3.0)), #Voltage to degree
                                               'InOffset':-9,                #Lowest input voltage indication
                                               'Kp':0.8,
                                               }
                                     )
      self.Ibat = INST.Battery( self.screen, pos=txBatt_pos, size=battLevel_size,
                                                                             #Coefficiants current up to 6A
                                     coefList={'DegMinMax':(-270,0),         #Limits of indicator before applying offset
                                               'DegOffset':135,              #Resting point
                                               'DegModulu':360,
                                               'InToDeg':-270/6.0,           #Current to degree
                                               'InOffset':0,                 #Lowest current indication
                                               'Kp':0.8,
                                               }
                                     )

      self.alt = INST.DualIndicator( self.screen, pos=alt_pos, size=alt_size,
#                                  imgList={'Frame':'skin/Alt_Meter200.png',
#                                           'IndA':'skin/Alt_Meter200_L_Needle.png',
#                                           'IndB':'skin/Alt_Meter200_S_Needle.png',
#                                           #'Mark':'skin/Alt_Meter200_Null.png',
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
                                 
      self.vsi = INST.Generic( self.screen, pos=vsi_pos, size=vsi_size,
                               imgList={'Frame':'%s/resources/VerticalSpeedIndicator_Background.png'%folder,
                                        'Ind':'%s/resources/VerticalSpeedNeedle.png'%folder,
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

      self.head = INST.DualIndicator( self.screen, pos=head_pos, size=head_size,
                                  imgList={'Frame':'%s/resources/HeadingIndicator_Background.png'%folder,
                                           'IndA':'%s/resources/HeadingWheel.png'%folder,
                                           'IndB':'%s/resources/AirSpeedNeedle.png'%folder,
                                           'Mark':'%s/resources/HeadingIndicator_Aircraft.png'%folder,
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

      self.g = INST.Generic( self.screen, pos=g_pos, size=g_size,
                             imgList={'Frame':'%s/skin/G_Meter200.png'%folder,
                                      'Ind':'%s/skin/G_Meter_Ind200.png'%folder,
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

      #self.rfSignal = INST.DualPlot( self.screen, pos=rfSignal_pos,  size=rfSignal_size )
      self.rfSignal = INST.SinglePlot( self.screen, pos=rfSignal_pos,  size=rfSignal_size )

   def update(self, data_stream):
         """
         Updating all the dials. Usually done in a different rate then the actuale display refresh.
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

   def draw(self):
         """
         Drawing all the dials. Usually done every 100 to 20 [ms].
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

# Initialise screen.
BG_color = (0x22,0x22,0x22)
screen_size=(600,450)
pygame.init()
screen = pygame.display.set_mode(screen_size)
screen.fill((0xff,0xff,0xff))
   
# Initialise Dials.
path = pkg_resources.resource_filename('GSOF_Pygame_Cockpit', '')
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



