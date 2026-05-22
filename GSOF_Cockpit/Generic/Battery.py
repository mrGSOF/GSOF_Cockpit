## Created on: 28 Mar 2017
## Author    : Guy Soffer

import os
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad


class Battery(SingleIndicator):
    """Battery dial"""

    def __init__(
        self,
        screen,
        pos=(0, 0),
        size=(0, 0),
        bodyImage=None,
        legendImage=None,
        iconImage=None,
        handImage=None,
        inputMin=0,
        inputMax=100,
        kp=0.8,
    ):
        """Initialise dial at x,y. Default size of 300px can be overidden using w,h"""
        path = os.path.dirname(__file__)
        if bodyImage == None:
            bodyImage = imageLoad(
                os.path.join(path, "../resources/Indicator_Background.png")
            )
        if legendImage == None:
            bodyImage = imageLoad(os.path.join(path, "../resources/ledgend.png"))
        if handImage == None:
            handImage = imageLoad(os.path.join(path, "../resources/AirSpeedNeedle.png"))
        if iconImage == None:
            iconImage = imageLoad(os.path.join(path, "../resources/battery2.png"))

        super().__init__(
            screen,
            pos,
            size,
            bodyImage=bodyImage,
            handImage=handImage,
            inputOffset=-inputMin,
            kp=kp,
            inputToDeg=-270 / (inputMax - inputMin),
            offset_deg=160,
            minMax_deg=(-160, 160),
        )
        self.setIcon(iconImage=iconImage, x=0, y=100)  #< The battery icon
