## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math
import pygame

class SingleInput():
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

   def position(self, x, y):
       """Reposition top,left of dial at x,y"""
       self.x = x 
       self.y = y
       self.pos[0] = x
       self.pos[1] = y

   def position_center(self, x, y):
       """Reposition centre of dial at x,y"""
       self.x = x
       self.y = y
       self.pos[0] = x - self.pos[2]/2
       self.pos[1] = y - self.pos[3]/2

   def _overlay(self, image, x, y, r=0):
       """Overlays one image on top of another using 0xFFFF00 (Yellow) as the overlay color"""
       x -= (image.get_rect()[2] - self._dial.get_rect()[2])/2
       y -= (image.get_rect()[3] - self._dial.get_rect()[3])/2
       image.set_colorkey(0xFFFF00)
       self._dial.blit(image, (x,y))
