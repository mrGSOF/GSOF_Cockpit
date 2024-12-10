## Created on: 2/Dec 2024
## Author    : Guy Soffer

from GSOF_Cockpit.DualIndicator import DualIndicator

class AltMeter(DualIndicator):
    """Dual indicator altitude gauge)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handAImage=None, handBImage=None):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h."""
      super().__init__(screen=screen, bodyImage=bodyImage, handAImage=handAImage, handBImage=handBImage,
                       pos=pos, size=size,
                       #initVal     = initVal,
                       inputGain   = 1.0,        #< Input scaling is applied before offeset
                       inputOffset = 0.0,        #< Input offeset is added to input value afterscale factor
                       kp          = 1.0,        #< Filter coefficiant (0-no filter)

                       inputAtoDeg = -360.0/1000, #< Input value to degrees factor applied after offset
                       offsetA_deg = 0,           #< Input offeset is added to input value before scale factor
                       minMaxA_deg = None,        #< Indicator angle min/max (deg)
                       moduluA_deg = 360,         #< Modulu for indicator angle (deg)

                       inputBtoDeg = -36.0/1000,  #< Input value to degrees factor applied after offset
                       offsetB_deg = 0,           #< Input offeset is added to input value before scale factor
                       minMaxB_deg = None,        #< Indicator angle min/max (deg)
                       moduluB_deg = 360          #< Modulu for indicator angle (deg)
                      )
