## Created on: 2/Dec 2024
## Author    : Guy Soffer
import os, pygame
from GSOF_Cockpit.SingleIndicator import SingleIndicator

class VsiMeter(SingleIndicator):
    """Vertical velocity gauge"""
    def __init__(self, screen, pos=(0,0), size=(0,0),
                 bodyImage=None, handImage=None,
                 inputToDeg=25, offset_deg=90,minMax_deg=(-90,270), kp=0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h."""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage  = pygame.image.load(os.path.join(path, '../skin/VerticalSpeedIndicator_Background.png')).convert()
      if handImage == None:
         handImage  = pygame.image.load(os.path.join(path, '../skin/VerticalSpeedNeedle.png')).convert()
      super().__init__(screen=screen, pos=pos, size=size,
                       bodyImage=bodyImage,
                       handImage=handImage,
                       inputOffset = 0,
                       kp          = kp,
                       inputToDeg  = inputToDeg,
                       offset_deg  = offset_deg,
                       minMax_deg  = minMax_deg,
                       modulu_deg  = 360
                      )
