## SinglePlot.py
## 
## Created on: 28 Mar 2017
## Author:     Guy Soffer

import math, os
import pygame
from GSOF_Cockpit import SingleIndicator as SI
   
class SinglePlot(SI.SingleIndicator):
   """
   Generic Real-Time-Plot.
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList={}, coefList={}):
      """
      Initialise dial at x,y.
      Default size of 300px, can be overidden using w,h.
      """
      x,y=pos
      w,h=size
      self.inputA = 0
      self.scanPos = 0
      
      self.image = pygame.Surface((0,0))
      if bool(coefList) == False:
         self.A_MinMax = (60,240)
         self.A_Offset = 150
         self.A_In_to_Out = -1.0
         self.A_In_Offset = 0
         self.Scan_Region = (30,120)
      else:
         self.A_MinMax = coefList['A_MinMax']
         self.A_Offset = coefList['A_Offset']
         self.A_In_to_Out = coefList['A_InToOut']
         self.A_In_Offset = coefList['A_InOffset']
         self.Scan_Region = coefList['Scan_Region']

      if bool(imgList) == False:
         path = os.path.dirname(__file__)
         imgList['Frame'] = pygame.image.load(os.path.join(path, 'resources/RF_Dial_Background.png'))
      self.frameImage = imgList['Frame'].convert() #Frame of dial
      super(SI.SingleIndicator, self).__init__(screen, self.image, self.frameImage, pos, size)
       
   def update(self, inputA, scanPos):
       """Update and gauge values"""
       self.inputA = inputA
       self.scanPos = scanPos

   def draw(self):
      """Draw the updated gauge"""
      inputA = (self.inputA +self.A_In_Offset)*self.A_In_to_Out +self.A_Offset 
      scanPos = self.scanPos
      Min, Max = self.A_MinMax
      if inputA > Max:
         inputA = Max
      elif inputA < Min:
         inputA = Min

      top = self.dial.get_rect()[0] +60
      left = self.dial.get_rect()[1] +30
      bottom = self.dial.get_rect()[0] + self.dial.get_rect()[2] -60
      right = self.dial.get_rect()[1] + self.dial.get_rect()[3] -30
      height = bottom - top
      middle = height/2 + top
      scanPos %= right -30
      scanPos += 30
        
      #inputA %= 100
      inputA = height * inputA / 200
      
      #The tracing line (Current position)
      pygame.draw.line(self.dial, 0xFFFFFF, (scanPos,top), (scanPos,bottom), 1)     #Erase line
      pygame.draw.line(self.dial, 0x222222, (scanPos-1,top), (scanPos-1,bottom), 1) #Mark line

      pygame.draw.line(self.dial, 0x00FFFF, (scanPos-1,inputA), (scanPos-1,middle),4)
      pygame.draw.line(self.dial, 0xFFFF00, (scanPos-1,middle), (scanPos-1,middle))

      self.overlay(self.frameImage, 0,0)

      self.dial.set_colorkey(0xFFFF00)
      self.screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
