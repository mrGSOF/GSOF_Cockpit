## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math, os
import pygame
from GSOF_Cockpit import Dial_base
   
class SingleIndicator(Dial_base.Dial):
   """Dial gauge with single hand (niddle)"""
   def __init__(self, screen, pos=(0,0), size=(0,0), handImage=None, bodyImage=None,
                degMinMax = (-135,135),
                degOffset   = +135,
                inputToDeg  = 1,
                inputOffset = 0,
                degModulu   = 360,
                kp          = 0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if handImage == None:
         handImage = pygame.image.load(os.path.join(path, 'resources/AirSpeedNeedle.png'))
      if bodyImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/Indicator_Background.png'))
      super().__init__(screen, handImage, bodyImage, pos, size)
      self.Deg_MinMax = degMinMax
      self.Deg_Offset = degOffset
      self.Deg_Modulu = degModulu
      self.offset     = inputOffset #< input offset
      self.toDeg      = inputToDeg  #< Input to degrees
      self.Kp         = kp
      self.inVal      = 0
      self.update(self.inVal)
       
   def update(self, val):
      """Update the angle of the indicator's hand"""
      self.inVal += (val -self.inVal)*self.Kp
      angleX = (self.inVal +self.offset)*self.toDeg

      Min, Max = self.Deg_MinMax
      if angleX > Max:
         angleX = Max
      elif angleX < Min:
         angleX = Min

      angleX = math.fmod(angleX, self.Deg_Modulu)
      angleX += self.Deg_Offset
      self.angleX = angleX

   def draw(self, iconLayer = None):
      """Draw a indicator"""
      self._overlay(self._body, 0,0)                           #< Overlay on the body
      if iconLayer != None:
         self._overlay(iconLayer[0],iconLayer[1],iconLayer[2]) #< Overlay an icon in x,y
      hand = Dial_base.rotate(self._hand, int(self.angleX))    #< Rotate the hand
      self._overlay(hand, 0, 0)                                #< Overlay hand on body 
      self._dial.set_colorkey(0xFFFF00)
      self._screen.blit( pygame.transform.scale(self._dial,(self.w,self.h)), self.pos )
