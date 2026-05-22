## Created on: 20 May 2026
## Author:     Guy Soffer

import os
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.Input import InputX
from GSOF_Cockpit.GraphicsLib import (
    getSurface,
    scale,
    blit,
    drawLine,
    imageLoad,
    setTransparentColor,
    overlayColor,
)
from GSOF_Cockpit.Pygame_Colors import *
from GSOF_Cockpit.Plot import Plot_base


class DualPlot(Plot_base):
    """Real-Time Dual-Plots"""

    def __init__(
        self,
        screen,
        pos=(0, 0),
        size=(75, 120),
        bodyImage=None,
        topMargin=10,
        leftMargin=10,
        botMargin=10,
        rightMargin=10,
        style="dot",  # 'filled', 'line'
        colors=(RED, GREEN),
        A_initVal=0.0,
        A_MinMax=(-1, 1),
        A_Offset=0.0,
        A_Gain=1.0,
        A_PlotOffset=0.0,
        A_kp=1.0,
        B_initVal=0.0,
        B_MinMax=(-1, 1),
        B_Offset=0.0,
        B_Gain=1.0,
        B_PlotOffset=0.0,
        B_kp=1.0,
    ):
        """Initialise plot"""
        super().__init__(
            screen,
            pos,
            size,
            bodyImage,
            topMargin,
            leftMargin,
            botMargin,
            rightMargin,
            style,
            colors,
        )

        # Total size of ploting area
        top, left, w, h = self._dial.get_rect()
        self.top = top + topMargin
        self.left = left + leftMargin
        self.bottom = top + h - botMargin
        self.right = left + w - rightMargin
        self.height = self.bottom - self.top

        # Middle and height values for each plot
        self.middlePlot1 = (1 / 4) * self.height + self.top
        self.middlePlot2 = (3 / 4) * self.height + self.top
        self.middles = (self.middlePlot1, self.middlePlot2)

        A_phyToPlot = self.height / (A_MinMax[1] - A_MinMax[0])
        A_plotZero = A_phyToPlot * (A_MinMax[1] + A_MinMax[0]) / 2

        B_phyToPlot = self.height / (B_MinMax[1] - B_MinMax[0])
        B_plotZero = B_phyToPlot * (B_MinMax[1] + B_MinMax[0]) / 2

        h = self.height / 4
        self.plots = [
            InputX(
                initVal=A_initVal,
                offset=A_Offset,
                gain=A_Gain,
                kp=1.0,
                toAu=A_phyToPlot / 2,
                offset_au=A_plotZero,
                minMax_au=(-h, h),
                modulu_au=None,
            ),
            InputX(
                initVal=B_initVal,
                offset=B_Offset,
                gain=B_Gain,
                kp=1.0,
                toAu=B_phyToPlot / 2,
                offset_au=B_plotZero,
                minMax_au=(-h, h),
                modulu_au=None,
            ),
        ]
