# Andrea Abril Palencia Gutierrez, 18198
# DR2: Light and Shadows --- Graficas por computadora, seccion 20
# 14/09/2020 - 21/09/2020

from gl import Raytracer, color
from obj import Obj
from sphere import Sphere, Material,PointLight, AmbientLight
import random

# materiales
nieve = Material(diffuse = color(1, 1, 1 ))
negro = Material(diffuse = color(0, 0, 0 ))
nariz = Material(diffuse = color(1, 0.65, 0))
gris = Material(diffuse = color(0.77647, 0.76078, 0.77647))

imagen = Raytracer(800,1000)

imagen.pointLight = PointLight(position = (-1,1,2), intensity = 0.5)
imagen.ambientLight = AmbientLight(strength = 0.1)

# cuerpo
imagen.scene.append( Sphere((0, 0.8,  -5), 0.5, nieve) )
imagen.scene.append( Sphere((0, 0, -5), 0.6, nieve) )
imagen.scene.append( Sphere((0, -1, -5), 0.8, nieve) )
# nariz
imagen.scene.append( Sphere((0, 0.6,  -4), 0.07, nariz) )
# boca
imagen.scene.append( Sphere((-0.08, 0.4,  -4), 0.03, gris) )
imagen.scene.append( Sphere((0.08, 0.4,  -4), 0.03, gris) )
imagen.scene.append( Sphere((-0.20, 0.47,  -4), 0.03, gris) )
imagen.scene.append( Sphere((0.20, 0.47,  -4), 0.03, gris) )
# ojos
imagen.scene.append( Sphere((0.09, 0.8,  -4), 0.05, negro) )
imagen.scene.append( Sphere((-0.09, 0.8,  -4), 0.05, negro) )
imagen.scene.append( Sphere((-0.09, 0.6,  -3), 0.02, nieve) )
imagen.scene.append( Sphere((0.05, 0.6,  -3), 0.02, nieve) )

# botones
imagen.scene.append( Sphere((0, 0,  -4), 0.06, negro) )
imagen.scene.append( Sphere((0, -0.4,  -4), 0.07, negro) )
imagen.scene.append( Sphere((0, -0.8,  -4), 0.08, negro) )

imagen.rtRender()
imagen.glFinish('imagen.bmp')
print("LISTO! la imagen ya esta con el nombre de 'imagen.bmp' ")