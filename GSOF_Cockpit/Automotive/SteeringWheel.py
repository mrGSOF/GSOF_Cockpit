## Created on: 10 Mar 2023
## Author:     Guy Soffer

from GSOF_Cockpit.Utils import getResourcePath
from GSOF_Cockpit.SingleIndicator import SingleIndicator
from GSOF_Cockpit.GraphicsLib import imageLoad


class SteeringWheel(SingleIndicator):
    def __init__(
        self,
        screen,
        pos,
        size,
        bodyImage=None,
        wheelImage=None,
        inputToDeg=10.0,
        offset_deg=9.8,
        kp=0.8,
        minMax_deg=(-270, 270),
    ):

        if bodyImage == None:
            bodyImage = imageLoad(
                getResourcePath(
                    "GSOF_Cockpit", "resources/Indicator_Background.png"
                )
            )
        if wheelImage == None:
            wheelImage = imageLoad(
                getResourcePath(
                    "GSOF_Cockpit", "resources/SteeringWheel.png"
                )
            )

        super().__init__(
            screen=screen,
            pos=pos,
            size=size,
            bodyImage=bodyImage,
            handImage=wheelImage,
            inputToDeg=inputToDeg,
            offset_deg=offset_deg,
            kp=kp,
            minMax_deg=minMax_deg,
        )
