'''
*****************************************
WELCOME TO PYTHON CLASSES AND INHERITANCE
COURSE FROM MICHIGAN UNIVERSITY
*****************************************
'''
from ast import Global
from cmath import sqrt
import matplotlib.pyplot as plt
import numpy as np
from pyparsing import lineStart
from variables import *

dt = 0.002
vx = 2.12
vy = 1

data_x = []
data_y = []
data_t = []
data_velx = []
data_vely = []

velx = 0
vely = 0

getData = []

data = []

def intersectionPoint(time, xo, yo, x, y):

    global t
    t = 0

    if xo < 4.5 and yo > 3: # Bola no segundo quadrante
        time = time - (time * 0.10)
    else:
        time = time - (time * 0.5)

    velx = (x - xo) / time
    vely = (y - yo) / time

    while time > t:

        #calculo feito para x0 = 3 e y0 = 6
        x = xo + velx * t
        data_x.append(x)

        y = yo + vely * t
        data_y.append(y)

        t = t + dt
        data_t.append(t)

        data_velx.append(velx)
        data_vely.append(vely)
    
    getData.append(data_x)
    getData.append(data_y)
    getData.append(data_t)
    getData.append(data_velx)
    getData.append(data_vely)

    return getData




