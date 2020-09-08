# Andrea Abril Palencia Gutierrez, 18198
# DR1: Spheres and Materials --- Graficas por computadora, seccion 20
# 31/08/2020 - 07/09/2020

import struct
import random
import numpy as np
from numpy import matrix, cos, sin, tan
from obj import Obj
from mate import normal_fro

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

celeste = color(0.4745, 0.549, 0.9686)
rosado = color(0.98431, 0.74901, 0.988235)
negro = color(0,0,0)
blanco = color(1,1,1)
azul = color(0.015, 0.047, 0.227)

class Raytracer(object):
    def __init__(self, ancho, alto):
        self.curr_color = blanco
        self.clear_color = rosado
        self.glCreateWindow(ancho, alto)
        self.camPosition = (0,0,0)
        self.fov = 60
        self.scene = []

    def glCreateWindow(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.glClear()
        self.glViewport(0, 0, ancho, alto)

    def glViewport(self, x, y, ancho, alto):
        self.viewport_x = x
        self.viewport_y = y
        self.viewportancho = ancho
        self.viewportalto = alto

    def glClear(self):
        self.pixels = [ [ self.clear_color for x in range(self.ancho)] for y in range(self.alto) ]
        self.zbuffer = [ [ float('inf') for x in range(self.ancho)] for y in range(self.alto) ]

    def glVertex(self, x, y, color = None):
        if x < self.viewport_x or x >= self.viewport_x + self.viewportancho or y < self.viewport_y or y >= self.viewport_y + self.viewportalto:
            return

        if x >= self.ancho or x < 0 or y >= self.alto or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.curr_color
        except:
            pass

    def glColor(self, r, g, b):
        self.curr_color = color(r,g,b)

    def glClearColor(self, r, g, b):
        self.clear_color = color(r,g,b)

    def glFinish(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.ancho * self.alto * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.ancho))
        archivo.write(dword(self.alto))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.ancho * self.alto * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno
        for x in range(self.alto):
            for y in range(self.ancho):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.ancho * self.alto * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.ancho))
        archivo.write(dword(self.alto))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.ancho * self.alto * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.alto):
            for y in range(self.ancho):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.alto):
            for y in range(self.ancho):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth,depth,depth))

        archivo.close()

    def rtRender(self):
        #pixel por pixel
        for y in range(self.alto):
            for x in range(self.ancho):

                # pasar valor de pixel a coordenadas NDC (-1 a 1)
                Px = 2 * ( (x+0.5) / self.ancho) - 1
                Py = 2 * ( (y+0.5) / self.alto) - 1

                #FOV(angulo de vision), asumiendo que el near plane esta a 1 unidad de la camara
                t = tan( (self.fov * np.pi / 180) / 2 )
                r = t * self.ancho / self.alto
                Px *= r
                Py *= t

                #Nuestra camara siempre esta viendo hacia -Z
                direction = (Px, Py, -1)
                direction = direction / normal_fro(direction)

                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camPosition, direction)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material

                if material is not None:
                    self.glVertex(x, y, material.diffuse)

                











                











