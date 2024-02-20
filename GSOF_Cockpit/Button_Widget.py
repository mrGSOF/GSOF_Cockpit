import pygame

EVT_BUTTON = 0
MouseBtnPressed = 0
MouseBtnReleased = 1
MouseEnteredArea = 2
MouseExitArea = 3

class Button(TextCtrl):
    def action(self, mousePos, actionBtn, fade=0.6):
        if self.inArea(mousePos):
            if self.overArea == False:
                self.overArea = True
                #print('Entered')
                if self.functionEnterArea:
                    self.functionEnterArea()
            if self.pressed == True:
                if actionBtn[0] == 0:
                    #print('Released')
                    self.pressed = False
                    if self.functionReleased:
                        self.functionReleased()
                else:
                    self.draw(0)
            else:
                if actionBtn[0] == 1:
                    #print('Press')
                    self.pressed = True
                    if self.functionPress:
                        self.functionPress()
                else:
                    self.draw()
        else:
            if self.overArea == True:
                self.overArea = False
                #print('Exit')
                if self.functionExitArea:
                    self.functionExitArea()
            self.draw(fade=fade)
            self.pressed = False
