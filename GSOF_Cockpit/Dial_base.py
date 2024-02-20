## Dial_base.py
## 
## Created on: 28 Mar 2017
## Author:     Guy Soffer

import math
import pygame

class Dial():
   """Generic gauge"""
   def __init__(self, screen, image, frameImage, pos=(0,0), size=(0,0) ):
      """
      pos = Position of top left corner of the dial (x,y)
      size = Width and height of dial (w,h)
      """
      self.screen = screen
      self.image = image
      self.frameImage = frameImage
      self.dial = pygame.Surface(self.frameImage.get_rect()[2:4])
      self.dial.fill(0xFFFF00)

      self.x, self.y = pos
      self.w, self.h = size
      if self.w == 0:
         self.w = self.frameImage.get_rect()[2]
      if self.h == 0:
         self.h = self.frameImage.get_rect()[3]

      self.pos = self.dial.get_rect()
      self.pos = self.pos.move( *pos )
      self.angleX = 0
      self.angleY = 0

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

   def rotate(self, image, angle):
       """
       Rotate supplied image by "angle" degrees
       This rotates round the centre of the image
       If you need to offset the centre, resize the image using self.clip
       This is used to rotate dial needles and probably doesn't need to be used externally
       """
       tmpImage = pygame.transform.rotate(image ,angle)
       imageCentreX = tmpImage.get_rect()[0] +tmpImage.get_rect()[2]/2
       imageCentreY = tmpImage.get_rect()[1] +tmpImage.get_rect()[3]/2

       targetWidth = tmpImage.get_rect()[2]
       targetHeight = tmpImage.get_rect()[3]

       imageOut = pygame.Surface((targetWidth, targetHeight))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(tmpImage,
                     (0,0),
                     pygame.Rect(imageCentreX -targetWidth/2,
                                 imageCentreY -targetHeight/2,
                                 targetWidth,
                                 targetHeight
                                 )
                     )
       return imageOut

   def clip(self, image, x=0, y=0, w=0, h=0, oX=0, oY=0):
       """
       Cuts out a part of the needle image at x,y position to the correct size (w,h)
       This is put on to "imageOut" at an offset of oX,oY if required
       This is used to center the indicators inside the gauge frame
       """
       if w == 0:
           w = image.get_rect()[2]
       if h == 0:
           h = image.get_rect()[3]
           
       needleW = w +2*math.sqrt(oX*oX)
       needleH = h +2*math.sqrt(oY*oY)
       imageOut = pygame.Surface((needleW, needleH))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(image, (needleW/2 -w/2 +oX, needleH/2 -h/2 +oY), pygame.Rect(x,y,w,h))
       return imageOut

   def overlay(self, image, x, y, r=0):
       """Overlays one image on top of another using 0xFFFF00 (Yellow) as the overlay color"""
       x -= (image.get_rect()[2] - self.dial.get_rect()[2])/2
       y -= (image.get_rect()[3] - self.dial.get_rect()[3])/2
       image.set_colorkey(0xFFFF00)
       self.dial.blit(image, (x,y))
