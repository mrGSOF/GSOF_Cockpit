## Created on: 23 Dec 2024
## Author:     Guy Soffer

import os
from GSOF_Cockpit.DualIndicator import DualIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad

class Heading(DualIndicator):
    """Turn heading gauge"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                 bodyImage=None, wheelImage=None, needleImage=None,
                 inputOffset = 0.0,
                 kp          = 0.8,
                 inputToDeg  = 1.0,
                 offset_deg  = 0.0,
                ):
        path = os.path.dirname(__file__)
        if bodyImage   == None:
            bodyImage   = imageLoad(os.path.join(path, '../skin/HeadingIndicator_Background.png'))
        if wheelImage  == None:
            wheelImage  = imageLoad(os.path.join(path, '../skin/HeadingWheel.png'))
        if needleImage == None:
            needleImage = imageLoad(os.path.join(path, '../skin/AirSpeedNeedle.png'))

        super().__init__( screen, pos=pos, size=size,
                         bodyImage   = bodyImage,
                         handAImage  = wheelImage,
                         handBImage  = needleImage,
                         inputOffset = inputOffset,
                         kp          = kp,
                         inputGain   = 1.0,
                         inputAtoDeg = inputToDeg,
                         offsetA_deg = offset_deg,
                         minMaxA_deg = None,
                         moduluA_deg = 360,
                         inputBtoDeg = inputToDeg,
                         offsetB_deg = offset_deg,
                         minMaxB_deg = None,
                         moduluB_deg = 360
                        )

    def update(self, val, valB=None):
        """Update the angle of two hands"""
        super().update(val, -(valB -val))
