## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math, os, pkg_resources
import pygame
from GSOF_Cockpit import SingleIndicator as SI
   
class Battery(SI.SingleIndicator):
   """Battery dial"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                handImage=None, bodyImage=None, iconImage=None, legendImage=None,
                degMinMax   = (-135,135),
                degOffset   = +135,
                inputToDeg  = 1,
                inputOffset = 0,
                degModulu   = 360,
                kp          = 0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/Indicator_Background.png'))
      if legendImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/ledgend.png'))
      if handImage == None:
         handImage = pygame.image.load(os.path.join(path, 'resources/AirSpeedNeedle.png'))
      if iconImage == None:
         self.icon = pygame.image.load(os.path.join(path, 'resources/battery2.png'))
      else:
         self.icon = iconImage

      super().__init__(screen, pos, size,
                       handImage   = handImage,
                       bodyImage   = bodyImage,
                       degMinMax   = degMinMax,
                       degOffset   = degOffset,
                       inputToDeg  = inputToDeg,
                       inputOffset = inputOffset,
                       degModulu   = degModulu,
                       kp          = kp)

   def draw(self):
      """Draw a Battery dial"""
      super().draw( (self.icon, 0, 100) )
