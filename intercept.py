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

a_x = 0
a_y = 0
v_xo = 0
v_yo = 0

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

    timeToBall = float(input("Tempo de interceptação do robô de 10 a 90%: "))
    global t
    global v_x
    global v_y

    timeToBall = timeToBall / 100
    
    t = 0

    if (xo < 4.5 and yo > 3) or xo <= 2 and yo <= 3: # Bola no segundo quadrante
        time = time - (time * timeToBall)
    else:
        time = time - (time * timeToBall)

    velx = (x - xo) / time
    vely = (y - yo) / time

    a_x = velx / time
    a_y = vely / time

    while time > t:

        v_x = v_xo + a_x * t
        x = xo + velx * t
        
        data_x.append(x)

        v_y = v_yo + a_y * t
        y = yo + vely * t
        
        data_y.append(y)

        t = t + dt
        data_t.append(t)

        vel_mag = pow(v_x, 2) + pow(v_y, 2)
        vel_mag = pow(vel_mag, 1/2)

        
        if t >= time - (time * 0.5):
            t_const = time - (time * 0.5)
            v_x = v_xo + a_x * t_const
            v_y = v_yo + a_y * t_const

            vel_mag = pow(v_x, 2) + pow(v_y, 2)
            vel_mag = pow(vel_mag, 1/2)

            data_velx.append(v_x)
            data_vely.append(v_y)

        else:
            data_velx.append(v_x)
            data_vely.append(v_y)
    
    getData.append(data_x)
    getData.append(data_y)
    getData.append(data_t)
    getData.append(data_velx)
    getData.append(data_vely)
    getData.append(vel_mag)

    return getData




