## Created on: 25 Dec 2024
## Author    : Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.Input import Hand #, InputXYZ
from GSOF_Cockpit.GraphicsLib import imageLoad, rotate, scale, drawOnScreen
  
class Map(Gauge):
    """Locate and rotate a marker on background image (map)"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                 bodyImage=None, mapImage=None, markerImage=None,
                 inputXY_minMax=(-10,10),
                 mapXY_minMax = (-100, -100),
                 inputToDeg = 1.0,
                 offset_deg = 0.0,
                 kp       = 0.8):
        path = os.path.dirname(__file__)
        if bodyImage == None:
            bodyImage = imageLoad(os.path.join(path, '../skin/Frame_Rect.png'))
        if mapImage  == None:
            mapImage  = imageLoad(os.path.join(path, '../skin/Grid_BackgroundWhite.png'))
        if markerImage == None:
            markerImage = imageLoad(os.path.join(path, '../skin/Aircraft_Top.png'))

        super().__init__(screen, bodyImage, pos, size)
        self.setIcon(mapImage, x=0, y=0)
        inputToMapX = mapXY_minMax[0]/inputXY_minMax[0]
        inputToMapY = mapXY_minMax[1]/inputXY_minMax[1]
        
        self._marker = Hand(
                            initVal     = 0.0,
                            offset      = 0.0,
                            gain        = -1.0,
                            kp          = kp,
                            offset_deg  = offset_deg,
                            toDeg       = inputToDeg,
                            minMax_deg  = None,
                            modulu_deg  = 360,
                            skin        = markerImage
                           )

    def update(self, x, y, deg=0):
        """Update the position and angle of the marker"""
        self.posX, self.posY = x,y
        self._marker.update(deg)

    def draw(self, draw=True):
        """Draw the map and marker"""
        if self._icon != None:
            self._overlay(self._icon ,self._iconX ,self._iconY)         #< Overlay icon on dial at x,y
        self._overlay(self._body, 0,0)                                  #< Overlay body on dial

        marker = rotate(self._marker.skin, int(self._marker.angle_deg)) #< Rotate the hand
        self._overlay(marker, self.posX, self.posY)                     #< Overlay hand on body 
        if draw == True:
            drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos )
