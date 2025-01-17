## Created on: 17/Dec 2024
## Author    : Guy Soffer

import os
from GSOF_Cockpit.Input import Hand
from GSOF_Cockpit.GraphicsLib import rotate, drawOnScreen, getMouse, imageLoad
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.Button import Button_Round
from GSOF_Cockpit import Pygame_Colors as COLOR

class GMeter_Analog(SingleIndicator):
    """G-Meter gauge with minimum/maximum markers and reset button"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handImage=None, minMaxHandImage=None):
      """Initialise gauge"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage  = imageLoad(os.path.join(path, '../skin/G_Meter.png'))
      if handImage == None:
         handImage  = imageLoad(os.path.join(path, '../skin/G_Meter_Ind.png'))
      super().__init__(screen, pos=pos, size=size,
                       bodyImage   = bodyImage,
                       handImage   = handImage,
                       inputOffset = 9.8,
                       kp          = 0.8,
                       inputToDeg  = 4.6,
                       offset_deg  = 90,
                       minMax_deg  = (-270,270),
                       modulu_deg  = 270)

      if minMaxHandImage == None:
         minMaxImage  = imageLoad(os.path.join(path, '../skin/Alt_Meter200_S_Needle.png'))
      self._minHand = Hand(
                           initVal     = 0.0,
                           offset      = 0.0,
                           gain        = 1.0,
                           kp          = 1.0,
                           offset_deg  = 135,
                           toDeg       = 4.6,
                           minMax_deg  = (-270, 270),
                           modulu_deg  = 270,
                           skin        = minMaxImage
                           )
      self._maxHand = Hand(
                           initVal     = 0.0,
                           offset      = 0.0,
                           gain        = 1.0,
                           kp          = 1.0,
                           offset_deg  = 135,
                           toDeg       = 4.6,
                           minMax_deg  = (-270, 270),
                           modulu_deg  = 270,
                           skin        = minMaxImage
                           )
      self.resetG()
      self.rstBtn = Button_Round( screen=screen,
                            pos=(pos[0] +10, pos[1] +118), size=(25,25),
                            funcPressed=self.resetG,
                            color=COLOR.RED, textColor=COLOR.WHITE,
                            name="R" )

##      self.rstBtn = Button_Empty( screen=screen,
##                            pos=(pos[0] +12, pos[1] +120), size=(30,30),
##                            funcPressed=self.resetG)

    def update(self, val):
        """Update the angle of the indicator's hand"""
        minG = self.minG
        maxG = self.maxG
        if minG > val:
            minG = val
            self._minHand.update(minG)
            self.minG = minG
            self._minMaxChg = True
        elif maxG < val:
            maxG = val
            self._maxHand.update(maxG)
            self.maxG = maxG
            self._minMaxChg = True
        super().update(val)
        
    def resetG(self, Min=0.0, Max=0.0):
        ###print("G Meter reset")
        self.minG = Min
        self.maxG = Max
        self._minMaxChg = True
        
    def _drawMinMaxMarks(self, draw=True):
        if self._minMaxChg == True:
            self.__minHand = rotate(self._minHand.skin, int(self._minHand.angle_deg)) #< Rotate the minimum mark
            self.__maxHand = rotate(self._maxHand.skin, int(self._maxHand.angle_deg)) #< Rotate the maximum mark
            self._minMaxChg = False
        self._overlay(self.__minHand, 0, 0)                                           #< Overlay hand on body 
        self._overlay(self.__maxHand, 0, 0)                                           #< Overlay hand on body 
        if draw == True:
            drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos )

    def draw(self, draw=True):
        super().draw(draw=False)         #< Draw the gauge
        self._drawMinMaxMarks(draw)      #< Draw the min/max markers
        self.rstBtn.action( getMouse() ) #< Check for button action and draw the button
