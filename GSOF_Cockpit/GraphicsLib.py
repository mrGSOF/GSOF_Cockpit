## Created on: 2 / Dec 2024
## Author    : Guy Soffer

import math
import pygame

overlayColor = 0xFFFF00

def init():
    pygame.init()

def update():
    pygame.display.update()
    
def getScreen(screenSize):
    return pygame.display.set_mode(screenSize)
    
def fillScreen(screen, rgbColor):
    screen.fill(rgbColor)
   
def getSurface(surfaceSize):
    return pygame.Surface(surfaceSize)

def getRectSize(surface, center=(0,0)):
    return surface.get_rect(center=center)

def fillSurface(surface, rgbColor):
    surface.fill(rgbColor)

def setTransparentColor(surface, rgbColor=0xFFFF00):
    surface.set_colorkey(rgbColor)
    
def imageLoad(filename):
    return pygame.image.load(filename).convert()

def getMouse():
    return {"pos":pygame.mouse.get_pos(), "btn":pygame.mouse.get_pressed()}

def scale(image, newSize):
    return pygame.transform.scale(image, newSize)

def blit(dest, image, pos, special_flags=0):
    dest.blit( image, pos )

def drawLine(surface, color, fromPnt, toPnt, width=1):
    pygame.draw.line(surface, color, fromPnt, toPnt, width)

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
    imageWidth  = tmpImage.get_rect()[2]
    imageHeight = tmpImage.get_rect()[3]
    imageCentreX = tmpImage.get_rect()[0] +int(imageWidth/2)
    imageCentreY = tmpImage.get_rect()[1] +int(imageHeight/2)


    imageOut = getSurface((imageWidth, imageHeight))
    fillSurface(imageOut, overlayColor )
    setTransparentColor(imageOut, overlayColor )
    blit(imageOut, tmpImage,
         (0,0),
         pygame.Rect(imageCentreX -int(imageWidth/2),
                     imageCentreY -int(imageHeight/2),
                     imageWidth,
                     imageHeight
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
