import math

class InputX():
    def __init__(self, initVal, offset, gain, kp, toAu, offset_au, minMax_au, modulu_au):
        self.val_Z1    = initVal
        self.offset    = offset
        self.gain      = gain
        self.kp        = kp
        self.toAu      = toAu
        self.offset_au = offset_au
        self.minMax_au = minMax_au
        self.modulu_au = modulu_au
        self.update(self.val_Z1)

    def update(self, val) -> None:
        val = val*self.gain +self.offset
        self.val_Z1 += (val -self.val_Z1)*self.kp
        self._updateMovement()

    def _updateMovement(self, val=None):
        if val == None:
            val = self.val_Z1
        pos = val*self.toAu +self.offset_au

        if self.minMax_au != None:
            Min, Max = self.minMax_au
            if pos > Max:
                pos = Max
            elif pos < Min:
                pos = Min
        self.pos_au = math.fmod(pos, self.modulu_au)

class InputXY():
    """Manipulate the skin using two variables (X,Y)"""
    def __init__(self,
                 initValX, offsetX, gainX, kpX, toAuX, offsetX_au, minMaxX_au, moduluX_au,
                 initValY, offsetY, gainY, kpY, toAuY, offsetY_au, minMaxY_au, moduluY_au,
                 ):
        self.inX = InputX(initValX, offsetX, gainX, kpX, toAuX, offsetX_au, minMaxX_au, moduluX_au)
        self.inY = InputX(initValY, offsetY, gainY, kpY, toAuY, offsetY_au, minMaxY_au, moduluY_au)

    def update(self, valX, valY) -> None:
        self.inX.update(valX)
        self.inY.update(valY)

class InputXYZ(InputXY):
    """Three degree of freedom input (R,X,Y)"""
    def __init__(self,
                 initValX, offsetX, gainX, kpX, toAuX, offsetX_au, minMaxX_au, moduluX_au,
                 initValY, offsetY, gainY, kpY, toAuY, offsetY_au, minMaxY_au, moduluY_au,
                 initValZ, offsetZ, gainZ, kpZ, toAuZ, offsetZ_au, minMaxZ_au, moduluZ_au,
                 ):
        super().__init__(initValX, offsetX, gainX, kpX, toAuX, offsetX_au, minMaxX_au, moduluX_au,
                         initValY, offsetY, gainY, kpY, toAuY, offsetY_au, minMaxY_au, moduluY_au)
        self.inZ = Input(initValZ, offsetZ, gainZ, kpZ, toAuZ, offsetZ_au, minMaxZ_au, moduluZ_au)

    def update(self, valX, valY, valZ) -> None:
        super().update(valX, valY)
        self.inZ.update(valZ)

class Hand(InputX):
    def __init__(self, initVal, offset, gain, kp, toDeg, offset_deg, minMax_deg, modulu_deg, skin):
        super().__init__(initVal, offset, gain, kp, toDeg, offset_deg, minMax_deg, modulu_deg)
        self.skin = skin

    def _updateMovement(self, val=None):
        super()._updateMovement(val)
        self.angle_deg = self.pos_au

class MapRXY(InputXYZ):
    """Manipulate the skin using three variables, R,X,Y"""
    def __init__(self, skin,
                 initValX, offsetX, gainX, kpX, toAuX, offsetX_au, minMaxX_au, moduluX_au,
                 initValY, offsetY, gainY, kpY, toAuY, offsetY_au, minMaxY_au, moduluY_au,
                 initValZ, offsetZ, gainZ, kpZ, toAuZ, offsetZ_au, minMaxZ_au, moduluZ_au,
                 ):
        super().__init__(initVal, offset, gain, kp, toDeg, offset_deg, minMax_deg, modulu_deg)
        self.skin = skin
