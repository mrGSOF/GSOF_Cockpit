## Created on: 28 Mar 2017
## Author    : Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.Input import Hand
from GSOF_Cockpit.GraphicsLib import rotate, drawOnScreen, imageLoad

class SingleIndicator(Gauge):
    """Dial gauge with single hand (needle)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None,
                initVal     = 0.0,
                inputGain   = 1.0,
                inputOffset = 0.0,
                kp          = 0.8,
                inputToDeg  = 1,
                offset_deg  = +135,
                minMax_deg  = (-135,135),
                modulu_deg  = 360):
        """Initialise dial at x,y. Default size of 300px can be overridden using w,h"""
        path = os.path.dirname(__file__)
        if handImage == None:
            handImage = imageLoad(os.path.join(path, 'resources/AirSpeedNeedle.png'))
        if bodyImage == None:
            bodyImage = imageLoad(os.path.join(path, 'resources/Indicator_Background.png'))
        super().__init__(screen, bodyImage, pos, size)
        self._handA = Hand(
                           initVal     = initVal,
                           offset      = inputOffset,
                           gain        = inputGain,
                           kp          = kp,
                           offset_deg  = offset_deg,
                           toDeg       = inputToDeg,
                           minMax_deg  = minMax_deg,
                           modulu_deg  = modulu_deg,
                           skin        = handImage
                           )
        SingleIndicator.update(self, val=initVal)

    def update(self, val):
        """Update the angle of the indicator's hand"""
        self._handA.update(val)

    def draw(self, draw=True):
        """Draw a indicator"""
        super().draw(draw=False)                                    #< Draw body and icon
        hand = rotate(self._handA.skin, int(self._handA.angle_deg)) #< Rotate the hand
        self._overlay(hand, 0, 0)                                   #< Overlay hand on body 
        if draw == True:
            drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos )
