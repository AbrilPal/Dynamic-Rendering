from gl import Raytracer, color
from obj import Obj
from sphere import Sphere, Material
import random

brick = Material(diffuse = color(0.8, 0.25, 0.25 ))
stone = Material(diffuse = color(0.4, 0.4, 0.4 ))
grass = Material(diffuse = color(0.5, 1, 0))

imagen = Raytracer(500,300)

imagen.scene.append( Sphere([0, 0, -7], 1, brick) )
imagen.scene.append( Sphere([1, 1, -10], 1, stone) )
imagen.scene.append( Sphere([-1.5, -1.5, -13], 1, grass) )
 
imagen.rtRender()

imagen.glFinish('imagen.bmp')