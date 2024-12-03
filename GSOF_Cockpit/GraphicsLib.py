## Created on: 2 / Dec 2024
## Author    : Guy Soffer

import math
import pygame

overlayColor = 0xFFFF00

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

class Hand():
    def __init__(self, initVal, offset, gain, kp, toDeg, offset_deg, minMax_deg, modulu_deg, skin):
      self.val_Z1     = initVal
      self.offset     = offset
      self.gain       = gain
      self.kp         = kp
      self.toDeg      = toDeg
      self.offset_deg = offset_deg
      self.minMax_deg = minMax_deg
      self.modulu_deg = modulu_deg
      self.skin       = skin
      self.update(self.val_Z1)

    def update(self, val) -> None:
        val = val*self.gain +self.offset
        self.val_Z1 += (val -self.val_Z1)*self.kp
        self._updateAngle()

    def _updateAngle(self, val=None):
        if val == None:
            val = self.val_Z1
        angle = val*self.toDeg +self.offset_deg

        if self.minMax_deg != None:
            Min, Max = self.minMax_deg
            if angle > Max:
                angle = Max
            elif angle < Min:
                angle = Min
        self.angle_deg = math.fmod(angle, self.modulu_deg)
