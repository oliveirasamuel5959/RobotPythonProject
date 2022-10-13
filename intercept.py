'''
*****************************************
WELCOME TO PYTHON CLASSES AND INHERITANCE
COURSE FROM MICHIGAN UNIVERSITY
*****************************************
'''
from ast import Global
import matplotlib.pyplot as plt
import numpy as np
from pyparsing import lineStart


dt = 0.002
vx = 2.12
vy = 1

data_x = []
data_y = []
data_t = []

velx = 0
vely = 0

getData = []

data = []


def intersectionPoint(time, xo, yo, x, y):

    global t
    t = 0

    time = time - (time * 0.15)

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
    
    getData.append(data_x)
    getData.append(data_y)
    getData.append(data_t)

    return getData

#data = intersectionPoint(1.5, 5, 3, 4.84, 3.25)



