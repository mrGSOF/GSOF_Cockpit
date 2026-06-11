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
    from GSOF_Cockpit.Wireframe3D.Model3D import Model3D
    from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
    from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
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
    Object(obj=Objects.net(25, 25), color=(0, 100, 0))
    .rotate(x=PI / 2, y=0, z=0)
    .translate(-100, -100, -100)
    .scale(0.1)
    .setOrigin()
)
axis = (
    Object(filename="%s/objects/axis.json" % path, color=(10, 10, 10))
    .translate(0, 0, 0)
    .scale(1.5)
    .setOrigin()
)
plane = (
    Object(filename="%s/objects/c172.stl" % path, color=(0, 0, 255))
    .rotate(x=-PI / 2, y=0, z=0)
    .translate(0, 0, 0)
    .setOrigin()
)
plane.setCenter(method="arithCenter")

world = Assembly(objects=(net, axis, plane))
world = Model3D(
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
