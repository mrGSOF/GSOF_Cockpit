## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math, os
import pygame
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit import Dial_base

class DualIndicator(SingleIndicator):
   """Dual-Indicator dial (Like Altmeter)"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, handAImage=None, handBImage=None,
                initVal     = 0.0,
                inputGain   = 1.0,
                inputOffset = 0.0,
                kp          = 0.8,
                inputAtoDeg = 1,
                inputBtoDeg = 1/10,
                offsetA_deg = 0.0,
                offsetB_deg = 0.0,
                minMaxA_deg = (-360,0),
                minMaxB_deg = (-360,0),
                moduluA_deg = 360,
                moduluB_deg = 360):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h."""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage  = pygame.image.load(os.path.join(path, 'resources/Altimeter_Background.png'))
      if handAImage == None:
         handAImage = pygame.image.load(os.path.join(path, 'resources/LongNeedleAltimeter.png'))
      super().__init__(screen=screen, bodyImage=bodyImage, handImage=handAImage,
                       pos=pos, size=size,
                       initVal     = initVal,
                       inputGain   = inputGain,
                       inputOffset = inputOffset,
                       kp          = kp,
                       inputToDeg  = inputAtoDeg,
                       offset_deg  = offsetA_deg,
                       minMax_deg  = minMaxA_deg,
                       modulu_deg  = moduluA_deg)
      if handBImage == None:
         handBImage = pygame.image.load(os.path.join(path, 'resources/SmallNeedleAltimeter.png'))
      self._handB = Dial_base.Hand(
                                   initVal     = initVal,
                                   offset      = inputOffset,
                                   gain        = inputGain,
                                   kp          = kp,
                                   offset_deg  = offsetB_deg,
                                   toDeg       = inputBtoDeg,
                                   minMax_deg  = minMaxB_deg,
                                   modulu_deg  = moduluB_deg,
                                   skin        = handBImage
                                   )

##      if marksImage != None:
##         self._marks = marksImage.convert()
##      else:
##         self._marks = False

##      self.valA       = 0
##      self.minMaxA    = aMinMax
##      self.toDegA     = aToDeg
##      self.kpA        = kpA
##      self.degModuluA = aDegModulu
##      self.degOffsetA = aDegOffset
##
##      self.val        = 0
##      self.minMaxB    = bMinMax
##      self.toDegB     = bToDeg
##      self.bpB        = kpB
##      self.degModuluB = bDegModulu
##      self.degOffsetB = bDegOffset

   def update(self, val, valB=None):
      super().update(val)
##      self.valA += (valA -self.valA)*self.A_Kp
##      self.valB += (valB -self.valB)*self.B_Kp
##      
##      valA = self.valA
##      valB = self.valB
##
##      if self.A_MinMax != None:
##         Min, Max = self.A_MinMax
##         if (valA > Max):
##             valA = Max 
##         if (valA < Min):
##             valA = Min 
##
##      if self.B_MinMax != None:
##         Min, Max = self.B_MinMax
##         if (valB > Max): 
##             valB = Max
##         if (valB < Min): 
##             valB = Min
##             
##      angleA = valA * self.A_to_Deg
##      angleB = valB * self.B_to_Deg
##      
##      self.angleX = math.fmod(angleA, self.A_DegModulu)
##      self.angleX += self.A_DegOffset
##         
##      self.angleY = math.fmod(angleB, self.B_DegModulu)
##      self.angleY += self.B_DegOffset

   def draw(self):
       """
       Called to draw a Turn Coordinator dial.
       "angleX" and "angleY" are the inputs.
       "screen" is the surface to draw the dial on.       
       """
       super().draw()
##       angleX = int(self.angleX)
##       angleY = int(self.angleY)
##      #If the Needle is not centered in the skin-file. We can compensate for that. 
###       tmpImage = self.clip(self.A_Ind, 0, 0, 0, 0, 0, 0)
###       tmpImage = self.rotate(tmpImage, angleX)
##       tmpImage = self.rotate(self.A_Ind, angleX)
##       self.overlay(self.frameImage, 0,0)
##       self.overlay(tmpImage, 0, 0)
##       #tmpImage = self.clip(self.marks, 0, 0, 0, 0, 0, 0)
##       #self.overlay(tmpImage, 0, 80)
##
##      #If the Needle is not centered in the skin-file. We can compensate for that. 
###       tmpImage = self.clip(self.B_Ind, 0, 0, 0, 0, 0, 0)
###       tmpImage = self.rotate(tmpImage, angleY)
##       tmpImage = self.rotate(self.B_Ind, angleY)
##       self.overlay(tmpImage, 0, 0)
##       self.dial.set_colorkey(0xFFFF00)
##       self._screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
