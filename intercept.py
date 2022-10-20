'''
*********************************************
Modulo do programa que calcula as Equações do
movimento robô para retornar uma lista com
todas as veriaveis 
*********************************************
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
vel_mag = 0

getData = []

data = []

def intersectionPoint(time, xo, yo, x, y):

    global t
    t = 0

    if (xo < 4.5 and yo > 3) or xo <= 2 and yo <= 3: # Bola no segundo quadrante
        time = time - (time * 0.20)
    else:
        time = time - (time * 0.40)

    velx = (x - xo) / time
    vely = (y - yo) / time

    vel_mag = pow(velx, 2) + pow(vely, 2)
    vel_mag = pow(vel_mag, 1/2)

    while time > t:

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
    getData.append(vel_mag)

    return getData




