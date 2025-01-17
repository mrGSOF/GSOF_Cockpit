## Created on: 9 Dec 2024
## Author    : Guy Soffer

import os
from GSOF_Cockpit.DualIndicator import DualIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad
  
class SetPointVsFeedbackFill(DualIndicator):
   """Percentage dial with fill mark and maximum rabge of 180 degrees"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, setPointImage=None, feedbackImage=None,
                inputGain = 1.0,
                inputOffset = 0.0,
                inputMin = 0,
                inputMax = 100,
                kp       = 0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = imageLoad(os.path.join(path, '../resources/EngineIndicator_Background.png'))
      if setPointImage == None:
         setPointImage = imageLoad(os.path.join(path, '../resources/EngineIndicator_Needle.png'))
      if feedbackImage == None:
         feedbackImage = imageLoad(os.path.join(path, '../resources/AirSpeedNeedle.png'))

      super().__init__(screen, pos, size,
                       bodyImage   = bodyImage,
                       handAImage  = setPointImage,
                       handBImage  = feedbackImage,
                       inputGain   = inputGain,
                       inputOffset = inputOffset,
                       kp          = kp,

                       offsetA_deg = 0,
                       inputAtoDeg = -180/(inputMax-inputMin),
                       minMaxA_deg = (-180, 0),

                       offsetB_deg = 180,
                       inputBtoDeg = -180/(inputMax-inputMin),
                       minMaxB_deg = (-180, 180))

class SetPointVsFeedback(DualIndicator):
   """Percentage dial with needle and full turn range (360 degree)"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, setPointImage=None, feedbackImage=None,
                inputGain = 1.0,
                inputOffset = 0.0,
                inputMin = 0,
                inputMax = 100,
                kp       = 0.8):
      """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
      path = os.path.dirname(__file__)
      if bodyImage == None:
         bodyImage = imageLoad(os.path.join(path, '../resources/EngineIndicator_Background.png'))
      if setPointImage == None:
         setPointImage = imageLoad(os.path.join(path, '../resources/EngineIndicator_Needle.png'))
      if feedbackImage == None:
         feedbackImage = imageLoad(os.path.join(path, '../resources/AirSpeedNeedle.png'))

      super().__init__(screen, pos, size,
                       bodyImage   = bodyImage,
                       handAImage  = setPointImage,
                       handBImage  = feedbackImage,
                       inputGain   = inputGain,
                       inputOffset = inputOffset,
                       kp          = kp,

                       inputAtoDeg = -180/(inputMax-inputMin),
                       offsetA_deg = 180,
                       minMaxA_deg = (-180, 0),

                       inputBtoDeg = -180/(inputMax-inputMin),
                       offsetB_deg = 180,
                       minMaxB_deg = (-180, 0))
