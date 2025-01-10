## Created on: 2/Dec 2024
## Author    : Guy Soffer
import os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad

def poly(coef, at):
    y=0
    x=1
    for c in coef:
        y += c*x
        x *= at
    return y

class MachMeter(SingleIndicator):
    """Mach gauge"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None,
                minAngle=5, maxAngle=355,
                maxMach=1.5, kp=0.8): 
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h."""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage  = imageLoad(os.path.join(path, '../skin/Mach_Meter_Body.png'))
      if handImage == None:
         handImage  = imageLoad(os.path.join(path, '../skin/Mach_Meter_Needle.png'))
      self.coef = (5.0, -309.667, +874.0, -485.333, +96.0)
      super().__init__(screen=screen, bodyImage=bodyImage, handImage=handImage,
                       pos=pos, size=size,
                       #initVal     = initVal,
                       inputGain   = 1.0,        #< Input scaling is applied before offeset
                       inputOffset = 0.0,       #< Input offeset is added to input value afterscale factor
                       kp          = kp,         #< Filter coefficiant (0-no filter)

                       inputToDeg = -1,#(maxAngle-minAngle)/maxMach,  #< Input value to degrees factor applied after offset
                       offset_deg = minAngle,                      #< Input offeset is added to input value before scale factor
                       minMax_deg = (-maxAngle, -minAngle),        #< Indicator angle min/max (deg)
                       modulu_deg = 360,                           #< Modulu for indicator angle (deg)
                      )

    def update(self, val):
        """Update the angle of the indicator's hand"""
        val = poly(self.coef, val)
        super().update(val)
##deg   mach
##  5   0
## 90   0.75
##180   1.0
##270   1.25
##355   1.5

