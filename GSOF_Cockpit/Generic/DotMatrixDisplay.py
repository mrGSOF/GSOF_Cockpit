## Created on: 25 Jan 2025
## Author    : Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.GraphicsLib import (
    blit,
    fillSurface,
    getSurface,
    initFont,
    getFont,
    renderText,
)
from GSOF_Cockpit.Pygame_Colors import *

CYAN1 = (128, 255, 255)


class DotMatrixDisplay(Gauge):
    def __init__(self, screen, bodyImage, pos, size, bgColor, pxColor, rows=8, cols=21):
        super().__init__(screen, bodyImage, pos, size)
        self.cols = cols
        self.rows = rows

        scaleX = int(size[0] / (cols * 6 + 2))
        scaleY = int(size[1] / (rows * 8))
        self.scale = scaleX if scaleX < scaleY else scaleY

        self.ofsX = 1 * self.scale
        self.ofsY = 0

        initFont()  # you have to call this at the start,
        # if you want to use this module.
        self.fontSize = int(7 * self.scale)
        path = os.path.dirname(__file__)
        font = os.path.join(path, "lcd-5x7-segment-monospace.ttf")
        # self.font   = getSysFont("Comic Sans MS", self.fontSize)
        self.font = getFont(font, self.fontSize)
        self.fontX2 = getFont(font, self.fontSize * 2)
        self.color = CYAN1
        self.backlight = BLACK
        self.chrSizeX = 6 * self.scale
        self.chrSizeY = 8 * self.scale
        self.cls()

    def _text_objects(self, string, font):
        text = renderText(string, font, self.color)
        surf = getSurface((text.get_width(), text.get_height()))
        fillSurface(surf, self.backlight)
        blit(surf, text, (0, 0))
        return surf

    def cls(self):
        fillSurface(self._dial, self.backlight)

    def clrLine(self, row):
        self.printAt(col=0, row=row, s=" " * self.cols)

    def printAt(self, col, row, s, X2=False):
        x, y = col, row
        if X2:
            scale = 2 * self.scale
            font = self.fontX2
        else:
            scale = self.scale
            font = self.font

        TextSurf = self._text_objects(s, font)
        blit(
            self._dial,
            TextSurf,
            (self.ofsX + x * self.chrSizeX, self.ofsY + y * self.chrSizeY),
        )

    def printCenter(self, row, s, clrLine=True):
        x = int((self.cols - len(s)) / 2)
        if clrLine:
            self.clrLine(row)
        self.printAt(x, row, s)

    def printLeft(self, row, s, clrLine=False):
        if clrLine:
            self.clrLine(row)
        self.printAt(0, row, s)

    def printRight(self, row, s, clrLine=False):
        x = self.cols - len(s)
        if clrLine:
            self.printAt(0, row, " " * x + s)
        else:
            self.printAt(x, row, s)

    def printBmpAt(self, bmp, x, y):
        bmp = scale(
            bmp, (int(bmp.get_width() * self.scale), int(bmp.get_height() * self.scale))
        )
        blit(
            self._dial, bmp, (self.ofsX + x * self.scale, self.ofsY + y * self.chrSizeY)
        )
