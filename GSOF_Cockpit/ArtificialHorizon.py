## Created on: 28 Mar 2017
## Author    : Guy Soffer

import math, os
import pygame
from GSOF_Cockpit.Dial_base import Dial_base

class ArtificialHorizon(Dial_base):
   """Artificial horizon dial"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, ballImage=None, birdImage=None,
                rollOffset = 0.0,    #< Input offeset is added to input value afterscale factor
                rollToDeg  = 1.0,    #< Input scaling is applied before offeset
                rollKp     = 0.5,    #< Filter coefficiant (0-no filter)

                pitchOffset = 0.0,    #< Input offeset is added to input value afterscale factor
                pitchToDeg  = 1.0,    #< Input scaling is applied before offeset
                pitchKp     = 0.5)    #< Filter coefficiant (0-no filter)
      """Artificial horizon gauge. Default size of 300px can be overidden using w,h"""
##      self.roll = 0
##      self.pitch = 0
##      if bool(coefList) == False:
##         self.rollToDeg   = 1
##         self.rollOffset  = 0
##         self.pitchToDeg  = 1
##         self.pitchOffset = 0
##         self.Kp = 0
##      else:
##         self.rollToDeg   = coefList['RollToDeg']
##         self.rollOffset  = coefList['RollOffset']
##         self.pitchToDeg  = coefList['PitchToDeg']
##         self.pitchOffset = coefList['PitchOffset']
##         self.Kp = coefList['Kp']

      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = pygame.image.load(os.path.join(path, 'resources/Horizon_Background.png')).convert()

      if ballImage == None:
         ballImage = pygame.image.load(os.path.join(path, 'resources/Horizon_GroundSky.png')).convert()

      if birdImage == None:
         birdImage = pygame.image.load(os.path.join(path, 'resources/Maquette_Avion.png')).convert()

      super().__init__(screen,
                       bodyImage = bodyImage,
                       handAImage = ballImage,
                       handBImage = None,                       
                       pos, size)
       
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
