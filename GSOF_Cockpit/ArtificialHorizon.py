## Created on: 28 Mar 2017
## Author    : Guy Soffer

import os
import pygame
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.GraphicsLib import InputXY, clip, rotate
class ArtificialHorizon(Gauge):
    """Artificial horizon dial"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                 bodyImage=None, ballImage=None, birdImage=None,
                 rollOffset = 0.0,    #< Input offeset is added to input value afterscale factor
                 rollToDeg  = 1.0,    #< Input scaling is applied before offeset
                 rollKp     = 0.5,    #< Filter coefficiant (0-no filter)

                 pitchOffset = 0.0,    #< Input offeset is added to input value afterscale factor
                 pitchToDeg  = 1.0,    #< Input scaling is applied before offeset
                 pitchKp     = 0.5):   #< Filter coefficiant (0-no filter)
       """Artificial horizon gauge. Default size of 300px can be overidden using w,h"""
       path = os.path.dirname(__file__)
       if bodyImage == None:
            bodyImage = pygame.image.load(os.path.join(path, 'resources/Horizon_Background.png')).convert()

       if ballImage == None:
           ballImage = pygame.image.load(os.path.join(path, 'resources/Horizon_GroundSky.png')).convert()

       if birdImage == None:
           birdImage = pygame.image.load(os.path.join(path, 'resources/Maquette_Avion.png')).convert()

       super().__init__(screen,
                        bodyImage = bodyImage,
                        pos=pos, size=size)
       self.setIcon(birdImage, x=0, y=0)
       self.inXY = InputXY(initValX=0, offsetX=rollOffset,  gainX=1, kpX=rollKp,  toAuX=rollToDeg,  offsetX_au=0, minMaxX_au=None, moduluX_au=360,
                           initValY=0, offsetY=pitchOffset, gainY=1, kpY=pitchKp, toAuY=pitchToDeg, offsetY_au=0, minMaxY_au=None, moduluY_au=360)
       self._ball = ballImage
       
    def update(self, roll, pitch):
        """Update the artificial horizon dial with roll and pitch angles"""
        self.inXY.update(valX=roll, valY=pitch) #< Filter the inputs
        if (self.inXY.inX.pos_au > 180):
            self.inXY.inX.pos_au -= 360 

        pitch = self.inXY.inY.pos_au
        if (pitch > 90)and(pitch < 270):
            pitch = 180 - pitch 
        elif (pitch > 270):
            pitch -= 360
        self.inXY.inY.pos_au = pitch

    def draw(self, draw=True):
        """Called to draw an Artificial horizon dial"""
        roll  = int(self.inXY.inX.pos_au)
        pitch = int(self.inXY.inY.pos_au)
        tmpBall = clip(self._ball, 0, (59-pitch)*720/180, 250, 250)  #< Pitch
        tmpBall = rotate(tmpBall, roll)                              #< Roll
        self._overlay(tmpBall, 0, 0)
        self._overlay(self._body, 0,0)
        if self._icon != None:
            self._overlay(self._icon ,self._iconX ,self._iconY)      #< Overlay the bird icon on gauge
        self._dial.set_colorkey(0xFFFF00)
        if draw == True:
            self._screen.blit( pygame.transform.scale(self._dial,(self.w,self.h)), self.pos )
