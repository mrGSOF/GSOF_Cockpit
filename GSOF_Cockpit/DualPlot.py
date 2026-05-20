## Created on: 28 Mar 2017
## Author:     Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.Input import InputX
from GSOF_Cockpit.GraphicsLib import getSurface, scale, blit, drawLine, imageLoad, setTransparentColor, overlayColor
from GSOF_Cockpit.Pygame_Colors import *

class DualPlot(Gauge):
   """
   Generic Real-Time Dual-Plots.
   """
   def __init__(self, screen, pos=(0,0), size=(75,120),
                bodyImage=None,
                topMargin=10, leftMargin=10, botMargin=10, rightMargin=10,
                #topMargin=50, leftMargin=50, botMargin=50, rightMargin=50,
                style        = 'dot', # 'filled', 'line'
                colors       = (RED, GREEN),
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
      #self.margins = (topMargin, leftMargin, botMargin, rightMargin)
      self.colors = colors
      self.style = style
      if bodyImage == None:
         path = os.path.dirname(__file__)
         bodyImage = imageLoad(os.path.join(path, 'skin/Frame_Rect.png'))
      super().__init__(screen, scale(bodyImage, size), pos, size)

      # Total size of ploting area
      top,left, w,h = self._dial.get_rect()
      self.top     = top +topMargin
      self.left    = left +leftMargin
      self.bottom  = top +h -botMargin
      self.right   = left +w -rightMargin
      self.height  = self.bottom -self.top

      # Middle and height values for each plot
      self.heightPlot  = self.height/2
      self.middlePlot1 = (1/4)*self.height +self.top
      self.middlePlot2 = (3/4)*self.height +self.top
      self.middles = (self.middlePlot1, self.middlePlot2)
      self.scanPos = self.left

      print(top, left, top +h, left +w )
      print(self.top, self.left, self.bottom, self.right )
     
      A_phyToPlot = self.height / (A_MinMax[1] -A_MinMax[0])
      A_plotZero =  A_phyToPlot*(A_MinMax[1] +A_MinMax[0])/2
      
      B_phyToPlot = self.height / (B_MinMax[1] -B_MinMax[0])
      B_plotZero =  B_phyToPlot*(B_MinMax[1] +B_MinMax[0])/2

      self.plots = [InputX(initVal=A_initVal, offset=A_Offset, gain=A_Gain, kp=1.0, toAu=A_phyToPlot/2, offset_au=A_plotZero, minMax_au=(-h/2, h/2), modulu_au=None),
                    InputX(initVal=B_initVal, offset=B_Offset, gain=B_Gain, kp=1.0, toAu=B_phyToPlot/2, offset_au=B_plotZero, minMax_au=(-h/2, h/2), modulu_au=None)
                   ]
       
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
       if self.scanPos > self.right:
          self.scanPos = self.left
       scanPos = self.scanPos

       drawLine(self._dial, 0xFFFFFF, (scanPos, self.top),   (scanPos, self.bottom), 4) #< Draw the cursor as vertical line
       drawLine(self._dial, 0x222222, (scanPos-1,self.top), (scanPos-1,self.bottom), 4) #< Clear the points of the previous plot   

       for plot, middle, color in zip(self.plots, self.middles, self.colors):
          val = plot.pos_au
          if self.style == 'dot':
             drawLine(self._dial, color, (scanPos-1, middle -val*0.98), (scanPos-1, middle -val), 4) #< Draw dot plot
          else:
             drawLine(self._dial, color, (scanPos-1, middle -val), (scanPos-1, middle), 4)  #< Draw line plot
          
          drawLine(self._dial, color, (self.left, middle), (self.right, middle)) #< Draw center line

       self._overlay(self._body, 0,0)
       setTransparentColor(self._dial, overlayColor)
       blit( self._screen, self._dial, self.pos )
 
