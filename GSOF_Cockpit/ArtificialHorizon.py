## ArticifialHorizon.py
##
## Created on: 28 Mar 2017
## Author:     Guy Soffer

import math, os
import pygame
from GSOF_Cockpit import Dial_base

class ArtificialHorizon(Dial_base.Dial):
   """
   Artificial horizon dial.
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList={}, coefList={}):
      """
      Initialise dial at x,y.
      Default size of 300px can be overidden using w,h.
      """
      self.roll = 0
      self.pitch = 0
      if bool(coefList) == False:
         self.rollToDeg   = 1
         self.rollOffset  = 0
         self.pitchToDeg  = 1
         self.pitchOffset = 0
         self.Kp = 0
      else:
         self.rollToDeg   = coefList['RollToDeg']
         self.rollOffset  = coefList['RollOffset']
         self.pitchToDeg  = coefList['PitchToDeg']
         self.pitchOffset = coefList['PitchOffset']
         self.Kp = coefList['Kp']

      if bool(imgList) == False:
         path = os.path.dirname(__file__)
         imgList['Frame'] = pygame.image.load(os.path.join(path, 'resources/Horizon_Background.png'))
         imgList['Ball']  = pygame.image.load(os.path.join(path, 'resources/Horizon_GroundSky.png'))
         imgList['Bird']  = pygame.image.load(os.path.join(path, 'resources/Maquette_Avion.png'))
      self.image = imgList['Ball'].convert()
      self.frameImage = imgList['Frame'].convert()
      self.maquetteImage = imgList['Bird'].convert()
      super().__init__(screen, self.image, self.frameImage, pos, size)
       
   def update(self, roll, pitch):
      """
      Called to step the Artificial horizon dial.
      "Roll-Angle" and "Pitch-Angle" are the inputs.
      """
      ## Filter the input
      self.roll += (roll -self.roll)*self.Kp
      self.pitch += (pitch -self.pitch)*self.Kp

      roll = (self.roll +self.rollOffset)*self.rollToDeg
      pitch = (self.pitch +self.pitchOffset)*self.pitchToDeg

      roll %= 360
      pitch %= 360
      if (roll > 180):
         roll -= 360 
      if (pitch > 90)and(pitch < 270):
         pitch = 180 - pitch 
      elif (pitch > 270):
         pitch -= 360

      self.angleX = roll
      self.angleY = pitch

   def draw(self):
      """
      Called to draw an Artificial horizon dial.
      """
      roll = int(self.angleX)
      pitch = int(self.angleY)
      tmpImage = self.clip(self.image, 0, (59-pitch)*720/180, 250, 250)
      tmpImage = self.rotate(tmpImage, roll)
      self.overlay(tmpImage, 0, 0)
      self.overlay(self.frameImage, 0,0)
      self.overlay(self.maquetteImage, 0,0)
      self.dial.set_colorkey(0xFFFF00)
      self.screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
