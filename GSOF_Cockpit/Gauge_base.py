## Created on: 2 / Dec 2024
## Author    : Guy Soffer

import math
import pygame
from GSOF_Cockpit import GraphicsLib as Lib

class Gauge():
   """Generic gauge with single input variable"""
   def __init__(self, screen, bodyImage, pos=(0,0), size=(0,0), iconImage=None ):
      """
      pos = Position of top left corner of the dial (x,y)
      size = Width and height of dial (w,h)
      """
      self._screen = screen
      self._body   = bodyImage.convert()
      self._dial   = pygame.Surface(self._body.get_rect()[2:4])
      self._icon   = iconImage
      self._dial.fill(0xFFFF00)

      self.x, self.y = pos
      self.w, self.h = size
      if self.w == 0:
         self.w = self._body.get_rect()[2]
      if self.h == 0:
         self.h = self._body.get_rect()[3]

      self.pos = self._dial.get_rect()
      self.pos = self.pos.move( *pos )

   def setIcon(self, iconImage, x, y):
      self._icon  = iconImage
      self._iconX = x
      self._iconY = y
      return self
   
   def setPosition(self, x, y) -> None:
       """Reposition top,left of dial at x,y"""
       self.x = x 
       self.y = y
       self.pos[0] = x
       self.pos[1] = y

   def positionCenter(self, x, y) -> None:
       """Reposition centre of dial at x,y"""
       self.x = x
       self.y = y
       self.pos[0] = x - self.pos[2]/2
       self.pos[1] = y - self.pos[3]/2

   def _overlay(self, image, x, y, r=0) -> None:
       """Overlays one image on top of another using 0xFFFF00 (Yellow) as the overlay color"""
       x -= (image.get_rect()[2] - self._dial.get_rect()[2])/2
       y -= (image.get_rect()[3] - self._dial.get_rect()[3])/2
       image.set_colorkey(0xFFFF00)
       self._dial.blit(image, (x,y))

   def draw(self, draw=True):
      self._overlay(self._body, 0,0)                         #< Overlay body on dial
      if self._icon != None:
         self._overlay(self._icon ,self._iconX ,self._iconY) #< Overlay icon on dial at x,y
      if draw == True:
         Lib.drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos)
