# Andrea Abril Palencia Gutierrez, 18198
# DR1: Spheres and Materials --- Graficas por computadora, seccion 20
# 31/08/2020 - 07/09/2020

# libreria
import struct
from obj import Obj
from textura import Texture
import numpy as np
from numpy import matrix, cos, sin, tan

# para especificar cuanto tamaño quiero guardar en bytes de cada uno
def char(c):
    # solo un byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # solo 2 bytes
    return struct.pack('=h', w)

def dword(d):
    # solo 4 bytes
    return struct.pack('=l', d)

def convertir(co):
    # 1 ------ 255
    # x ------ y
    color_r = co * 255
    return int(color_r)
    
def color(r, g, b):
    return bytes([int(b), int(g), int(r)])

# colores predeterminados
azul = color(4,12,58)
negro = color(0,0,0)
blanco = color(255,255,255)

# clase principal
class Raytracer(object):
    # inicializa cualquier objeto dentro de la clase Render
    def __init__(self, ancho, alto):
        self.glCreateWindow(ancho, alto)
        # color predeterminado del punto en la pantalla
        self.punto_color = negro
        # camara
        self.camPosition = [0, 0, 0]
        self.fov = 60
        #scena
        self.scene = []

    def glCreateWindow(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.glClear()
        self.glViewPort(0, 0, ancho, alto)

    def glViewPort(self, x, y, ancho, alto):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_ancho = ancho
        self.viewport_alto = alto

    # fondo de toda la imagen
    def glClear(self):
        # color de fondo
        self.pixels = [[azul for x in range(self.ancho)] for y in range(self.alto)]
        self.zbuffer = [ [ -float('inf') for x in range(self.ancho)] for y in range(self.alto) ]

    # crear un punto en cualquier lugar de la pantalla 
    def glVertex(self, x, y, color = None):
        if x < self.viewport_x or x >= self.viewport_x + self.viewport_ancho or y < self.viewport_x or y >= self.viewport_x + self.viewport_alto:
            return

        if x >= self.ancho or x < 0 or y >= self.alto or y < 0:
            return
        try:
            self.pixels[y][x] = color or self.punto_color
        except:
            pass

    # permite cambiar el color del punto
    def glColor(self, color_p):
        self.punto_color = color_p

    # hacer lineas
    def  glLine( self , x0 , y0 , x1 , y1 ):
        # coordenasdas en pixeles
        # x0 = int((x0 + 1) * (self.viewport_ancho/2) + self.viewport_x)
        # y0 = int((y0 + 1) * (self.viewport_alto/2) + self.viewport_y)
        # x1 = int((x1 + 1) * (self.viewport_ancho/2) + self.viewport_x)
        # y1 = int((y1 + 1) * (self.viewport_alto/2) + self.viewport_y)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        inclinado = dy > dx

        if inclinado:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        desplazamiento = 0
        limit = 0.5
        
        # si es division por cero el programa no ejecuta nada
        try:
            m = dy/dx
            y = y0

            for x in range(x0, x1 + 1):
                if inclinado:
                    self.glVertex(y, x)
                else:
                    self.glVertex(x, y)

                desplazamiento += m
                if desplazamiento >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1
        except ZeroDivisionError:
            pass

    # hace el zbuffer de la imagen
    def glZBuffer(self, filename):
        imagen = open(filename, 'wb')

        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14 + 40 + self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(14 + 40))

        imagen.write(dword(40))
        imagen.write(dword(self.ancho))
        imagen.write(dword(self.alto))
        imagen.write(word(1))
        imagen.write(word(24))
        imagen.write(dword(0))
        imagen.write(dword(self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))

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
                imagen.write(color(depth,depth,depth))

        imagen.close()

    # escribe el imagen
    def glFinish(self, name):
        imagen = open(name, 'wb')
        imagen.write(bytes('B'.encode('ascii')))
        imagen.write(bytes('M'.encode('ascii')))
        imagen.write(dword(14 + 40 + self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(14 + 40))
        imagen.write(dword(40))
        imagen.write(dword(self.ancho))
        imagen.write(dword(self.alto))
        imagen.write(word(1))
        imagen.write(word(24))
        imagen.write(dword(0))
        imagen.write(dword(self.ancho * self.alto * 3))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))
        imagen.write(dword(0))

        for x in range(self.alto):
            for y in range(self.ancho):
                imagen.write(self.pixels[x][y])
                
        imagen.close()

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
                direction = [Px, Py, -1]
                direction = direction / np.linalg.norm(direction)

                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camPosition, direction)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material

                if material is not None:
                    self.glVertex(x, y, material.diffuse)
