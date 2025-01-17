from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR

MouseBtnPressed  = 0
MouseBtnReleased = 1
MouseEnterArea   = 2
MouseExitArea    = 3

class Button_base():
    """Baseclass for a button"""
    def __init__(self, screen, pos=(0,0), size=None,
                 funcEnterArea=None, funcExitArea=None, funcPressed=None, funcReleased=None):
        self.area = (pos[0], pos[1], size[0], size[1])
        self._overArea = False
        self._pressed = False
        self.setCallback(event=MouseBtnPressed,  function=funcPressed)
        self.setCallback(event=MouseBtnReleased, function=funcReleased)
        self.setCallback(event=MouseEnterArea,   function=funcEnterArea)
        self.setCallback(event=MouseExitArea,    function=funcExitArea)

    def setCallback(self, event, function):
        if event == MouseBtnPressed:
            self._fPress = function
        elif event == MouseBtnReleased:
            self._fReleased = function
        elif event == MouseEnterArea:
            self._fEnterArea = function
        elif event == MouseExitArea:
            self._fExitArea = function
        else:
            print("Unrecognized MouseBtn event")
        return self

    def _inArea(self, pos) -> bool:
        posX=pos[0]
        posY=pos[1]
        TL=(self.area[0], self.area[1])
        BR=(self.area[0] +self.area[2], self.area[1] +self.area[3])
        if (TL[0] <posX < BR[0]) and ( TL[1] < posY < BR[1]):
            return True
        return False

    def action(self, mouse={}, fade=0.6):
        mousePos=mouse["pos"]
        actionBtn=mouse["btn"]
        if self._inArea(mousePos):
            if self._overArea == False:
                print('Entered')
                self._overArea = True
                if self._fEnterArea:
                    self._fEnterArea()

            if self._pressed == True:
                if actionBtn[0] == 0:
                    print('Released')
                    self._pressed = False
                    if self._fReleased:
                        self._fReleased()
                else:
                    self.draw(fade=0)
            else:
                if actionBtn[0] == 1:
                    print('Press')
                    self._pressed = True
                    if self._fPress:
                        self._fPress()
                else:
                    self.draw()
        else:
            if self._overArea == True:
                self._overArea = False
                print('Exit')
                if self._fExitArea:
                    self._fExitArea()
            self.draw(fade=fade)
            self._pressed = False

class Button_Empty(Button_base):
    """Transparent button without label"""
    def draw(self, fade=1.0):
        return

class Button_Rect(Text, Button_base):
    """Rectangular button with label"""
    def __init__(self, screen, pos=(0,0), size=None,
                 color=COLOR.GRAY, textColor=COLOR.BLACK,
                 name="Button", font=None,
                 funcEnterArea=None, funcExitArea=None, funcPressed=None, funcReleased=None):
        Text.__init__(self, screen, pos, size, color, textColor, name, font)
        Button_base.__init__(self, screen, pos, (self.area[2],self.area[3]),
                 funcEnterArea, funcExitArea, funcPressed, funcReleased) 

    def draw(self, fade=1.0):
        Text.draw(self, fade)

class Button_Round(Text, Button_base):
    """Rectangular button with label"""
    def __init__(self, screen, pos=(0,0), size=None,
                 color=COLOR.GRAY, textColor=COLOR.BLACK,
                 name="Button", font=None,
                 funcEnterArea=None, funcExitArea=None, funcPressed=None, funcReleased=None):
        Text.__init__(self, screen, pos, size, color, textColor, name, font)
        Button_base.__init__(self, screen, pos, (self.area[2],self.area[3]),
                 funcEnterArea, funcExitArea, funcPressed, funcReleased) 

    def _inArea(self, pos) -> bool:
        x = pos[0] -self.center[0]
        y = pos[1] -self.center[1]
        r = (x**2) +(y**2)
        if (r <= self.radius):
            return True
        return False

    def draw(self, fade=1) -> None:
        Text.drawEllipse(self, fade)
