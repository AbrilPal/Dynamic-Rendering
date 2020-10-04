# Andrea Abril Palencia Gutierrez, 18198
# DR2: Light and Shadows --- Graficas por computadora, seccion 20
# 14/09/2020 - 21/09/2020

import struct
import random
import numpy as np
from numpy import matrix, cos, sin, tan
from obj import Obj
from mate import normal_fro, resta_lis, division_lis_fro, punto, multi_N, multColor, sumVectors, mulVectors, multiply

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
        self.pointLight = None
        self.ambientLight = None

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
                intersectV = None

                for obj in self.scene:
                    intersect = obj.ray_intersectt(self.camPosition, direction)
                    if intersect is not None:
                        if intersect.distance < self.zbuffer[y][x]:
                            self.zbuffer[y][x] = intersect.distance
                            material = obj.material
                            intersectV = intersect

                if intersectV is not None:
                    self.glVertex(x, y, self.pointColor(material, intersectV))

    def pointColor(self, material, intersect):
        objectColor = [material.diffuse[2] / 255,
                    material.diffuse[1] / 255,
                    material.diffuse[0] / 255]

        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specColor = [0,0,0]

        shadow_intensity = 0

        if self.ambientLight:
            ambientColor = [self.ambientLight.strength * self.ambientLight.color[2] / 255,
                            self.ambientLight.strength * self.ambientLight.color[1] / 255,
                            self.ambientLight.strength * self.ambientLight.color[0] / 255]

        if self.pointLight:
            # Sacamos la direccion de la luz para este punto
            light_dirp = resta_lis(self.pointLight.position[0], intersect.point[0], self.pointLight.position[1], intersect.point[1], self.pointLight.position[2], intersect.point[2])
            light_dirp = division_lis_fro(light_dirp, normal_fro(light_dirp))

            # Calculamos el valor del diffuse color
            intensityp = self.pointLight.intensity * max(0, punto(light_dirp, intersect.normal[0],intersect.normal[1],intersect.normal[2]))
            diffuseColor = [intensityp * self.pointLight.color[2] / 255,
                            intensityp * self.pointLight.color[1] / 255,
                            intensityp * self.pointLight.color[2] / 255]

            # Iluminacion especular
            view_dirp = resta_lis(self.camPosition[0], intersect.point[0], self.camPosition[1], intersect.point[1], self.camPosition[2], intersect.point[2])
            view_dirp = division_lis_fro(view_dirp, normal_fro(view_dirp))

            reflectp=2*(punto(intersect.normal, light_dirp[0],light_dirp[1],light_dirp[2]))
            reflectp=multi_N(reflectp, intersect.normal)
            reflectp=resta_lis(reflectp[0], light_dirp[0],reflectp[1], light_dirp[1],reflectp[2], light_dirp[2])
            spec_intensity = self.pointLight.intensity * (max(0, punto(view_dirp, reflectp[0],reflectp[1],reflectp[2])) ** material.spec)

            specColor = [spec_intensity * self.pointLight.color[2] / 255,
                        spec_intensity * self.pointLight.color[1] / 255,
                        spec_intensity * self.pointLight.color[0] / 255]

            for obj in self.scene:
                if obj is not intersect.sceneObject:
                    hit = obj.ray_intersectt(intersect.point,  light_dirp)
                    if hit is not None and intersect.distance < normal_fro(resta_lis(self.pointLight.position[0], intersect.point[0],self.pointLight.position[1], intersect.point[1],self.pointLight.position[2], intersect.point[2])):
                        shadow_intensity = 1

        # Formula de iluminacion
        finalColorp = mulVectors(sumVectors(ambientColor, multiply((1 - shadow_intensity), sumVectors(diffuseColor, specColor))), objectColor)

        r = min(1,finalColorp[0])
        g = min(1,finalColorp[1])
        b = min(1,finalColorp[2])

        return color(r, g, b)
