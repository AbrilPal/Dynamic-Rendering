# Andrea Abril Palencia Gutierrez, 18198
# DR2: Light and Shadows --- Graficas por computadora, seccion 20
# 14/09/2020 - 21/09/2020

import struct
import random
import numpy as np
from numpy import matrix, cos, sin, tan
from obj import Obj, Envmap
from mate import normal_fro, resta_lis, division_lis_fro, punto, multi_N, multColor, sumVectors, mulVectors, multiply, subVectors, dotVectors

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3

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

def reflectVector(normal, dirVector):
    # R = 2 * (N dot L) * N - L
    reflect = 2 * np.dot(normal, dirVector)
    reflect = np.multiply(reflect, normal)
    reflect = np.subtract(reflect, dirVector)
    reflect = reflect / np.linalg.norm(reflect)
    return reflect

def refractVector(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    # Snell's Law
    cosi = max(-1, min(1, np.dot(I, N)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        N = np.array(N) * -1

    eta = etai/etat
    k = 1 - eta * eta * (1 - (cosi * cosi))

    if k < 0: # Total Internal Reflection
        return None
    
    R = eta * np.array(I) + (eta * cosi - k**0.5) * N
    return R / np.linalg.norm(R)

def fresnel(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    cosi = max(-1, min(1, np.dot(I, N)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1: # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    return (Rs * Rs + Rp * Rp) / 2

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
        self.dirLight = None
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

                self.glVertex(x, y, self.castRay(self.camPosition, direction))

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

    def scene_intercept(self, orig, direction, origObj = None):
        tempZbuffer = float('inf')
        intersect = None
        material = None

        for obj in self.scene:
            if obj is not origObj:
                hit = obj.ray_intersectt(orig, direction)
                if hit is not None:
                    if hit.distance < tempZbuffer:
                        tempZbuffer = hit.distance
                        material = obj.material
                        intersect = hit

        return material, intersect

    def castRay(self, orig, direction, origObj = None, recursion = 0):

        material, intersect = self.scene_intercept(orig, direction, origObj)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.envmap:
                return self.envmap.getColor(direction)
            return self.bitmap_color

        objectColor = [material.diffuse[2] / 255,
                       material.diffuse[1] / 255,
                       material.diffuse[0] / 255]

        ambientColor = [0,0,0]
        diffuseColor = [0,0,0]
        specColor = [0,0,0]

        reflectColor = [0,0,0]
        refractColor = [0,0,0]

        finalColor = [0,0,0]

        shadow_intensity = 0

        view_dir = subVectors(self.camPosition, intersect.point)
        view_dir = view_dir / normal_fro(view_dir)

        if self.ambientLight:
            ambientColor = [self.ambientLight.strength * self.ambientLight.color[2] / 255,
                            self.ambientLight.strength * self.ambientLight.color[1] / 255,
                            self.ambientLight.strength * self.ambientLight.color[0] / 255]

        if self.pointLight:
            light_dir = subVectors(self.pointLight.position, intersect.point)
            light_dir = light_dir / normal_fro(light_dir)

            intensity = self.pointLight.intensity * max(0, dotVectors(light_dir, intersect.normal))
            diffuseColor = [intensity * self.pointLight.color[2] / 255,
                            intensity * self.pointLight.color[1] / 255,
                            intensity * self.pointLight.color[2] / 255]

            reflect = reflectVector(intersect.normal, light_dir) 

            spec_intensity = self.pointLight.intensity * (max(0, dotVectors(view_dir, reflect)) ** material.spec)
            specColor = [spec_intensity * self.pointLight.color[2] / 255,
                         spec_intensity * self.pointLight.color[1] / 255,
                         spec_intensity * self.pointLight.color[0] / 255]


            shadMat, shadInter = self.scene_intercept(intersect.point,  light_dir, intersect.sceneObject)
            if shadInter is not None and shadInter.distance < normal_fro(subVectors(self.pointLight.position, intersect.point)):
                shadow_intensity = 1

        
        if material.matType == OPAQUE:
            finalColor = sumVectors(ambientColor, multiply((1 - shadow_intensity), sumVectors(diffuseColor, specColor)))
            if material.texture and intersect.texCoords:
                texColor = material.texture.getColor(intersect.texCoords[0], intersect.texCoords[1])

                finalColor *= np.array([texColor[2] / 255,
                                        texColor[1] / 255,
                                        texColor[0] / 255])

        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intersect.normal, direction * -1)
            reflectColor = self.castRay(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflectColor = [reflectColor[2] / 255,
                            reflectColor[1] / 255,
                            reflectColor[0] / 255]

            finalColor = sumVectors(reflectColor, multiply((1 - shadow_intensity), specColor))

        elif material.matType == TRANSPARENT:

            outside = dotVectors(direction, intersect.normal) < 0
            bias = 0.001 * intersect.normal
            kr = fresnel(intersect.normal, direction, material.ior)

            reflect = reflectVector(intersect.normal, direction * -1)
            reflectOrig = sumVectors(intersect.point, bias) if outside else subVectors(intersect.point, bias)
            reflectColor = self.castRay(reflectOrig, reflect, None, recursion + 1)
            reflectColor = [reflectColor[2] / 255,
                            reflectColor[1] / 255,
                            reflectColor[0] / 255]

            if kr < 1:
                refract = refractVector(intersect.normal, direction, material.ior)
                refractOrig = subVectors(intersect.point, bias) if outside else sumVectors(intersect.point, bias)
                refractColor = self.castRay(refractOrig, refract, None, recursion + 1)
                refractColor = [refractColor[2] / 255,
                                refractColor[1] / 255,
                                refractColor[0] / 255]

            # reflectColor * kr + refractColor * (1 - kr) + (1 - shadow_intensity) * specColor
            finalColor = sumVectors(sumVectors(multiply(kr, reflectColor), multiply((1-kr), refractColor)), multiply((1 - shadow_intensity), specColor))

        # finalColor *= objectColor
        finalColor = mulVectors(finalColor, objectColor)

        r = min(1,finalColor[0])
        g = min(1,finalColor[1])
        b = min(1,finalColor[2])

        return color(r, g, b)
