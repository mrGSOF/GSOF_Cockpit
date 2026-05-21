## Created on: 20 May 2026
## Author:     Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.Input import InputX
from GSOF_Cockpit.GraphicsLib import getSurface, scale, blit, drawLine, imageLoad, setTransparentColor, overlayColor
from GSOF_Cockpit.Pygame_Colors import *

class Plot_base(Gauge):
   """Base class for Real-Time plots"""
   def __init__(self, screen, pos, size,
                bodyImage,
                topMargin, leftMargin, botMargin, rightMargin,
                style, #'dot', 'filled', 'line'
                colors,
               ):
      """Initialise plot"""
      self.colors = colors
      self.style = style
      if bodyImage == None:
         path = os.path.dirname(__file__)
         bodyImage = imageLoad(os.path.join(path, 'skin/Frame_Rect.png'))
      super().__init__(screen, scale(bodyImage, size), pos, size)

      self._calcPlotArea(topMargin, leftMargin, botMargin, rightMargin)

      self.scanPos = self.left
      self.middles = []
      self.plots = []

   def _calcPlotArea(self, topMargin, leftMargin, botMargin, rightMargin):
      # Total size of ploting area
      top,left, w,h = self._dial.get_rect()
      self.top     = top +topMargin
      self.left    = left +leftMargin
      self.bottom  = top +h -botMargin
      self.right   = left +w -rightMargin
      self.height  = self.bottom -self.top
      
   def update(self, *inputs, scanPos=None):
       """Update and plots with new values"""
       for plot, val in zip(self.plots, inputs):
              plot.update(val)
       self.scanPos += 0.1
       if scanPos != None:
          self.scanPos = scanPos

   def draw(self):
       """Draw the most updated representation of the dial"""
       #The drawing area in the gauge
       if self.scanPos > self.right:
          drawLine(self._dial, overlayColor, (self.scanPos-1,self.top), (self.scanPos-1,self.bottom), 4)
          self.scanPos = self.left
       scanPos = self.scanPos

       drawLine(self._dial, 0xFFFFFF, (scanPos, self.top),   (scanPos, self.bottom), 4) #< Draw the cursor as vertical line
       drawLine(self._dial, overlayColor, (scanPos-1,self.top), (scanPos-1,self.bottom), 4) #< Clear the points of the previous plot   

       for plot, middle, color in zip(self.plots, self.middles, self.colors):
          val = plot.pos_au
          if self.style == 'dot':
             drawLine(self._dial, color, (scanPos-1, middle -val*0.98), (scanPos-1, middle -val), 4) #< Draw dot plot
          else:
             drawLine(self._dial, color, (scanPos-1, middle -val), (scanPos-1, middle), 4)  #< Draw line plot
          
          drawLine(self._dial, GRAY, (self.left, middle), (self.right, middle)) #< Draw center line

       self._overlay(self._body, 0,0)
       setTransparentColor(self._dial, overlayColor)
       blit( self._screen, self._dial, self.pos )
       
class Plot(Plot_base):
   """Generic Real-Time plot"""
   def __init__(self, screen, pos=(0,0), size=(75,120),
                bodyImage=None,
                topMargin=10, leftMargin=10, botMargin=10, rightMargin=10,
                style        = 'dot', # 'filled', 'line'
                colors       = (RED, GREEN),
                A_initVal    = 0.0,
                A_MinMax     = (-1, 1),
                A_Offset     = 0.0,
                A_Gain       = 1.0,
                A_PlotOffset = 0.0,
                A_kp         = 1.0,
               ):
      """Initialise plot"""
      super().__init__(screen, pos, size, bodyImage,
                       topMargin, leftMargin, botMargin, rightMargin,
                       style, colors)

      # Middle and height values for each plot
      plots = len(colors)
      middlePlot = 0.5*self.height +self.top
      self.middles = [middlePlot]*plots

      A_phyToPlot = self.height / (A_MinMax[1] -A_MinMax[0])
      A_plotZero =  A_phyToPlot*(A_MinMax[1] +A_MinMax[0])

      h = self.height/2
      for i in range(0,plots):
         self.plots.append(
            InputX(initVal=A_initVal, offset=A_Offset, gain=A_Gain, kp=1.0, toAu=A_phyToPlot, offset_au=A_plotZero, minMax_au=(-h, h), modulu_au=None))
 
