## Created on: 25 Jan 2025
## Author    : Guy Soffer

import os
import pygame
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.GraphicsLib import drawOnScreen, blit, scale, initFont, fillSurface
from GSOF_Cockpit.Pygame_Colors import *
  
CYAN1 = (128,255,255)

class DotMatrixDisplay(Gauge):
    def __init__(self, screen, bodyImage, pos, size, bgColor, pxColor, rows=8, cols=21):
        super().__init__(screen, bodyImage, pos, size)
        self.cols = cols
        self.rows = rows

        scaleX = int(size[0]/(cols*6 +2))
        scaleY = int(size[1]/(rows*8))
        self.scale = scaleX if scaleX<scaleY else scaleY

        self.xOfs = 1*self.scale
        self.yOfs = 0
        
        #self.disp = pygame.display.set_mode( (self.dispX, self.dispY) )
        initFont() # you have to call this at the start, 
                   # if you want to use this module.
        self.fontSize =int(7*self.scale)
        path = os.path.dirname(__file__)
        font = os.path.join(path, "lcd-5x7-segment-monospace.ttf")
        #self.font   = pygame.freetype.SysFont("Comic Sans MS", 5*scale)
        self.font   = pygame.font.Font(font, self.fontSize)
        self.fontX2 = pygame.font.Font(font, self.fontSize*2)
        self.color = CYAN1
        self.backlight = BLACK

        self.cls()

    def _text_objects(self, text, font):
        textSurface = font.render(text, True, self.color)
        return textSurface, textSurface.get_rect()

    def cls(self):
        fillSurface(self._dial, self.backlight)

##    def clrLine(self, row):
##        orgX = 0
##        endX = self.w
##        orgY = row*8*self.scale
##        endY = 8*self.scale
##        self.disp.fill(self.backlight, rect=(orgX, orgY, endX, endY))

    def printAt(self, x, y, s, clrLine=False, X2=False):
        if X2:
            scale = 2*self.scale
            font = self.fontX2
        else:
            scale = self.scale
            font = self.font

#        if (clrLine == True):
#            self.clrLine(y)
        
        if (clrLine == True):
            orgX = self.xOfs
            endX = self.dispX
        else:#if (clrLine == False):
            orgX = self.xOfs +x*6*self.scale
            endX = len(s)*6*scale

        #orgY = self.yOfs +y*8*self.scale
        #endY = 8*scale
        #self.cls()
        TextSurf, TextRect = self._text_objects(s, font)

        #TextRect.centerx += self.xOfs +x*6*self.scale
        #TextRect.centery += self.yOfs +y*8*self.scale
        blit(self._dial, TextSurf, (x*6.0*self.scale, y*8*self.scale))
        
    def printCenter(self, row, s, clrLine=True):
        x = int((self.cols -len(s))/2)
        if clrLine:
            self.clrLine(row)
        self.PrintAt(x, row, s)

    def printLeft(self, row, s, clrLine=False):
        self.PrintAt(0, row, s, clrLine=clrLine)

    def printRight(self, row, s, clrLine=False):
        x = self.cols -len(s)
        if clrLine:
            self.PrintAt(0, row, ' '*x)
            self.Print(s)
        else:
            self.PrintAt(x, row, s)

    def printBmpAt(self, bmp, x, y):
        bmp = scale(bmp, (int(bmp.get_width()*self.scale),
                                           int(bmp.get_height()*self.scale)))
        blit(self._dial, bmp,(self.xOfs +x*self.scale, self.yOfs +y*8*self.scale))

##    def draw(self, draw=True):
##        self.cls()
##        super().draw(draw=True)
##        self._overlay(self.scr, 0,0)
##        if draw == True:
##            drawOnScreen(self._screen, self._dial, (self.w, self.h), self.pos )
        

