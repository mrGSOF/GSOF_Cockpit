## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math, os
import pygame
from GSOF_Cockpit import Dial_base

class SingleIndicator(Dial_base.Dial):
   """Dial gauge with single hand (niddle)"""
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
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if handImage == None:
         handImage = pygame.image.load(os.path.join(path, 'resources/AirSpeedNeedle.png'))
      if bodyImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/Indicator_Background.png'))
      super().__init__(screen, bodyImage, pos, size)
      self._handA = Dial_base.Hand(
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
      self.update(val=initVal)

   def update(self, val):
      """Update the angle of the indicator's hand"""
      self._handA.update(val)

   def draw(self, iconLayer = None):
      """Draw a indicator"""
      self._overlay(self._body, 0,0)                                        #< Overlay on the body
      if iconLayer != None:
         self._overlay(iconLayer[0] ,iconLayer[1] ,iconLayer[2])            #< Overlay an icon in x,y
      hand = Dial_base.rotate(self._handA.skin, int(self._handA.angle_deg)) #< Rotate the hand
      self._overlay(hand, 0, 0)                                             #< Overlay hand on body 
      self._dial.set_colorkey(0xFFFF00)
      self._screen.blit( pygame.transform.scale( self._dial, (self.w, self.h)), self.pos )
