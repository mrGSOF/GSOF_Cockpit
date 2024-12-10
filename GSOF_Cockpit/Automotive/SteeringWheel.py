## Created on: 10 Mar 2023
## Author:     Guy Soffer

import pkg_resources
import pygame
from GSOF_Cockpit import SingleIndicator as SI

class SteeringWheel(SI.SingleIndicator):
    def __init__(self, screen, pos, size,
                 bodyImage=None, wheelImage=None,
                 inputToDeg = 10.0,
                 offset_deg = 9.8,
                 kp         = 0.8,
                 minMax_deg = (-270,270)
                 ):
        
        if bodyImage == None:
            bodyImage  = pygame.image.load(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/Indicator_Background.png')).convert()
        if wheelImage == None:
            wheelImage = pygame.image.load(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/SteeringWheel.png')).convert()
            
        super().__init__( screen=screen, pos=pos, size=size,
                          bodyImage  = bodyImage,
                          handImage = wheelImage,
                          inputToDeg = inputToDeg,
                          offset_deg = offset_deg,
                          kp         = kp,
                          minMax_deg = minMax_deg)
