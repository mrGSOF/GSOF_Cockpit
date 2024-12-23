## Created on: 2/Dec 2024
## Author    : Guy Soffer
import os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad

class AirSpeedMeter(SingleIndicator):
    """Air speed indicator gauge)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None,
                minAngle=-180, maxAngle=180,
                maxSpeed=1000, kp=0.8): 
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h."""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage  = imageLoad(os.path.join(path, '../skin/AirSpeedIndicator_Background.png'))
      if handImage == None:
         handImage  = imageLoad(os.path.join(path, '../skin/AirSpeedNeedle.png'))
      super().__init__(screen=screen, bodyImage=bodyImage, handImage=handImage,
                       pos=pos, size=size,
                       #initVal     = initVal,
                       inputGain   = 1.0,        #< Input scaling is applied before offeset
                       inputOffset = 0.0,        #< Input offeset is added to input value afterscale factor
                       kp          = kp,         #< Filter coefficiant (0-no filter)

                       inputToDeg = -(maxAngle-minAngle)/maxSpeed, #< Input value to degrees factor applied after offset
                       offset_deg = minAngle,                      #< Input offeset is added to input value before scale factor
                       minMax_deg = None,                          #< Indicator angle min/max (deg)
                       modulu_deg = 360,                           #< Modulu for indicator angle (deg)
                      )
