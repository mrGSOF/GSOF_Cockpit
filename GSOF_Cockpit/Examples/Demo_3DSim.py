#!/usr/bin/python
"""
* Demo_Cockpit.py
* Created on: 6 Jan 2025
* Author:     Guy Soffer
* Copyright (C) 2025 Guy Soffer
"""

import sys, math, random
import pygame
from Data import Data
from GSOF_Cockpit.Aerospace import ArtificialHorizon as AH
from GSOF_Cockpit.Aerospace import TurnCoordinator_Analog as TC
from GSOF_Cockpit.Aerospace import AltMeter_Analog as ALT
from GSOF_Cockpit.Aerospace import MachMeter_Analog as MACH
from GSOF_Cockpit.Aerospace import AirSpeedMeter_Analog as AS
from GSOF_Cockpit.Aerospace import VsiMeter_Analog as VSI
from GSOF_Cockpit.Aerospace import Heading_Analog as HEAD

try:
    from GSOF_Cockpit.Wireframe3D import Model3D as WORLD
    from GSOF_3dWireFrame.Lib3D import Object_WireFrame as OWF
    from GSOF_3dWireFrame.Lib3D import Object_base as OB
    from GSOF_3dWireFrame.Lib3D import Objects

    _3D_active = True
except:
    _3D_active = False
    print("GSOF_Wireframe3D module isn't installed")

##from GSOF_Cockpit.Button import Button_Rect
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock


class DemoCockpit:
    """Constructs the gauges screen"""

    def __init__(
        self, screen, pos=(0, 0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder="./"
    ):
        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        world_size = (int(600 * scale), int(300 * scale))
        turn_size = (int(150 * scale), int(150 * scale))
        horizon_size = (int(150 * scale), int(150 * scale))
        alt_size = (int(150 * scale), int(150 * scale))
        vsi_size = (int(150 * scale), int(150 * scale))
        head_size = (int(150 * scale), int(150 * scale))
        as_size = (int(150 * scale), int(150 * scale))
        mach_size = (int(150 * scale), int(150 * scale))
        background_size = (int(600 * scale), int(600 * scale))

        ###Positioning the gauges
        X0, Y0 = pos
        world_pos = (X0 + gap, Y0 + gap)
        as_pos = (world_pos[0] + 0, world_pos[1] + world_size[1] + gap)
        horizon_pos = (as_pos[0] + as_size[0] + gap, as_pos[1])
        alt_pos = (horizon_pos[0] + horizon_size[0] + gap, horizon_pos[1])
        mach_pos = (alt_pos[0] + alt_size[0] + gap, alt_pos[1])

        turn_pos = (as_pos[0], as_pos[1] + as_size[1] + gap)
        head_pos = (turn_pos[0] + turn_size[0] + gap, turn_pos[1])
        vsi_pos = (head_pos[0] + head_size[0] + gap, head_pos[1])

        ###Initialise the gauges.
        self.background = Text(
            screen=self.screen, pos=pos, size=background_size, color=colorBG, name=""
        )
        PI = math.pi
        net = (
            OWF.Object_wireFrame(obj=Objects.net(25, 25), color=(0, 100, 0))
            .rotate(x=PI / 2, y=0, z=0)
            .translate(V=(-1000, -2000, -1000), initShape=True)
            .scale(0.2, initShape=True)
        )
        axis = (
            OWF.Object_wireFrame(
                filename="%s/objects/axis.json" % folder, color=(10, 10, 10)
            )
            .translate(V=(0, 0, 0), initShape=True)
            .scale(1.5, initShape=True)
        )
        plane = (
            OWF.Object_wireFrame(
                filename="%s/objects/c172.stl" % folder, color=(0, 0, 255)
            )
            .rotate(x=-PI / 2, y=0, z=0)
            .translate(V=(0, 0, 0), initShape=True)
        )
        plane.setOrigin(
            origin=plane.getOrigin(origin="arithCenter"), initShape=True
        ).scale(0.035, initShape=True)
        world = OB.Object_container(objList=(net, axis, plane))
        self.world = WORLD.Model3D(
            self.screen,
            pos=world_pos,
            size=world_size,
            world=world,
            bodyImage=imageLoad("%s/skin/Frame_Rect600x300.png" % folder),
        )

        self.airSpd = AS.AirSpeedMeter(self.screen, pos=as_pos, size=as_size)
        self.horizon = AH.ArtificialHorizon(
            self.screen, pos=horizon_pos, size=horizon_size
        )
        self.alt = ALT.AltMeter(self.screen, pos=alt_pos, size=alt_size)
        self.mach = MACH.MachMeter(self.screen, pos=mach_pos, size=mach_size)
        self.turn = TC.TurnCoord(self.screen, pos=turn_pos, size=turn_size)
        self.head = HEAD.Heading(self.screen, pos=head_pos, size=head_size)
        self.vsi = VSI.VsiMeter(self.screen, pos=vsi_pos, size=vsi_size)

    def update(self, newData):
        """
        Update all the dials. Usually done in a different rate then the actuale display refresh.
        Also each dial can have a behaviour model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...)
        """
        self.world.update(
            x=newData["RX_worldX"],
            y=newData["RX_worldY"],
            z=newData["RX_worldZ"],
            yaw=newData["RX_worldYaw"],
            pitch=newData["RX_worldPitch"],
            roll=newData["RX_worldRoll"],
        )
        self.horizon.update(-newData["RX_est_x"], -newData["RX_est_y"])
        self.turn.update((newData["RX_est_x"]) / 2, (newData["RX_accel_x"]) / 4)
        self.alt.update(newData["RX_alt"])
        self.mach.update(newData["RX_mach"])
        self.vsi.update(newData["RX_vsi"])
        self.head.update(
            newData["RX_head"], newData["RX_head"] + random.randrange(-5, 5)
        )
        self.airSpd.update(newData["RX_airSpd"])

    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.world.draw()

        self.horizon.draw()
        self.turn.draw()
        self.alt.draw()
        self.mach.draw()
        self.vsi.draw()
        self.head.draw()
        self.airSpd.draw()


# Initialise screen.
BG_color = COLOR.DARK
screen_size = (600, 600)
init()
screen = getScreen(screen_size)
fillScreen(screen, COLOR.WHITE)

# Initialise Dials.
path = "../"
Cockpit = DemoCockpit(screen, colorBG=BG_color, scale=1.0, folder=path)
Telemetry = Data(screen_size)
clock = Clock()

while True:
    ###Loop to update gauges
    Cockpit.update(Telemetry.getData())
    Cockpit.draw()
    update()
    clock.tick(Fs=25)
