# Andrea Abril Palencia Gutierrez, 18198
# Graficas por computadora, seccion 20
# 04/10/2020

def normal_fro(norm):
    return((norm[0]**2+norm[1]**2+norm[2]**2)**(1/2))
    
def resta_lis(x0, x1, y0, y1, z0, z1):
    arr_sub = []
    arr_sub.extend((x0 - x1, y0 - y1, z0 - z1))
    return arr_sub

def division_lis_fro(norm, frobenius):
    if (frobenius==0):
        resultado=[]
        resultado.append(float('NaN'))
        resultado.append(float('NaN'))
        resultado.append(float('NaN'))
        return resultado
    else:
        resultado=[]
        resultado.append(norm[0]/ frobenius)
        resultado.append(norm[1]/ frobenius)
        resultado.append(norm[2]/ frobenius)
        return resultado

def punto(normal, lightx, lighty, lightz):
    return (normal[0]*lightx+normal[1]*lighty+normal[2]*lightz)

def baryCoords(Ax, Bx, Cx, Ay, By, Cy, Px, Py):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((By - Cy)*(Px - Cx) + (Cx - Bx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        v = ( ((Cy - Ay)*(Px - Cx) + (Ax - Cx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

def M_Inverse(m):
    determinant = getMatrixDeternminant(m)
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

def getMatrixDeternminant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

def multiplicacion_M(matriz1, matriz2, c1, f1, c2, f2): 
    matriz3 = []
    for i in range(f1):
        matriz3.append( [0] * c2 )
    for i in range(f1):
        for j in range(c2):
            for k in range(f2):
                    numf=matriz1[i][k] * matriz2[k][j]
                    matriz3[i][j] += numf
    return matriz3

def cruz_lis(v0, v1):
    resultado=[]
    resultado.append(v0[1]*v1[2]-v1[1]*v0[2])
    resultado.append(-(v0[0]*v1[2]-v1[0]*v0[2]))
    resultado.append(v0[0]*v1[1]-v1[0]*v0[1])
    return resultado

def mult_M(v, m): 
    c = []
    for i in range(0,len(v)):
        temp=[]
        for j in range(0,len(m[0])):
            s = 0
            for k in range(0,len(v[0])):
                s += v[i][k]*m[k][j]
            temp.append(s)
        c.append(temp)
    return c

def zeros_matrix(rows, cols):
    m = []
    while len(m) < rows:
        m.append([])
        while len(m[-1]) < cols:
            m[-1].append(0.0)

    return m

def multi_N(c, normal):
    return (normal[0]*c,normal[1]*c,normal[2]*c)

def multColor(v1,v2):
    res=[]
    res.append(v1[0]*v2[0])
    res.append(v1[1]*v2[1])
    res.append(v1[2]*v2[2])
    return res

def sumVectors(vec1, vec2):
    sumList = []
    sumList.extend((vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2]))
    return sumList

def mulVectors(vec1, vec2):
    mulList = []
    mulList.extend((vec1[0] * vec2[0], vec1[1] * vec2[1], vec1[2] * vec2[2]))
    return mulList

def multiply(dotNumber, normal):
    arrMul = []
    arrMul.extend((dotNumber * normal[0], dotNumber * normal[1], dotNumber * normal[2]))
    return arrMul

def subVectors(vec1, vec2):
    subList = []
    subList.extend((vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2]))
    return subList