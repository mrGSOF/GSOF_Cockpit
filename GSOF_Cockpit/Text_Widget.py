import pygame
from GSOF_Cockpit import Pygame_Colors as COLOR

class TextCtrl():
    def __init__(self, GUIobj=False, pos=(0,0), size=-1, color=COLOR.GRAY, textColor=COLOR.BLACK, name='Button', function=False, ANSI=False, draw=True):
        self.GUIobj = GUIobj
        self.overArea = False
        self.pressed = False
        self.functionPress = function
        self.functionReleased = False
        self.functionOver = False
        self.functionEnterArea = False
        self.functionExitArea = False
        
        self.ANSI = ANSI

        self.color = color
        self.textColor = textColor
        self.textSize = 20
        self.font = pygame.font.Font(None, self.textSize)
        self.name = name
        self.textBitmap = self.font.render(self.name, True, self.textColor)

        if size == -1:
            size = (self.textBitmap.get_width()+10, self.textBitmap.get_height()+8)
        self.area = (pos[0], pos[1], size[0], size[1])
        if draw:
            self.draw()
            
    def style(self, name=False, textColor=False, color=False, font=False, textSize=False):
        if name != False:
            self.name = name
        if textColor != False:
            self.textColor = textColor
        if color != False:
            self.color = color
        if font != False:
            self.font = font
        if textSize != False:
            self.textSize = textSize
        self.textBitmap = self.font.render(self.name, True, self.textColor)
        
    def Bind(self, event, function):
        if event == MouseBtnPressed:
            self.functionPress=function
        elif event == MouseBtnReleased:
            self.functionReleased=function
        elif event == MouseEnterArea:
            self.functionEnterArea=function
        elif event == MouseExitArea:
            self.functionExitArea=function
        
    def draw(self, GUIobj=False, fade=1):
        if self.ANSI == False:
            color = (self.color[0]*fade, self.color[1]*fade, self.color[2]*fade)
            pygame.draw.rect(self.GUIobj, color, self.area)

            textPosX = self.area[0] +int(self.area[2]/2) -self.textBitmap.get_width()/2
            textPosY = self.area[1] +int(self.area[3]/2) -self.textBitmap.get_height()/2
            if GUIobj != False:
                GUIobj.blit(self.textBitmap, (textPosX, textPosY))
            elif self.GUIobj != False:
                self.GUIobj.blit(self.textBitmap, (textPosX, textPosY))

    def inArea(self, pos):
        posX=pos[0]
        posY=pos[1]
        TL=(self.area[0], self.area[1])
        BR=(self.area[0] +self.area[2], self.area[1] +self.area[3])
        if (TL[0] <posX < BR[0]) and ( TL[1] < posY < BR[1]):
            return True
        return False

    def action(self, mousePos, actionBtn, fade=1.0):
        self.draw(fade)
