# Andrea Abril Palencia Gutierrez, 18198
# Graficas por computadora, seccion 20
# 17/08/2020 - 24/08/2020

# carga de archivo obj
class Obj(object):
    def __init__(self, filename):
        # leer el archivo obj
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.read()

    def read(self):
        for line in self.lines:
            # esto depende del modelo, porque no todos tienen la misma estructura
            if line:
               if len(line) > 0 :
                    if line[0] != '#' :
                        prefix, value = line.split(' ', 1)
                        value = value.strip().replace('//','/').replace('  ',' ')

                        if prefix == 'v':
                            self.vertices.append(list(map(float,value.split(' '))))
                        elif prefix == 'f':
                            nvalue = value.strip()
                            self.faces.append([list(map(int, face.split('/'))) for face in nvalue.split(' ')])
                        elif prefix == 'vn':
                            nvalue = value.strip()
                            self.normals.append(list(map(float,value.split(' '))))
                        elif prefix == 'vt':
                            nvalue = value.strip()
                            self.texcoords.append(list(map(float,value.split(' '))))

