import pygame
from GSOF_Cockpit import Pygame_Colors as COLOR

class Text():
    def __init__(self, screen, pos=(0,0), size=None,
                 color=COLOR.GRAY, textColor=COLOR.BLACK,
                 name="Button", font=None):

        self._screen = screen
        if font == None:
            font = pygame.font.Font(None, 20)
        self.setText(name, textColor, color, font)

        if size == None:
            size = (self.textBitmap.get_width()+10, self.textBitmap.get_height()+8)
        self.area = (pos[0], pos[1], size[0], size[1])
        self.center = (self.area[0] +int(self.area[2]/2), self.area[1] +int(self.area[3]/2))
        self.radius = size[0]
            
    def setText(self, name=None, textColor=None, color=None, font=None):
        if name != None:
            self.name = name
        if textColor != None:
            self.textColor = textColor
        if color != None:
            self.color = color
        if font != None:
            self.font = font
        self.textBitmap = self.font.render(self.name, True, self.textColor)
        return self
                
    def draw(self, fade=1) -> None:
        color = (self.color[0]*fade, self.color[1]*fade, self.color[2]*fade)
        pygame.draw.rect(self._screen, color, self.area)

        textPosX = self.center[0] -self.textBitmap.get_width()/2
        textPosY = self.center[1] -self.textBitmap.get_height()/2
        self._screen.blit(self.textBitmap, (textPosX, textPosY))

    def drawEllipse(self, fade=1) -> None:
        color = (self.color[0]*fade, self.color[1]*fade, self.color[2]*fade)
        pygame.draw.ellipse(self._screen, color, self.area)

        textPosX = self.area[0] +int(self.area[2]/2) -self.textBitmap.get_width()/2
        textPosY = self.area[1] +int(self.area[3]/2) -self.textBitmap.get_height()/2
        self._screen.blit(self.textBitmap, (textPosX, textPosY))
