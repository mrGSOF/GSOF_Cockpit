## Generic.py
 
## Created on: 28 Mar 2017
## Author:     Guy Soffer

import math, os, pkg_resources
import pygame
from GSOF_Cockpit import SingleIndicator as SI
   
class Battery(SI.SingleIndicator):
   """
   Battery dial.
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList={}, coefList={}):
      """
      Initialise dial at x,y.
      Default size of 300px can be overidden using w,h.
      """
      if bool(coefList) == False:
         coefList={'DegMinMax':(-135,135),
                  'DegOffset':+135,
                  'InToDeg':1,
                  'InOffset':0,
                  'DegModulu':360}
         
      if bool(imgList) == False:
         path = os.path.dirname(__file__)
         self.icon = pygame.image.load(os.path.join(path, 'resources/battery2.png'))
         ind = pygame.image.load(os.path.join(path, 'resources/AirSpeedNeedle.png'))
         frame = pygame.image.load(os.path.join(path, 'resources/Indicator_Background.png'))
         super().__init__(screen, pos, size,
                          imgList={'Ind':ind, 'Frame':frame},
                          coefList=coefList
                          )
         self.frameImage = pygame.image.load(os.path.join(path, 'resources/ledgend.png')).convert()
      else:
         self.icon = imgList['Icon'].convert()         #Icon of dial
         super().__init__(screen, pos, size, imgList=imgList, coefList=coefList) #Frame & Indicator if dial
         self.frameImage = imgList['Legend'].convert() #Marks of dial
      
   def draw(self):
      """
      Called to draw a Battery dial.
      """
      super().draw( (self.icon, 0, 100) )
