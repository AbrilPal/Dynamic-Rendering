# Andrea Abril Palencia Gutierrez, 18198
# DR2: Light and Shadows --- Graficas por computadora, seccion 20
# 14/09/2020 - 21/09/2020

from gl import Raytracer, color
from obj import Obj, Envmap
from sphere import Sphere, Material, PointLight, AmbientLight, Plane, AABB
import random
from textura import Texture

# materiales
suelo = Material(diffuse= color(0, 1, 0), spec = 64)
madera = Material(texture = Texture('madera.bmp'))
grama = Material(texture= Texture('hoja.bmp'))
ladrillo = Material(texture= Texture('piedra.bmp'))

imagen = Raytracer(900,600)
imagen.envmap = Envmap('cielo-atardecer.bmp')

imagen.pointLight = PointLight(position = (0,2,0), intensity = 0.5)
imagen.ambientLight = AmbientLight(strength = 0.2)

# tierra
imagen.scene.append( Plane((0, -4, 0), (0,1,0), suelo) )
# arbol 1
# tronco
imagen.scene.append(AABB((-5, -3.5, -7), 1, madera))
imagen.scene.append(AABB((-5, -2.5, -7), 1, madera))
imagen.scene.append(AABB((-5, -1.5, -7), 1, madera))
imagen.scene.append(AABB((-5, -0.5, -7), 1, madera))
# hojas
imagen.scene.append(Sphere((-4.9, 0.2,-6), 1.2, grama))
imagen.scene.append(Sphere((-3.9, 0,-7), 1.5, grama))
imagen.scene.append(Sphere((-4.9, 1.6,-8), 1, grama))
# castillo
# estructura
imagen.scene.append(AABB((5, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((5, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((5, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((3, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((3, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((3, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((1, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((1, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((-5, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((-5, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((-5, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((-3, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((-3, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((-3, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((-1, 1, -30), 2, ladrillo))
# #torre 1
imagen.scene.append(AABB((9, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((9, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((9, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((9, 3, -30), 2, ladrillo))
imagen.scene.append(AABB((9, 5, -30), 2, ladrillo))
# imagen.scene.append(AABB((9, 7, -30), 2, ladrillo))
# imagen.scene.append(AABB((9, 9, -30), 2, ladrillo))
imagen.scene.append(AABB((7, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((7, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((7, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((7, 3, -30), 2, ladrillo))
imagen.scene.append(AABB((7, 5, -30), 2, ladrillo))
# imagen.scene.append(AABB((7, 7, -30), 2, ladrillo))
# imagen.scene.append(AABB((7, 9, -30), 2, ladrillo))
#torre 2
imagen.scene.append(AABB((-9, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((-9, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((-9, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((-9, 3, -30), 2, ladrillo))
imagen.scene.append(AABB((-9, 5, -30), 2, ladrillo))
# imagen.scene.append(AABB((-9, 7, -30), 2, ladrillo))
# imagen.scene.append(AABB((-9, 9, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, -3, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, -1, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, 1, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, 3, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, 5, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, 7, -30), 2, ladrillo))
imagen.scene.append(AABB((-7, 9, -30), 2, ladrillo))
# arbol 2
# tronco
imagen.scene.append(AABB((13, -3.5, -25), 1, madera))
imagen.scene.append(AABB((13, -2.5, -25), 1, madera))
imagen.scene.append(AABB((13, -1.5, -25), 1, madera))
imagen.scene.append(AABB((13, -0.5, -25), 1, madera))
# hojas
imagen.scene.append(Sphere((12, 0.2,-24), 1.2, grama))
imagen.scene.append(Sphere((13, 0,-25), 1.5, grama))
imagen.scene.append(Sphere((14.5, 1,-26), 1, grama))
# arbol 3
# tronco
imagen.scene.append(AABB((16, -3.5, -20), 1, madera))
imagen.scene.append(AABB((16, -2.5, -20), 1, madera))
imagen.scene.append(AABB((16, -1.5, -20), 1, madera))
imagen.scene.append(AABB((16, -0.5, -20), 1, madera))
# hojas
imagen.scene.append(Sphere((14.3, 0.5,-19.7), 1.2, grama))
imagen.scene.append(Sphere((16, 0,-20), 1.5, grama))



imagen.rtRender()
imagen.glFinish('imagen.bmp')
print("LISTO! la imagen ya esta con el nombre de 'imagen.bmp' ")