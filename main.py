from cProfile import label
from glob import glob
from xmlrpc.server import resolve_dotted_attribute
import numpy as np
import matplotlib.pyplot as plt
from intercept import intersectionPoint
from variables import *

'''
==================================
EQUAÇÕES DE MOVIMENTO DA BOLA EM X
==================================
x(t) = -0.007t³ - 0.17t² + 2.5t + 1
dx(t)/dt = -0.021t² - 0.34t + 2.5
d²x(t)/dt² = -0.042t - 0.34


==================================
EQUAÇÕES DE MOVIMENTO DA BOLA EM Y
==================================
y(t) = -0.2t² + 1.8t + 0.7
dy(t)/dt = -0.4t + 1.8
d²y(t)/dt² = -0.4

'''


'''
*
Inicialização dos vetores tempo e posição em x, y e o vetor tempo
leitura do arquivo de texto com as dados de tempo
*
'''
time = []
x_pos = []
y_pos = []

ball_yvel = []
ball_xvel = []

data = np.loadtxt(fname = 'time.txt')
for i in data:
    time.append(i)

'''
*
Equação de movimento em x em função do tempo 
com os valores da posição para o intervalo de [0,20,0.02]
*
'''
for i in range(len(time)):
    #x(t) = -0.007t³ - 0.17t² + 2.5t + 1

    x = -0.007*time[i]**3 - 0.17*time[i]**2 + 2.5*time[i] + 1
    x_vel = -0.021*time[i]**2 - 0.34*time[i] + 2.5

    x_pos.append(x)
    ball_xvel.append(x_vel)

'''
*
Equação de movimento em y em função do tempo 
com os valores da posição para o intervalo de [0,20,0.02]
*
'''
for i in range(len(time)):
    #y(t) = -0.2t² + 1.8t + 0.7

    y = -0.2*time[i]**2 + 1.8*time[i] + 0.7
    y_vel = -0.2*time[i] + 1.8

    y_pos.append(y)
    ball_yvel.append(y_vel)

    


'''
*
Inicialização da classe para o calculo da posição
relativa entre a bola e o robo como vetores de posição
*
'''
class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, p):
        import math
        delta_x = self.x - p.x
        delta_y = self.y - p.y
        return math.sqrt(delta_x**2 + delta_y**2)
    
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"



'''
Equações do Movimento do Robô
'''
x_robotInitial = 0
y_robotInitial = 6

vx_robot = 0
vy_robot = 0

vxmax_robot = 2.10
vymax_robot = 0.3
raio_bolaRobo = 0.03
tempo = 0

relativeDist = []
min_dist = 0

xo = float(input("Digite o valor inicial xo: "))
yo = float(input("Digite o valor inicial yo: "))

for i in range(len(time)):

    bola = Coordinate(x_pos[i], y_pos[i])
    robot = Coordinate(xo, yo)
    relativeDist.append(bola.distance(robot))


    #print("robot = ({}, {}) bola = ({:.2f}, {:.2f}) Dist = {:.2f} t = {}" .format(xo, yo, x_pos[i], y_pos[i], bola.distance(robot), time[i]))
        


robot_data = []

def min_distance():

    global new_time
    global ballx_pos
    global bally_pos

    min = relativeDist[0]
    #ballx_pos = 0
    #bally_pos = 0
    #new_time = 0

    for i in range(len(relativeDist)):
        if(relativeDist[i] < min):
            min = relativeDist[i]
            ballx_pos = x_pos[i]
            bally_pos = y_pos[i]
            new_time = time[i]
        
    print("Min value is {:.2f} in time {:.2f} at bola = ({:.2f}, {:.2f})"  .format( min, new_time, ballx_pos, bally_pos))

min_distance()

robot_data = intersectionPoint(new_time, xo, yo, ballx_pos, bally_pos)



#===================================================
#--------- Gráfico da Trajetória da bola------------
#-------- e Posição de interceptação do Robô -------
#===================================================
fig, axs = plt.subplots(nrows=2, ncols=2)

axs[0][0].plot(xo, yo, color='none', linestyle = 'dashed', linewidth = 2,
marker = 'o', markersize = 6, markerfacecolor = 'blue', markeredgecolor = 'blue')
axs[0][0].plot(robot_data[0], robot_data[1], label='Bola (x,y) pos', color='blue', linewidth = 0.75)
axs[0][0].plot(x_pos, y_pos, label='Bola (x,y) pos', color='orange')


axs[0][0].legend(loc="upper left", shadow=True, fontsize="small")
axs[0][0].set_xlim(0,9)
axs[0][0].set_ylim(0,6)
axs[0][0].set_xlabel("x (m)")
axs[0][0].set_ylabel("y (m)")
axs[0][0].set_title("Gráfico da trajetória da bola\n e do robô até a interceptção")
axs[0][0].grid()
plt.grid()

#===================================================
#--------- Gráfico da posição x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[1][0].plot(robot_data[robot_time], robot_data[robot_xpos], label='posição x do robô')
axs[1][0].plot(robot_data[robot_time], robot_data[robot_ypos], label='posição y do robô')

axs[1][0].legend(loc="upper left", shadow=True, fontsize="small")
axs[1][0].legend(loc="upper left", shadow=True, fontsize="small")
axs[1][0].set_xlim(0,new_time)
axs[1][0].set_ylim(0, 9)
axs[1][0].set_xlabel("temp t (s)")
axs[1][0].set_ylabel("posição em x (m)")
axs[1][0].set_title("Gráfico x e y da posição\n do robô em função do tempo")
axs[1][0].grid()
plt.grid()


#===================================================
#--------- Gráfico da velocidade x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[0][1].plot(robot_data[robot_time], robot_data[robot_xvel])
axs[0][1].plot(robot_data[robot_time], robot_data[robot_yvel])

axs[0][1].legend(loc="upper left", shadow=True, fontsize="small")
axs[0][1].set_xlim(0,new_time)
axs[0][1].set_ylim(-2, 2)
axs[0][1].set_xlabel("temp t (s)")
axs[0][1].set_ylabel("posição em x (m)")
axs[0][1].set_title("Gráfico x e y da posição\n do robô em função do tempo")
axs[0][1].grid()
plt.grid()


#===================================================
#--------- Gráfico da velocidade x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[1][1].plot(time, ball_xvel)
axs[1][1].plot(time, ball_yvel)

axs[1][1].legend(loc="upper left", shadow=True, fontsize="small")
axs[1][1].set_xlabel("temp t (s)")
axs[1][1].set_ylabel("posição em x (m)")
axs[1][1].set_title("Gráfico da velocidade x\n da bola em função do tempo")
axs[1][1].grid()
plt.grid()

plt.tight_layout()
plt.show()


#fig1.savefig('fig1.png')





    