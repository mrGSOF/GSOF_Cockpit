## Created on: 28 Mar 2017
## Author:     Guy Soffer


import math, os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import getSurface, scale, blit, drawLine

class DualPlot(SingleIndicator):
   """
   Generic Real-Time Dual-Plots.
   """
   def __init__(self, screen, pos=(0,0), size=(0,0), imgList={}, coefList={}):
      """
      Initialise dial at x,y.
      Default size of 300px can be overidden using w,h.
      """
      x,y=pos
      w,h=size
      self.inputA = 0
      self.inputB = 0
      self.scanPos = scanPos

      self.image = getSurface((0,0))
      if bool(coefList) == False:
         self.A_MinMax = (75,120)
         self.A_Offset = 75
         self.A_In_to_Out = 1
         self.A_In_Offset = 0

         self.B_MinMax = (30,75)
         self.B_Offset = 30
         self.B_In_to_Out = 1
         self.B_In_Offset = 0

         self.Scan_Region = (30,120)
      else:
         self.A_MinMax = coefList['A_MinMax']
         self.A_Offset = coefList['A_Offset']
         self.A_In_to_Out = coefList['A_InToOut']
         self.A_In_Offset = coefList['A_InOffset']

         self.B_MinMax = coefList['A_MinMax']
         self.B_Offset = coefList['A_Offset']
         self.B_In_to_Out = coefList['A_InToOut']
         self.B_In_Offset = coefList['A_InOffset']

         self.Scan_Region = coefList['Scan_Region']

      if bool(imgList) == False:
         path = os.path.dirname(__file__)
         imgList['Frame'] = imageLoad(os.path.join(path, 'resources/RF_Dial_Background.png'))
      self.frameImage = imgList['Frame'].convert() #Frame of dial
      super(SingleIndicator).__init__(screen, self.image, self._bodyImage, pos, size)
       
   def update(self, inputA, inputB, scanPos):
       """
       Update and step the internal model machine       
       """
       self.inputA = inputA
       self.inputB = inputB
       self.scanPos = scanPos

   def draw(self):
       """
       Draw the most updated representation of the dial     
       """
       #Fatch the latest data from the model
       inputA = self.inputA
       inputB = self.inputB
       scanPos = self.scanPos
       
       top = self._dial.get_rect()[0] +60
       left = self._dial.get_rect()[1] +30
       bottom = self._dial.get_rect()[0] + self._dial.get_rect()[2] -60
       right = self._dial.get_rect()[1] + self._dial.get_rect()[3] -30
       height = bottom - top
       middle = height/2 + top

       scanPos %= right -30
       scanPos += 30
       inputA %= 100
       inputB %= 100
       inputA = height * inputA / 200
       inputB = height * inputB / 200

       drawLine(self._dial, 0xFFFFFF, (scanPos,top), (scanPos,bottom), 1)
       drawLine(self._dial, 0x222222, (scanPos-1,top), (scanPos-1,bottom), 1)

       drawLine(self._dial, 0x00FFFF, (scanPos-1,middle-inputA), (scanPos-1,middle),4)
       drawLine(self._dial, 0xFF00FF, (scanPos-1,bottom-inputB), (scanPos-1,bottom),4)
       drawLine(self._dial, 0xFFFF00, (scanPos-1,middle), (scanPos-1,middle))

       self._overlay(self._body, 0,0)

       setTtransparentColor(self._dial, 0xFFFF00)
       blit( self._screen, scale(self._dial,(self.w,self.h)), self.pos )
 
