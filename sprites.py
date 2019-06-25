# Sprite objects

import sys
from pygame import sprite, image, transform
from PIL import Image
try:
    import numpy as np
    from hueshift import shift_hue
    HAVE_NUMPY = True
except ImportError:
    sys.stderr.write("Warning: numpy not available. The game will function without it, but you may experience poorer performace.\n")
    sys.stderr.flush()
    from colorsys import rgb_to_hsv, hsv_to_rgb
    HAVE_NUMPY = False

import time

class SpriteError(Exception):
    def __init__(self,msg):
        sys.stderr.write(msg+"\n")
        sys.stderr.flush()

class Spinner(sprite.Sprite):
    def __init__(self, imagepath, size=None):
        super().__init__()

        if not image.get_extended():
            raise SpriteError("Fatal: extended image support not available. Canot open sprite.")

        # get original image as 8-bit since LUT operations are faster
        # than bitmap operations
        im = Image.open(imagepath)
        self.original_image = image.fromstring(im.tobytes(), im.size, "P")

        # create the palette
        palette = []
        rgb = []
        for val in im.getpalette():
            rgb.append(val)
            if len(rgb) == 3:
                palette.append(rgb + [255])
                rgb = []
        print (palette[0])
        self.original_image.set_palette(palette)
        self.original_image.set_colorkey([255,255,255])
        
        self.original_rect = self.original_image.get_rect()

        self.base_image = transform.scale(self.original_image, size)
        self.image = self.base_image
        self.rect = self.original_rect

        # how much the spinner has been rotated by
        self.angle = 0
        self.hueshift = 0

        self.times_taken = []

    def set_centre_pos(self, pos):
        self.original_rect.center = (pos[0], pos[1])

    def rotate(self, angle):
        self.angle += angle
        self.image = transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.original_rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_hueshift(self, hueshift):
        """Sets the hueshift of the image via a LUT operation"""
        self.hueshift = hueshift
        p = self.original_image.get_palette()
        if HAVE_NUMPY:
            p2 = shift_hue(np.array(p), self.hueshift)
        else:
            hsv = [list(rgb_to_hsv(*val)) for val in p]
            for i in range(len(hsv)):
                hsv[i][0] = (hsv[i][0]+self.hueshift)%1.0
            p2 = [hsv_to_rgb(*val) for val in hsv]
        self.base_image.set_palette(p2)
