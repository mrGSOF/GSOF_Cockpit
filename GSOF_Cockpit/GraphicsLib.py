## Created on: 2 / Dec 2024
## Author    : Guy Soffer

import math, time
import pygame

overlayColor = 0xFFFF00

def init():
    pygame.init()

def update():
    pygame.display.update()
    
def fillScreen(screen, rgbColor):
    screen.fill(rgbColor)
   
def getScreen(screenSize):
    return pygame.display.set_mode(screenSize)
    
def imageLoad(filename):
    return pygame.image.load(filename).convert()

def getMouse():
    return {"pos":pygame.mouse.get_pos(), "btn":pygame.mouse.get_pressed()}

def scale(image, newSize):
    return pygame.transform.scale(image, newSize)

def blit(dest, image, pos):
    dest.blit( image, pos )

def drawEcllipse(screen, color, area):
    pygame.draw.ellipse(screen, color, area)

def drawRect(screen, color, area):
    pygame.draw.rect(screen, color, area)

def renderText(text, font, textColor):
    return font.render(text, True, textColor)

def getFont(name=None, size=20):
    return pygame.font.Font(name, size)

def getBitmapWidth(bmp):
    return bmp.get_width()
    
def getBitmapHeight(bmp):
    return bmp.get_height()

def rotate(image, angle):
    """
    Rotate image by "angle" degrees around it's center
    If you need to offset the centre, resize the image using clip
    Used to rotate dial needles and probably doesn't need to be used externally
    """
    tmpImage = pygame.transform.rotate(image ,angle)
    imageCentreX = tmpImage.get_rect()[0] +tmpImage.get_rect()[2]/2
    imageCentreY = tmpImage.get_rect()[1] +tmpImage.get_rect()[3]/2

    targetWidth  = tmpImage.get_rect()[2]
    targetHeight = tmpImage.get_rect()[3]

    imageOut = pygame.Surface((targetWidth, targetHeight))
    imageOut.fill( overlayColor )
    imageOut.set_colorkey( overlayColor )
    imageOut.blit(tmpImage,
                  (0,0),
                  pygame.Rect(imageCentreX -targetWidth/2,
                              imageCentreY -targetHeight/2,
                              targetWidth,
                              targetHeight
                              )
                  )
    return imageOut

def clip(image, x=0, y=0, w=0, h=0, oX=0, oY=0):
    """
    Cuts out a part of the needle image at x,y position to the correct size (w,h)
    Copy to "imageOut" at an offset of oX,oY if required
    Used to center the indicators inside the gauge frame
    """
    if w == 0:
        w = image.get_rect()[2]
    if h == 0:
        h = image.get_rect()[3]
        
    needleW = w +2*math.sqrt(oX*oX)
    needleH = h +2*math.sqrt(oY*oY)
    imageOut = pygame.Surface((needleW, needleH))
    imageOut.fill( overlayColor )
    imageOut.set_colorkey( overlayColor )
    imageOut.blit(image, (needleW/2 -w/2 +oX, needleH/2 -h/2 +oY), pygame.Rect(x,y,w,h))
    return imageOut

def drawOnScreen(screen, obj, size, pos) -> None:
    obj.set_colorkey( overlayColor )
    screen.blit( pygame.transform.scale( obj, size), pos )

class Clock():
    def __init__(self):
        self.T0 = time.time()

    def tick(self, Fs=None, Ts=None):
        if Ts == None:
            Ts = 1.0/Fs
        self.T0 += Ts
        wait = self.T0 -time.time()
        if wait > 0.01:
            time.sleep(wait)
        wait = self.T0 -time.time()
        while (wait < 0.01) and (wait > 0.001):
            wait = self.T0 -time.time()
        
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
    """Manimulate the skin using two variables (X,Y)"""
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
    """Manimulate the skin using three variables, R,X,Y"""
    def __init__(self, skin,
                 initValX, offsetX, gainX, kpX, toAuX, offsetX_au, minMaxX_au, moduluX_au,
                 initValY, offsetY, gainY, kpY, toAuY, offsetY_au, minMaxY_au, moduluY_au,
                 initValZ, offsetZ, gainZ, kpZ, toAuZ, offsetZ_au, minMaxZ_au, moduluZ_au,
                 ):
        super().__init__(initVal, offset, gain, kp, toDeg, offset_deg, minMax_deg, modulu_deg)
        self.skin = skin
