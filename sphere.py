import numpy as np
from gl import color
from mate import punto, resta_lis, normal_fro, sumVectors, multiply, subVectors

WHITE = color(1,1,1)

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0):
        self.diffuse = diffuse
        self.spec = spec


class Intersect(object):
    def __init__(self, distance, point, normal, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObject = sceneObject

class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersectt(self, orig, dir):
        L = resta_lis(self.center[0],orig[0],self.center[1],orig[1],self.center[2],orig[2])
        tca = punto(L,dir[0], dir[1], dir[2])
        l = normal_fro(L) # magnitud de L
        d = (l**2 - tca**2) ** 0.5
        if d > self.radius:
            return None

        # thc es la distancia de P1 al punto perpendicular al centro
        thc = (self.radius ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0: 
            return None


        hit = sumVectors(orig, multiply(t0, dir))
        norm = subVectors( hit, self.center )
        norm = norm / normal_fro(norm)

        return Intersect(distance = t0,
                         point = hit,
                         normal = norm,
                         sceneObject = self)


class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color

class PointLight(object):
    def __init__(self, position = (0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color