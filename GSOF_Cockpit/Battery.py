## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math, os, pkg_resources
import pygame
from GSOF_Cockpit import SingleIndicator
   
class Battery(SingleIndicator.SingleIndicator):
   """Battery dial"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, legendImage=None, iconImage=None, handImage=None,
                inputOffset = 0,
                kp          = 0.8,
                minMax_deg  = (-135,135),
                offset_deg  = +135,
                inputToDeg  = 1,
                modulu_deg  = 360):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/Indicator_Background.png'))
      if legendImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/ledgend.png'))
      if handImage == None:
         handImage = pygame.image.load(os.path.join(path, 'resources/AirSpeedNeedle.png'))
      if iconImage == None:
         iconImage = pygame.image.load(os.path.join(path, 'resources/battery2.png'))

      super().__init__(screen, pos, size,
                       bodyImage   = bodyImage,
                       handImage   = handImage,
                       inputOffset = inputOffset,
                       kp          = kp,
                       inputToDeg  = inputToDeg,
                       offset_deg  = offset_deg,
                       minMax_deg  = minMax_deg,
                       modulu_deg  = modulu_deg)
      self.setIcon(iconImage=iconImage, x=0, y=100)      
