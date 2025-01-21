"""
 * Data.py
 * Created on: 6 Jan 2025
 * Author:     Guy Soffer
 * Copyright (C) 2025 Guy Soffer
"""

import math, random
import pygame
from GSOF_Cockpit.GraphicsLib import getMouse


class Data():
    """Data source to drive gauges screen"""
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.t = 0
        self.Vbat = 9
        self.Ibat = 0
        self.alt = 0
        self.airSpd = 0.0
        self.vsi = 5

    def getData(self) -> dict:
        """Generate and return new set of data"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting....')
                sys.exit()   # end program.

        # Use dummy test data
        curPos = (getMouse())["pos"]

        # We have data.
        self.t += 1

        self.Vbat += 0.1
        if self.Vbat >13:
            self.Vbat = 9
        self.Ibat += 0.1
        self.Ibat %= 6.5

        self.alt += 10
        self.airSpd += 5.0
        if self.airSpd > 1500.0:
            self.airSpd = 0.0
        self.g = 9.8

        t = self.t
        head_r = 6.24*0.5*t*0.01
        posY   = 40*math.sin(head_r)
        posX   = 40*math.cos(head_r)
        head_d = head_r*180/3.14 +180

        return {'RX_time': t,
                'RX_eng':50+50*math.sin(6.28*0.01*t),
                'RX_batt_volt':self.Vbat, 'RX_batt_cur':self.Ibat,
                'TX_fr_success':posX, 'RX_G':self.g*(math.sin(6.28*0.01*t)),
                'RX_alt':self.alt, 'RX_accel_x':50*math.sin(6.28*0.01*t),
                'RX_est_x':(self.screen_size[0]/2 -curPos[0]), 'RX_est_y':(self.screen_size[1]/2 -curPos[1]),
                'RX_vsi':self.vsi*math.sin(6.28*0.01*t), 'RX_airSpd':self.airSpd,
                'RX_mach':self.airSpd/1000.0,
                'RX_posX':posX, 'RX_posY':posY, 'RX_head':head_d,
                'RX_worldX':0, 'RX_worldY':0, 'RX_worldZ':-600.0,
                'RX_worldYaw':-head_d +180, 'RX_worldPitch':0.0, 'RX_worldRoll':45.0
               }

