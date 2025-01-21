## Created on: 2/Dec 2024
## Author    : Guy Soffer

from GSOF_Cockpit.DualIndicator import DualIndicator
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR

class AltMeter(DualIndicator):
    """Dual indicator altitude gauge)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                digitsColor=COLOR.BLACK,
                bodyImage=None, handAImage=None, handBImage=None):
      """Initialise dial at x,y. Default size of 300px can be overridden using w,h."""
      super().__init__(screen=screen, bodyImage=bodyImage, handAImage=handAImage, handBImage=handBImage,
                       pos=pos, size=size,
                       #initVal     = initVal,
                       inputGain   = 1.0,        #< Input scaling is applied before offset
                       inputOffset = 0.0,        #< Input offset is added to input value afterscale factor
                       kp          = 1.0,        #< Filter coefficient (0-no filter)

                       inputAtoDeg = -360.0/1000, #< Input value to degrees factor applied after offset
                       offsetA_deg = 0,           #< Input offset is added to input value before scale factor
                       minMaxA_deg = None,        #< Indicator angle min/max (deg)
                       moduluA_deg = 360,         #< Modulu for indicator angle (deg)

                       inputBtoDeg = -36.0/1000,  #< Input value to degrees factor applied after offset
                       offsetB_deg = 0,           #< Input offset is added to input value before scale factor
                       minMaxB_deg = None,        #< Indicator angle min/max (deg)
                       moduluB_deg = 360          #< Modulu for indicator angle (deg)
                      )
      self.altitude = 0.0
      self.digitalDisp = Text( screen=screen,
                            pos=(pos[0] +int(size[0]*0.15), pos[1] +int(size[1]*0.44)), size=(int(0.27*size[0]), int(0.14*size[1])),
                            color=None, textColor=digitsColor,
                            name="%d"%self.altitude )

    def update(self, val):
        """Update the angle of two hands"""
        super().update(val, valB=None)
        self.altitude = val

    def draw(self, draw=True):
        super().draw(draw=True)  #< Draw the gauge
        self.digitalDisp.setText("%06d"%int(self.altitude))
        self.digitalDisp.draw()  #< Check for button action and draw the button
