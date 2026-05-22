## Created on: 28 Mar 2017
## Author    : Guy Soffer

import os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import (
    getSurface,
    setTransparentColor,
    scale,
    drawLine,
    blit,
    imageLoad,
)


class SinglePlot(SingleIndicator):
    """Generic Real-Time-Plot"""

    def __init__(self, screen, pos=(0, 0), size=(0, 0), bodyImage=None, coefList={}):
        """Initialise dial at x,y. Default size of 300px, can be overridden using w,h"""
        x, y = pos
        w, h = size
        self.inputA = 0
        self.scanPos = 0

        self.image = getSurface((0, 0))
        if bool(coefList) == False:
            self.A_MinMax = (60, 240)
            self.A_Offset = 150
            self.A_In_to_Out = -1.0
            self.A_In_Offset = 0
            self.Scan_Region = (30, 120)
        else:
            self.A_MinMax = coefList["A_MinMax"]
            self.A_Offset = coefList["A_Offset"]
            self.A_In_to_Out = coefList["A_InToOut"]
            self.A_In_Offset = coefList["A_InOffset"]
            self.Scan_Region = coefList["Scan_Region"]

        if bodyImage == None:
            path = os.path.dirname(__file__)
            bodyImage = imageLoad(
                os.path.join(path, "resources/RF_Dial_Background.png")
            )
        super().__init__(screen, pos, size, bodyImage)

    def update(self, inputA, scanPos):
        """Update and gauge values"""
        self.inputA = inputA
        self.scanPos = scanPos

    def draw(self):
        """Draw the updated gauge"""
        inputA = (self.inputA + self.A_In_Offset) * self.A_In_to_Out + self.A_Offset
        scanPos = self.scanPos
        Min, Max = self.A_MinMax
        if inputA > Max:
            inputA = Max
        elif inputA < Min:
            inputA = Min

        top = self._dial.get_rect()[0] + 60
        left = self._dial.get_rect()[1] + 30
        bottom = self._dial.get_rect()[0] + self._dial.get_rect()[2] - 60
        right = self._dial.get_rect()[1] + self._dial.get_rect()[3] - 30
        height = bottom - top
        middle = height / 2 + top
        scanPos %= right - 30
        scanPos += 30

        # inputA %= 100
        inputA = height * inputA / 200

        # The tracing line (Current position)
        drawLine(
            surface=self._dial,
            color=0xFFFFFF,
            fromPnt=(scanPos, top),
            toPnt=(scanPos, bottom),
            width=1,
        )  #< Erase line
        drawLine(
            surface=self._dial,
            color=0x222222,
            fromPnt=(scanPos - 1, top),
            toPnt=(scanPos - 1, bottom),
            width=1,
        )  #< Mark line

        drawLine(
            surface=self._dial,
            color=0x00FFFF,
            fromPnt=(scanPos - 1, inputA),
            toPnt=(scanPos - 1, middle),
            width=4,
        )
        drawLine(
            surface=self._dial,
            color=0xFFFF00,
            fromPnt=(scanPos - 1, middle),
            toPnt=(scanPos - 1, middle),
        )

        self._overlay(self._body, 0, 0)

        setTransparentColor(self._dial, 0xFFFF00)
        blit(self._screen, scale(self._dial, (self.w, self.h)), self.pos)
