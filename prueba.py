from gl import Raytracer, color
from obj import Obj
from sphere import Sphere, Material
import random

nieve = Material(diffuse = color(1, 1, 1 ))
negro = Material(diffuse = color(0, 0, 0 ))
rojo = Material(diffuse = color(1, 0, 0))

imagen = Raytracer(500,300)

imagen.scene.append( Sphere((0, 20, -70), 10, nieve) )
imagen.scene.append( Sphere((0, 10, -37), 1, rojo) )
imagen.scene.append( Sphere((0, 12, -65), 1, negro) )
imagen.scene.append( Sphere((0, -9, -25), 1, negro) )
imagen.scene.append( Sphere((0, -5, -30), 1, negro) )
imagen.scene.append( Sphere((0, 0, -30), 1, negro) )
imagen.scene.append( Sphere((0, 0, -68), 12, nieve) )
imagen.scene.append( Sphere((0, -20, -66), 14, nieve) )
 
imagen.rtRender()

imagen.glFinish('imagen.bmp')