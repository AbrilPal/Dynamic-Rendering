import numpy as np
from gl import color
from mate import punto, resta_lis, normal_fro, sumVectors, multiply, subVectors, division_lis_fro, add, multi_N
from numpy import arccos, arctan2 

WHITE = color(1,1,1)
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0, matType = OPAQUE, ior = 1, texture = None):
        # color pero se esparce cuando tiene luz
        self.diffuse = diffuse
        self.spec = spec
        self.matType = matType
        self.ior = ior
        self.texture = texture


class Intersect(object):
    def __init__(self, distance, point, normal, texCoords, sceneObject):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texCoords = texCoords
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

        u = 1 - (arctan2( norm[2], norm[0]) / (2 * np.pi) + 0.5)
        v =  arccos(-norm[1]) / np.pi

        uvs = [u, v]

        return Intersect(distance = t0,
                         point = hit,
                         normal = norm,
                         texCoords = uvs,
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

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = division_lis_fro(normal, normal_fro(normal))
        self.material = material

    def ray_intersectt(self, orig, dir):
        denom = punto(dir, self.normal[0], self.normal[1], self.normal[2])

        if abs(denom) > 0.0001:
            val2=resta_lis(self.position[0], orig[0], self.position[1], orig[1], self.position[2], orig[2])
            t = punto(self.normal, val2[0],val2[1],val2[2])/denom
            if t > 0:
                # P = O + tD
                hit = add(orig, multi_N(t, dir))
                return Intersect(distance = t,
                                 point = hit,
                                 normal = self.normal,
                                 texCoords = None,
                                 sceneObject = self)

        return None

class AABB(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        halfSize = size / 2

        self.planes.append( Plane( add(position, (halfSize,0,0)), (1,0,0), material))
        self.planes.append( Plane( add(position, (-halfSize,0,0)), (-1,0,0), material))

        self.planes.append( Plane( add(position, (0,halfSize,0)), (0,1,0), material))
        self.planes.append( Plane( add(position, (0,-halfSize,0)), (0,-1,0), material))

        self.planes.append( Plane( add(position, (0,0,halfSize)), (0,0,1), material))
        self.planes.append( Plane( add(position, (0,0,-halfSize)), (0,0,-1), material))


    def ray_intersectt(self, orig, dir):

        epsilon = 0.001

        boundsMin = [0,0,0]
        boundsMax = [0,0,0]

        for i in range(3):
            boundsMin[i] = self.position[i] - (epsilon + self.size / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size / 2)

        t = float('inf')
        intersect = None

        uvs = None

        for plane in self.planes:
            planeInter = plane.ray_intersectt(orig, dir)

            if planeInter is not None:

                # Si estoy dentro del bounding box
                if planeInter.point[0] >= boundsMin[0] and planeInter.point[0] <= boundsMax[0]:
                    if planeInter.point[1] >= boundsMin[1] and planeInter.point[1] <= boundsMax[1]:
                        if planeInter.point[2] >= boundsMin[2] and planeInter.point[2] <= boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal[0]) > 0:
                                    # mapear uvs para eje x. Uso coordenadas en Y y Z.
                                    u = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[1]) > 0:
                                    # mapear uvs para eje y. Uso coordenadas en X y Z.
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[2]) > 0:
                                    # mapear uvs para eje Z. Uso coordenadas en X y Y.
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])

                                uvs = [u, v]

        if intersect is None:
            return None

        return Intersect(distance = intersect.distance,
                         point = intersect.point,
                         normal = intersect.normal,
                         texCoords = uvs,
                         sceneObject = self)
