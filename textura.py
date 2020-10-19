import struct

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
        
    def read(self):
        imagen = open(self.path, 'rb')
        imagen.seek(10)
        headerSize = struct.unpack('=l', imagen.read(4))[0]

        imagen.seek(14 + 4)
        self.ancho = struct.unpack('=l', imagen.read(4))[0]
        self.alto = struct.unpack('=l', imagen.read(4))[0]
        imagen.seek(headerSize)

        self.pixels = []

        for y in range(self.alto):
            self.pixels.append([])
            for x in range(self.ancho):
                b = ord(imagen.read(1)) / 255
                g = ord(imagen.read(1)) / 255
                r = ord(imagen.read(1)) / 255
                self.pixels[y].append(color(r,g,b))

        imagen.close()

    def getColor(self, tx, ty):
        if tx >= 0 and tx <= 1 and ty >= 0 and ty <= 1:
            x = int(tx * self.ancho)
            y = int(ty * self.alto)

            return self.pixels[y][x]
        else:
            return color(0,0,0)