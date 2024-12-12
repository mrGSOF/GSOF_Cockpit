from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR

MouseBtnPressed  = 0
MouseBtnReleased = 1
MouseEnteredArea = 2
MouseExitArea    = 3

class Button(Text):
    def __init__(self, screen, pos=(0,0), size=None,
                 color=COLOR.GRAY, textColor=COLOR.BLACK,
                 name="Button", font=None,
                 funcEnterArea=None, funcExitArea=None, funcPressed=None, funcReleased=None):
        super().__init__(screen, pos=(0,0), size=None,
                 color=COLOR.GRAY, textColor=COLOR.BLACK,
                 name="Button", font=None)
        self.overArea = False
        self.pressed = False
        self.setCallback(event=MouseBtnPressed,  function=funcPressed)
        self.setCallback(event=MouseBtnReleased, function=funcReleased)
        self.setCallback(event=MouseEnterArea,   function=funcEnterArea)
        self.setCallback(event=MouseExitArea,    function=funcExitArea)

    def setCallback(self, event, function):
        if event == MouseBtnPressed:
            self._fPress=function
        elif event == MouseBtnReleased:
            self._fReleased=function
        elif event == MouseEnterArea:
            self._fEnterArea=function
        elif event == MouseExitArea:
            self._fExitArea=function
        return self

    def _inArea(self, pos) -> bool:
        posX=pos[0]
        posY=pos[1]
        TL=(self.area[0], self.area[1])
        BR=(self.area[0] +self.area[2], self.area[1] +self.area[3])
        if (TL[0] <posX < BR[0]) and ( TL[1] < posY < BR[1]):
            return True
        return False

    def action(self, mousePos, actionBtn, fade=0.6):
        if self._inArea(mousePos):
            if self._overArea == False:
                #print('Entered')          
                self._overArea = True
                if self._fEnterArea:
                    self._fEnterArea()

            if self._pressed == True:
                if actionBtn[0] == 0:
                    #print('Released')
                    self._pressed = False
                    if self._fReleased:
                        self._fReleased()
                else:
                    self.draw(0)
            else:
                if actionBtn[0] == 1:
                    #print('Press')
                    self._pressed = True
                    if self._fPress:
                        self._fPress()
                else:
                    self.draw()
        else:
            if self._overArea == True:
                self._overArea = False
                #print('Exit')
                if self._fExitArea:
                    self._fExitArea()
            self.draw(fade=fade)
            self._pressed = False
