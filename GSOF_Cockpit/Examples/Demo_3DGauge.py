#!/usr/bin/python
"""
* Demo_3DGauge.py
* Created on: 20 Jan 2025
* Author:     Guy Soffer
* Copyright (C) 2025 Guy Soffer
"""

import math
from Data import Data

try:
    from GSOF_Cockpit.Wireframe3D import World3D as WORLD
    from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
    from GSOF_3dWireFrame.Lib3D import Object_base as OB
    from GSOF_3dWireFrame.Lib3D import Objects

    _3D_active = True
except:
    _3D_active = False
    print("GSOF_Wireframe3D module isn't installed")

from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

# Initialise screen.
BG_color = COLOR.DARK
screen_size = (600, 600)
pos = (0, 0)
init()
screen = getScreen(screen_size)
fillScreen(screen, COLOR.WHITE)

# Initialise Dials.
path = "../"
PI = math.pi

background = Text(screen=screen, pos=pos, size=screen_size, color=BG_color, name="")
net = (
    OWF.Object_wireFrame(obj=Objects.net(25, 25), color=(0, 100, 0))
    .rotate(x=PI / 2, y=0, z=0)
    .translate(V=(-1000, -2000, -1000), initShape=True)
    .scale(0.2, initShape=True)
)
axis = (
    OWF.Object_wireFrame(filename="%s/objects/axis.json" % path, color=(10, 10, 10))
    .translate(V=(0, 0, 0), initShape=True)
    .scale(1.5, initShape=True)
)
plane = (
    OWF.Object_wireFrame(filename="%s/objects/c172.stl" % path, color=(0, 0, 255))
    .rotate(x=-PI / 2, y=0, z=0)
    .translate(V=(0, 0, 0), initShape=True)
)
plane.setOrigin(origin=plane.getOrigin(origin="arithCenter"), initShape=True).scale(
    0.035, initShape=True
)
world = OB.Object_container(objList=(net, axis, plane))
world = WORLD.World(
    screen,
    pos=(0, 0),
    size=screen_size,
    world=world,
    bodyImage=imageLoad("%s/skin/Frame_Rect600x600.png" % path),
)

Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    newData = Telemetry.getData()
    world.update(
        x=newData["RX_worldX"],
        y=newData["RX_worldY"],
        z=newData["RX_worldZ"],
        yaw=newData["RX_worldYaw"],
        pitch=newData["RX_worldPitch"],
        roll=newData["RX_worldRoll"],
    )
    background.draw()
    world.draw()
    update()
    clock.tick(Fs=25)
