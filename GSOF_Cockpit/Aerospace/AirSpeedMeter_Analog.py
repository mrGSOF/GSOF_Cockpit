## Created on: 2/Dec 2024
## Author    : Guy Soffer
import os, pygame
from GSOF_Cockpit.SingleIndicator import SingleIndicator

class AirSpeedMeter(SingleIndicator):
    """Air speed indicator gauge)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h."""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage  = pygame.image.load(os.path.join(path, '../skin/AirSpeedIndicator_Background.png')).convert()
      if handImage == None:
         handImage  = pygame.image.load(os.path.join(path, '../skin/AirSpeedNeedle.png')).convert()
      super().__init__(screen=screen, bodyImage=bodyImage, handImage=handImage,
                       pos=pos, size=size,
                       #initVal     = initVal,
                       inputGain   = 1.0,        #< Input scaling is applied before offeset
                       inputOffset = 0.0,        #< Input offeset is added to input value afterscale factor
                       kp          = 0.8,        #< Filter coefficiant (0-no filter)

                       inputToDeg = -360.0/1000, #< Input value to degrees factor applied after offset
                       offset_deg = 180,         #< Input offeset is added to input value before scale factor
                       minMax_deg = None,        #< Indicator angle min/max (deg)
                       modulu_deg = 360,         #< Modulu for indicator angle (deg)
                      )
