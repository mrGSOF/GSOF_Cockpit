## Created on: 25 Dec 2024
## Author    : Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.GraphicsLib import imageLoad
  
class World(Gauge):
    def __init__(self, screen, pos=(0,0), size=(0,0),
                 bodyImage=None, world=None):
        path = os.path.dirname(__file__)
        if bodyImage == None:
            bodyImage = imageLoad(os.path.join(path, '../skin/Frame_Rect.png'))

        super().__init__(screen, bodyImage, pos, size)
        
##        self._world = Hand(
##                          initVal     = 0.0,
##                          offset      = 0.0,
##                          gain        = -1.0,
##                          kp          = kp,
##                          offset_deg  = offset_deg,
##                          toDeg       = inputToDeg,
##                          minMax_deg  = None,
##                          modulu_deg  = 360,
##                          skin        = markImage
##                         )

    def update(self, x=0, y=0, z=0, yaw=0, pitch=0, roll=0):
        """Update the position and attitude angle of 3D world"""
##        self.posX, self.posY = x,y
##        self._mark.update(deg)

##    def draw(self, draw=True):
##        """Draw a indicator"""
##        if self._icon != None:
##            self._overlay(self._icon ,self._iconX ,self._iconY)   #< Overlay icon on dial at x,y
##        self._overlay(self._body, 0,0)                            #< Overlay body on dial
##
##        mark = rotate(self._mark.skin, int(self._mark.angle_deg)) #< Rotate the hand
##        self._overlay(mark, self.posX, self.posY)                 #< Overlay hand on body 
##        if draw == True:
##            drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos )
  
    def draw(self, draw=True):
        super().draw(True)
