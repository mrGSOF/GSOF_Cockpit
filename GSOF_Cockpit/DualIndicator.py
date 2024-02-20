## DualIndicator.py
## 
## Created on: 28 Mar 2017
## Author:     Guy Soffer

import math, os
import pygame
from GSOF_Cockpit import Dial_base

class DualIndicator(Dial_base.Dial):
   """
   Generic Dual-Indicator dial (Like Altmeter).
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList={}, coefList={}):
      """
      Initialise dial at x,y.
      Default size of 300px can be overidden using w,h.
      """
      self.valA = 0
      self.valB = 0
      if bool(imgList) == False:
         path = os.path.dirname(__file__)
         imgList['Frame'] = pygame.image.load(os.path.join(path, 'resources/Altimeter_Background.png'))
         imgList['IndA']  = pygame.image.load(os.path.join(path, 'resources/LongNeedleAltimeter.png'))
         imgList['IndB']  = pygame.image.load(os.path.join(path, 'resources/SmallNeedleAltimeter.png'))
         self.marks = False
      self.frameImage = imgList['Frame'].convert()
      self.A_Ind = imgList['IndA'].convert()
      self.B_Ind = imgList['IndB'].convert()
      self.marks = False
      if 'Mark' in imgList:
         self.marks = imgList['Mark'].convert()
      super().__init__(screen, self.A_Ind, self.frameImage, pos, size)

      if bool(coefList) == False:
         self.A_DegModulu = 360
         self.B_DegModulu = 360
         self.A_DegOffset = 0
         self.B_DegOffset = 0
         self.A_to_Deg = 1.0
         self.B_to_Deg = 1.0
         self.A_MinMax = None
         self.B_MinMax = None
         self.A_Kp = 1
         self.B_Kp = 1
      else:
         self.A_MinMax = coefList['A_MinMax']
         self.B_MinMax = coefList['B_MinMax']
         self.A_to_Deg = coefList['A_ToDeg']
         self.B_to_Deg = coefList['B_ToDeg']
         self.A_Kp = coefList['A_Kp']
         self.B_Kp = coefList['B_Kp']
         self.A_DegModulu = coefList['A_DegModulu']
         self.B_DegModulu = coefList['B_DegModulu']
         self.A_DegOffset = coefList['A_DegOffset']
         self.B_DegOffset = coefList['B_DegOffset']
         
   def update(self, valA, valB):
      self.valA += (valA -self.valA)*self.A_Kp
      self.valB += (valB -self.valB)*self.B_Kp
      
      valA = self.valA
      valB = self.valB

      if self.A_MinMax != None:
         Min, Max = self.A_MinMax
         if (valA > Max):
             valA = Max 
         if (valA < Min):
             valA = Min 

      if self.B_MinMax != None:
         Min, Max = self.B_MinMax
         if (valB > Max): 
             valB = Max
         if (valB < Min): 
             valB = Min
             
      angleA = valA * self.A_to_Deg
      angleB = valB * self.B_to_Deg
      
      self.angleX = math.fmod(angleA, self.A_DegModulu)
      self.angleX += self.A_DegOffset
         
      self.angleY = math.fmod(angleB, self.B_DegModulu)
      self.angleY += self.B_DegOffset

   def draw(self):
       """
       Called to draw a Turn Coordinator dial.
       "angleX" and "angleY" are the inputs.
       "screen" is the surface to draw the dial on.       
       """
       angleX = int(self.angleX)
       angleY = int(self.angleY)
      #If the Needle is not centered in the skin-file. We can compensate for that. 
#       tmpImage = self.clip(self.A_Ind, 0, 0, 0, 0, 0, 0)
#       tmpImage = self.rotate(tmpImage, angleX)
       tmpImage = self.rotate(self.A_Ind, angleX)
       self.overlay(self.frameImage, 0,0)
       self.overlay(tmpImage, 0, 0)
       #tmpImage = self.clip(self.marks, 0, 0, 0, 0, 0, 0)
       #self.overlay(tmpImage, 0, 80)

      #If the Needle is not centered in the skin-file. We can compensate for that. 
#       tmpImage = self.clip(self.B_Ind, 0, 0, 0, 0, 0, 0)
#       tmpImage = self.rotate(tmpImage, angleY)
       tmpImage = self.rotate(self.B_Ind, angleY)
       self.overlay(tmpImage, 0, 0)
       self.dial.set_colorkey(0xFFFF00)
       self.screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
