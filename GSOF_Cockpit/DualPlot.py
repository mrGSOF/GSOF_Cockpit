## Created on: 28 Mar 2017
## Author:     Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.Input import InputX
from GSOF_Cockpit.GraphicsLib import getSurface, scale, blit, drawLine, imageLoad, setTransparentColor

class DualPlot(Gauge):
   """
   Generic Real-Time Dual-Plots.
   """
   def __init__(self, screen, pos=(0,0), size=(75,120),
                bodyImage=None,
                topMargin=10, leftMargin=10, botMargin=10, rightMargin=10,
                A_initVal    = 0.0,
                A_MinMax     = (-1, 1),
                A_Offset     = 0.0,
                A_Gain       = 1.0,
                A_PlotOffset = 0.0,
                A_kp         = 1.0,
                B_initVal    = 0.0,
                B_MinMax     = (-1, 1),
                B_Offset     = 0.0,
                B_Gain       = 1.0,
                B_PlotOffset = 0.0,
                B_kp         = 1.0
):
      """
      Initialise dial at x,y.
      Default size of 300px can be overridden using w,h.
      """
      self.margins = (topMargin, leftMargin, botMargin, rightMargin)
      x,y=pos
      w,h=size
      self.scanPos = 0.0
      A_phyToPlot = h / (A_MinMax[1] -A_MinMax[0])
      A_plotZero =  A_phyToPlot*(A_MinMax[1] +A_MinMax[0])/2
      
      B_phyToPlot = h / (B_MinMax[1] -B_MinMax[0])
      B_plotZero =  B_phyToPlot*(B_MinMax[1] +B_MinMax[0])/2

      self.plots = [InputX(initVal=A_initVal, offset=A_Offset, gain=A_Gain, kp=1.0, toAu=A_phyToPlot, offset_au=A_plotZero, minMax_au=(-h/2, h/2), modulu_au=None),
                   InputX(initVal=B_initVal, offset=B_Offset, gain=B_Gain, kp=1.0, toAu=B_phyToPlot, offset_au=B_plotZero, minMax_au=(-h/2, h/2), modulu_au=None)
                   ]
      if bodyImage == None:
         path = os.path.dirname(__file__)
         bodyImage = imageLoad(os.path.join(path, 'skin/Frame_Rect.png'))
      super().__init__(screen, bodyImage, pos, size)
       
   def update(self, *inputs, scanPos=None):
       """
       Update and plots with new values     
       """
       for plot, val in zip(self.plots, inputs):
              plot.update(val)
       self.scanPos += 0.1
       if scanPos != None:
          self.scanPos = scanPos

   def draw(self):
       """
       Draw the most updated representation of the dial     
       """
       #The drawing area in the gauge
       top,left, h,w = self._dial.get_rect()
       topMargin, leftMargin, botMargin, rightMargin = self.margins
       top    = top +topMargin
       left   = left +leftMargin
       bottom = top +h -botMargin
       right  = left +w -rightMargin
       height = bottom -top
       middle = height/2 +top

       if self.scanPos > right:
          self.scanPos = 0
       scanPos = self.scanPos

       for plot in self.plots:
          val = plot.pos_au
       

       drawLine(self._dial, 0xFFFFFF, (scanPos,top),   (scanPos,bottom), 4)   #< Draw cursor as vertical line
       drawLine(self._dial, 0x222222, (scanPos-1,top), (scanPos-1,bottom), 4)

       drawLine(self._dial, 0x00FFFF, (scanPos-1,middle -val*0.98), (scanPos-1, middle -val*1.02), 4) #< Draw dotplot on first half
       #drawLine(self._dial, 0x00FFFF, (scanPos-1,middle-val), (scanPos-1,middle), 4)  #< Draw line plot on first half
       #drawLine(self._dial, 0xFF00FF, (scanPos-1,bottom-valB), (scanPos-1,bottom), 4) #< Draw on second half
       
       drawLine(self._dial, 0xFFFF00, (scanPos-1,middle), (scanPos-1,middle)) #< Draw center line

       self._overlay(self._body, 0,0)

       setTransparentColor(self._dial, 0xFFFF00)
       blit( self._screen, scale(self._dial,(self.w,self.h)), self.pos )
 
