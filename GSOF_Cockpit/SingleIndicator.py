## Generic_base.py
## 
## Created on: 28 Mar 2017
## Author:     Guy Soffer

import math, os
import pygame
from GSOF_Cockpit import Dial_base
   
class SingleIndicator(Dial_base.Dial):
   """
   Dial gauge with single niddle.
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList={}, coefList={}):
      """
      Initialise dial at x,y
      Default size of 300px can be overidden using w,h
      """
      self.screen = screen
      self.inVal = 0
      if bool(coefList) == False:
         self.Deg_MinMax = (0,360)
         self.Deg_Offset = 0
         self.Deg_Modulu = 360
         self.In_to_Deg = 1
         self.In_Offset = 0
         self.Kp = 1
      else:
         self.Deg_MinMax = coefList['DegMinMax']
         self.Deg_Offset = coefList['DegOffset']
         self.Deg_Modulu = coefList['DegModulu']
         self.In_Offset = coefList['InOffset']
         self.In_to_Deg =  coefList['InToDeg']
         self.Kp = coefList['Kp']

      if bool(imgList) == False:
         path = os.path.dirname(__file__)
         imgList['Ind'] = pygame.image.load(os.path.join(path, 'resources/AirSpeedNeedle.png'))
         imgList['Frame'] = pygame.image.load(os.path.join(path, 'resources/Indicator_Background.png'))
      self.image = imgList['Ind'].convert()
      self.frameImage = imgList['Frame'].convert()
      super().__init__(screen, self.image, self.frameImage, pos, size)
       
   def update(self, inVal):
      self.inVal += (inVal -self.inVal)*self.Kp
      angleX = (self.inVal +self.In_Offset)*self.In_to_Deg

      Min, Max = self.Deg_MinMax
      if angleX > Max:
         angleX = Max
      elif angleX < Min:
         angleX = Min

      angleX = math.fmod(angleX, self.Deg_Modulu)
      angleX += self.Deg_Offset
      self.angleX = angleX

   def draw(self, iconLayer=0):
      """
      Called to draw a Generic dial
      "angleX" and "angleY" are the inputs
      "screen" is the surface to draw the dial on
      """
      angleX = int(self.angleX)
      #If the Needle is not centered in the skin-file. We can compensate for that. 
#      tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -35)
#      tmpImage = self.rotate(tmpImage, angleX)
      tmpImage = self.rotate(self.image, angleX)
      self.overlay(self.frameImage, 0,0)
      if iconLayer:
         self.overlay(iconLayer[0],iconLayer[1],iconLayer[2])
      self.overlay(tmpImage, 0, 0)
      self.dial.set_colorkey(0xFFFF00)
      self.screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
