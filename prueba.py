# Andrea Abril Palencia Gutierrez, 18198
# DR2: Light and Shadows --- Graficas por computadora, seccion 20
# 14/09/2020 - 21/09/2020

from gl import Raytracer, color
from obj import Obj, Envmap
from sphere import Sphere, Material, PointLight, AmbientLight, Plane, AABB
import random

# materiales
suelo = Material(diffuse = color(0.924, 0.92, 0.908 ), spec = 64)
paredes = Material(diffuse = color(0.972, 0.716, 0.972 ), spec = 64)
techo = Material(diffuse= color(1, 0.996, 0.928), spec = 64)

imagen = Raytracer(500,500)
imagen.envmap = Envmap('envmap.bmp')

imagen.pointLight = PointLight(position = (0,0,0), intensity = 1)
imagen.ambientLight = AmbientLight(strength = 0.1)

# cuarto
imagen.scene.append( Plane((0, 3, 0), (0,-1,0), techo) )  
imagen.scene.append( Plane((0, -3, 0), (0,1,0), suelo) )


imagen.rtRender()
imagen.glFinish('imagen.bmp')
print("LISTO! la imagen ya esta con el nombre de 'imagen.bmp' ")