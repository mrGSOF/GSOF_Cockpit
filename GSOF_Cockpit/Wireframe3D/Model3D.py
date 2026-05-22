## Created on: 25 Dec 2024
## Author    : Guy Soffer

import os, math
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.GraphicsLib import imageLoad, drawLine, fillSurface

from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
from GSOF_3dWireFrame.Lib3D import Object_base as OB
from GSOF_3dWireFrame.Lib3D import Objects
from GSOF_3dWireFrame.Lib3D import WireFrame_display as DISP

PI = math.pi


class Model3D(Gauge):
    def __init__(self, screen, pos=(0, 0), size=(0, 0), bodyImage=None, world=None):
        path = os.path.dirname(__file__)
        if bodyImage == None:
            bodyImage = imageLoad(os.path.join(path, "../skin/Frame_Rect.png"))

        super().__init__(screen, bodyImage, pos, size)

        if world == None:
            net = (
                OWF.Object_wireFrame(obj=Objects.net(25, 25), color=(0, 100, 0))
                .rotate(x=PI / 2, y=0, z=0)
                .translate(V=(-1000, -1000, -1000), initShape=True)
                .scale(0.2, initShape=True)
            )
            axis = (
                OWF.Object_wireFrame(
                    filename=os.path.join(path, "../objects/axis.json"),
                    color=(10, 10, 10),
                )
                .translate(V=(0, 0, 0), initShape=True)
                .scale(1.5, initShape=True)
            )
            world = OB.Object_container(objList=(net, axis))
        self._world = world
        self._wireframe = DISP.WireFrame(
            self._dial, drawLine, f=50, scale=10
        )  #< f and scale affect the perspective calculation

    def update(self, x=0, y=0, z=0, yaw=0, pitch=0, roll=0):  #< x:pitvh, y:roll, z:yaw
        """Update the position and attitude angle of 3D world"""
        self._world.reset()
        self._world.rotate(
            x=pitch * PI / 180, y=yaw * PI / 180, z=roll * PI / 180, initShape=False
        )
        self._world.translate(x=x, y=y, z=z, initShape=False)

    def draw(self, draw=True):
        fillSurface(self._dial, 0xFFFFFF)  # WHITE)
        # self._drawWireFrame(color=None)
        self._wireframe.draw(self._world)
        super().draw(True)

    def _drawWireFrame(self, color=None) -> None:
        for line in self._world.getLines():
            x0, y0, z0 = line.p0
            x1, y1, z1 = line.p1
            if color == None:
                color = line.color
            drawLine(self._dial, color, (x0, y0), (x1, y1))  #< Line from P0 to P1
