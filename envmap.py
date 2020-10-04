import struct
import numpy as np
from numpy import arccos, arctan2 
from gl import color

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        image = open(self.path, 'rb')
        image.seek(10)
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(14 + 4)
        self.width = struct.unpack('=l', image.read(4))[0]
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)

        self.pixels = []

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1)) / 255
                g = ord(image.read(1)) / 255
                r = ord(image.read(1)) / 255
                self.pixels[y].append(color(r,g,b))

        image.close()

    def getColor(self, direction):

        direction = direction / np.linalg.norm(direction)

        x = int( (arctan2( direction[2], direction[0]) / (2 * np.pi) + 0.5) * self.width)
        y = int( arccos(-direction[1]) / np.pi * self.height )

        return self.pixels[y][x]
