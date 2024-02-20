#!/usr/bin/python
"""
 * TurnCoordinator.py
 * 
 * Created on: 28 Mar 2017
 * Author:     Guy Soffer
 * 
 *      Copyright (C) 2017 Guy Soffer
 *      This Python module is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

 *      Thanks to Duncan Law for implementing and sharing the original code.
 *      Thanks to Chootair at http://www.codeproject.com/Members/Chootair 
 *      for the artwork that this code is based on.
 *      His full work is intended for C# and can be found here:
 *      http://www.codeproject.com/KB/miscctrl/Avionic_Instruments.aspx
"""


import math, pkg_resources
import pygame
from GSOF_Cockpit import Dial_base

class TurnCoord(Dial_base.Dial):
   """
   Turn Coordinator dial.
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList=False, coefList=False):
      """
      Initialise dial at x,y
      Default size of 300px can be overidden using w,h
      """
      self.TurnRate = 0
      self.SideAcc = 0
      if coefList == False:
         self.turnRateDeg_MinMax = (-45,45)
         self.slipDeg_MinMax = (-14,14)
         self.TurnRate_to_Deg = 1.0
         self.SideAcc_to_Deg = 1.0
         self.TurnKp = 1
         self.SideAccKp = 1
      else:
         self.turnRateDeg_MinMax = coefList['TurnRateDegMinMax']
         self.slipDeg_MinMax = coefList['SlipDegMinMax']
         self.TurnRate_to_Deg = coefList['TurnRateToDeg']
         self.SideAcc_to_Deg = coefList['SlipToDeg']
         self.TurnKp = coefList['Turn_Kp']
         self.SideAccKp = coefList['SideAcc_Kp']

      if imgList == False:
         self.image = pygame.image.load(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinatorAircraft.png')).convert()
         self.frameImage = pygame.image.load(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinator_Background.png')).convert()
         self.marks = pygame.image.load(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinatorMarks.png')).convert()
         self.ball = pygame.image.load(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinatorBall.png')).convert()
      else:
         self.image = pygame.image.load(imgList['TurnInd']).convert()
         self.frameImage = pygame.image.load(imgList['Frame']).convert()
         self.marks = pygame.image.load(imgList['Mark']).convert()
         self.ball = pygame.image.load(imgList['SlipInd']).convert()
      super().__init__(screen, self.image, self.frameImage, pos, size)

   def update(self, TurnRate, SideAcc):
      self.TurnRate += (TurnRate -self.TurnRate)*self.TurnKp
      self.SideAcc += (SideAcc -self.SideAcc)*self.SideAccKp
      TurnRate = self.TurnRate
      SideAcc = self.SideAcc

      angleX = TurnRate*self.TurnRate_to_Deg
      angleY = SideAcc*self.SideAcc_to_Deg

      Min, Max = self.turnRateDeg_MinMax
      if (angleX > Max):
          angleX = Max 
      if (angleX < Min):
          angleX = Min
          
      Min, Max = self.slipDeg_MinMax
      if (angleY > Max): 
          angleY = Max
      if (angleY < Min): 
          angleY = Min
          
      self.angleX = angleX
      self.angleY = angleY

   def draw(self):
      """
      Called to draw a Turn Coordinator dial
      "angleX" and "angleY" are the inputs
      "screen" is the surface to draw the dial on       
      """
      angleX = int(self.angleX)
      angleY = int(self.angleY)
      tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -12)
      tmpImage = self.rotate(tmpImage, angleX)
      self.overlay(self.frameImage, 0,0)
      self.overlay(tmpImage, 0, 0)
      tmpImage = self.clip(self.marks, 0, 0, 0, 0, 0, 0)
      self.overlay(tmpImage, 0, 80)
      tmpImage = self.clip(self.ball, 0, 0, 0, 0, 0, 300)
      tmpImage = self.rotate(tmpImage, angleY)
      self.overlay(tmpImage, 0, -220)
      self.dial.set_colorkey(0xFFFF00)
      self.screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
