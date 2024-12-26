## Created on: 25 Dec 2024
## Author    : Guy Soffer

import os, math
from GSOF_Cockpit.Gauge_base import Gauge
from GSOF_Cockpit.GraphicsLib import imageLoad, drawLine, fillSurface

from Lib3D import Object_WireFrame as OWF
from Lib3D import Object_base as OB
from Lib3D import Objects
from Lib3D import WireFrame_display as DISP

PI = math.pi

class World(Gauge):
    def __init__(self, screen, pos=(0,0), size=(0,0),
                 bodyImage=None, world=None):
        path = os.path.dirname(__file__)
        if bodyImage == None:
            bodyImage = imageLoad(os.path.join(path, '../skin/Frame_Rect.png'))

        super().__init__(screen, bodyImage, pos, size)

        if world == None:
            net = OWF.Object_wireFrame(obj=Objects.net(25,20), color=(0,100,0)).translate(V=(-1000, 0, 500), initShape=True).scale(0.15, initShape=True)
            plane = OWF.Object_wireFrame(filename=os.path.join(path, "../objects/F16.stl"), color=(0,0,255)).rotate(-PI/2,0,0).scale(0.015, initShape=True)
            world = OB.Object_container(objList = (
                net,
                plane,
                ))
        self._world = world
        
    def update(self, x=0, y=0, z=0, yaw=0, pitch=0, roll=0): #< x:pitvh, y:roll, z:yaw
        """Update the position and attitude angle of 3D world"""
        self._world.reset()
        self._world.translate(x=x, y=y, z=z, initShape=False)
        self._world.rotate(x=pitch*PI/180, y=roll*PI/180, z=yaw*PI/180, initShape=False)

    def draw(self, draw=True):
        fillSurface(self._dial, 0xffffff) #WHITE)
        self._drawWireFrame(color=None)
        super().draw(True)

    def _drawWireFrame(self, color=None) -> None:
        for line in self._world.getLines():
            x0, y0, z0 = line.p0
            x1, y1, z1 = line.p1
            if color == None:
                color = line.color
            drawLine( self._dial, color, (x0, y0), (x1, y1) ) #< Line from P0 to P1
