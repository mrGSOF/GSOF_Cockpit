## Created on: 28 Mar 2017
## Author    : Guy Soffer

import os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.Input import Hand
from GSOF_Cockpit.GraphicsLib import rotate, drawOnScreen, imageLoad

class DualIndicator(SingleIndicator):
    """Dual-Indicator dial (Like Altmeter)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handAImage=None, handBImage=None,
                initVal     = 0.0,
                inputGain   = 1.0,
                inputOffset = 0.0,
                kp          = 0.8,
                inputAtoDeg = -1,
                inputBtoDeg = -1,
                offsetA_deg = 0.0,
                offsetB_deg = 0.0,
                minMaxA_deg = None,
                minMaxB_deg = None,
                moduluA_deg = 360,
                moduluB_deg = 360):
      """Initialise dial at x,y. Default size of 300px can be overridden using w,h."""
      path = os.path.dirname(__file__)
      if handBImage == None:
          handBImage = imageLoad(os.path.join(path, 'resources/SmallNeedleAltimeter.png'))
      self._handB = Hand(
                         initVal     = initVal,
                         offset      = inputOffset,
                         gain        = inputGain,
                         kp          = kp,
                         offset_deg  = offsetB_deg,
                         toDeg       = inputBtoDeg,
                         minMax_deg  = minMaxB_deg,
                         modulu_deg  = moduluB_deg,
                         skin        = handBImage
                         )
      if bodyImage == None:
          bodyImage  = imageLoad(os.path.join(path, 'resources/Altimeter_Background.png'))
      if handAImage == None:
          handAImage = imageLoad(os.path.join(path, 'resources/LongNeedleAltimeter.png'))
      super().__init__(screen=screen, bodyImage=bodyImage, handImage=handAImage,
                       pos=pos, size=size,
                       initVal     = initVal,
                       inputGain   = inputGain,
                       inputOffset = inputOffset,
                       kp          = kp,
                       inputToDeg  = inputAtoDeg,
                       offset_deg  = offsetA_deg,
                       minMax_deg  = minMaxA_deg,
                       modulu_deg  = moduluA_deg)

    def update(self, val, valB=None):
        """Update the angle of two hands"""
        super().update(val)
        SingleIndicator.update(self, val)
        if valB == None:
            valB = val
        self._handB.update(valB)

    def draw(self, draw=True):
        """screen" is the surface to draw the dial on"""
        super().draw(draw=False)

        handB = rotate(self._handB.skin, int(self._handB.angle_deg)) #< Rotate the hand
        self._overlay(handB, 0, 0)                                   #< Overlay hand on body 
        if draw == True:
            drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos )
