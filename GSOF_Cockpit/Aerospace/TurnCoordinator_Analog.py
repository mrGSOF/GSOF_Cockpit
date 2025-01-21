"""
 * Created on: 28 Mar 2017
 * Author:     Guy Soffer
 * 
 *      Copyright (C) 2017 Guy Soffer
 *      This Python module is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

 *      Thanks to Duncan Law for implementing and sharing the original code.
 *      Thanks to Chootair at http://www.codeproject.com/Members/Chootair 
 *      for the artwork that this code is based on.
 *      His full work is intended for C# and can be found here:
 *      http://www.codeproject.com/KB/miscctrl/Avionic_Instruments.aspx
"""

import pkg_resources
from GSOF_Cockpit.DualIndicator import DualIndicator
from GSOF_Cockpit.GraphicsLib import rotate, scale, clip, blit, imageLoad

class TurnCoord(DualIndicator):
   """Turn Coordinator dial"""
   def __init__(self, screen, pos=(0,0), size=(0,0),
                bodyImage=None, turnImage=None, slipImage=None, iconImage=None,
                turnRateKp=0.5,                #< Filter coefficiant
                turnRateToDeg = 1.0,           #< Use 180.0/3.14 when input is in (Rad)
                turnRateOffset_deg = 0.0,      #< Offset angle of turn indicator
                turnRateMinMax_deg = (-45,45), #< deg
                slipKp=0.5,                    #< Filter coefficiant
                slipToDeg = 1.0,               #< Use 180.0/3.14 when input is in (Rad)
                slipOffset_deg = 0.0,          #< Offset angle of slip needle
                slipMinMax_deg = (-14,14)      #< Minimum and maximum angles of slip indicator
                ):
      """Initialise dial at x,y. Default size of 300px can be overridden using w,h."""

      if bodyImage == None:
         bodyImage  = imageLoad(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinator_Background.png'))
      if turnImage == None:
         turnImage  = imageLoad(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinatorAircraft.png'))
      if slipImage == None:
         slipImage  = imageLoad(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinatorBall.png'))
      if iconImage == None:
         iconImage  = imageLoad(pkg_resources.resource_filename('GSOF_Cockpit', 'resources/TurnCoordinatorMarks.png'))

      super().__init__(screen=screen, bodyImage=bodyImage, handAImage=turnImage, handBImage=slipImage,
                       pos=pos, size=size,
                       inputGain   = 1.0,                #< Input scaling is applied before offset
                       inputOffset = 0.0,                #< Input offset is added to input value afterscale factor
                       kp          = turnRateKp,         #< Filter coefficient (0-no filter)
                       #kp          = slipKp

                       inputAtoDeg = turnRateToDeg,      #< Input value to degrees factor applied after offset
                       offsetA_deg = turnRateOffset_deg, #< Input offset is added to input value before scale factor
                       minMaxA_deg = turnRateMinMax_deg, #< Indicator angle min/max (deg)
                       moduluA_deg = 360,                #< Modulu for indicator angle (deg)

                       inputBtoDeg = slipToDeg,          #< Input value to degrees factor applied after offset
                       offsetB_deg = slipOffset_deg,     #< Input offset is added to input value before scale factor
                       minMaxB_deg = slipMinMax_deg,     #< Indicator angle min/max (deg)
                       moduluB_deg = 360                 #< Modulu for indicator angle (deg)
                      )
      if iconImage != None:
         self.setIcon(iconImage, x=0, y=80)

   def update(self, TurnRate, SideAcc):
      super().update(val=TurnRate, valB=SideAcc)

   def draw(self):
      """Draw the Turn Coordinator dial on the screen" surface"""
      angleX = int(self._handA.pos_au) 
      angleY = int(self._handB.pos_au)
      tmpImage = clip(self._handA.skin, 0, 0, 0, 0, 0, -12) #< Turn rate
      tmpImage = rotate(tmpImage, angleX)
      self._overlay(self._body, 0,0) #< Body (frame)
      self._overlay(tmpImage, 0, 0)
      tmpImage = clip(self._icon, 0, 0, 0, 0, 0, 0)
      self._overlay(tmpImage, self._iconX, self._iconY)
      tmpImage = clip(self._handB.skin, 0, 0, 0, 0, 0, 300) #< Slip
      tmpImage = rotate(tmpImage, angleY)
      self._overlay(tmpImage, 0, -220)
      self._dial.set_colorkey(0xFFFF00)
      blit(dest=self._screen, image=scale(self._dial, (self.w,self.h)), pos=self.pos )
