## Created on: 9 Dec 2024
## Author    : Guy Soffer

import os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad
   
class PercentageFill(SingleIndicator):
   """Percentage dial with fill mark and maximum rabge of 180 degrees"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None,
                inputGain = 1.0,
                inputOffset = 0.0,
                inputMin = 0,
                inputMax = 100,
                kp       = 0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = imageLoad(os.path.join(path, '../resources/EngineIndicator_Background.png'))
      if handImage == None:
         handImage = imageLoad(os.path.join(path, '../resources/EngineIndicator_Needle.png'))

      super().__init__(screen, pos, size,
                       bodyImage   = bodyImage,
                       handImage   = handImage,
                       inputGain   = inputGain,
                       inputOffset = inputOffset,
                       kp          = kp,
                       inputToDeg  = -180/(inputMax-inputMin),
                       offset_deg  = 0,
                       minMax_deg  = (-180, 0))

class Percentage(SingleIndicator):
   """Percentage dial with needle and full turn range (360 degree)"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None,
                inputGain = 1.0,
                inputOffset = 0.0,
                inputMin = 0,
                inputMax = 100,
                kp       = 0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = imageLoad(os.path.join(path, '../resources/Indicator_Background.png'))
      if handImage == None:
         handImage = imageLoad(os.path.join(path, '../resources/AirSpeedNeedle.png'))

      super().__init__(screen, pos, size,
                       bodyImage   = bodyImage,
                       handImage   = handImage,
                       inputGain   = inputGain,
                       inputOffset = inputOffset,
                       kp          = kp,
                       inputToDeg  = -360/(inputMax-inputMin),
                       offset_deg  = 180,
                       minMax_deg  = (-180, 180))
