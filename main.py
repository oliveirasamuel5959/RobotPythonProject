from cProfile import label
from glob import glob
from tkinter import font
from xmlrpc.server import resolve_dotted_attribute
import numpy as np
import matplotlib.pyplot as plt
from intercept import intersectionPoint
from variables import *


#==============================================
#----- EQUAÇÕES DE MOVIMENTO DA BOLA EM x -----
#==============================================
# x(t) = -0.007t³ - 0.17t² + 2.5t + 1
# dx(t)/dt = -0.021t² - 0.34t + 2.5
# d²x(t)/dt² = -0.042t - 0.34


#==============================================
#----- EQUAÇÕES DE MOVIMENTO DA BOLA EM y -----
#==============================================
# y(t) = -0.2t² + 1.8t + 0.7
# dy(t)/dt = -0.4t + 1.8
# d²y(t)/dt² = -0.4



data = np.loadtxt(fname = 'time.txt')
for i in data:
    time.append(i)

#=====================================================================
#------------ Equações de movimento da componente x ------------------
#---- da bola em função do tempo para o intervalo [0, 20, 0.02] ------
#======================================================================
for i in range(len(time)):
    x = -0.007*time[i]**3 - 0.17*time[i]**2 + 2.5*time[i] + 1
    x_vel = -0.021*time[i]**2 - 0.34*time[i] + 2.5
    x_accel = -0.042*time[i] - 0.34

    x_pos.append(x)
    ball_xvel.append(x_vel)
    ball_xaccel.append(x_accel)


#=====================================================================
#------------ Equações de movimento da componente y ------------------
#---- da bola em função do tempo para o intervalo [0, 20, 0.02] ------
#=====================================================================
for i in range(len(time)):
    y = -0.2*time[i]**2 + 1.8*time[i] + 0.7
    y_vel = -0.2*time[i] + 1.8
    y_accel = -0.2

    y_pos.append(y)
    ball_yvel.append(y_vel)
    ball_yaccel.append(y_accel)


#=====================================================================
#------------ Inicialização da classe para o cálculo -----------------
#-------- do vetor posição relativa entre robô e bola ------------
#=====================================================================
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

#===================================================
#----- Variável de entrada do usuário com as -------
#---- posições iniciais (x, y) do robô no campo ----
#===================================================
xo = float(input("Digite o valor inicial xo entre 0 e 9: "))
yo = float(input("Digite o valor inicial yo entre 0 e 6: "))


#================================================
#----- chamada da classe para o calculo da ------
#----- posição relativa entre robô e bola -------
#================================================
for i in range(len(time)):
    bola = Coordinate(x_pos[i], y_pos[i])
    robot = Coordinate(xo, yo)
    relativeDist.append(bola.distance(robot))
    #print("robot = ({}, {}) bola = ({:.2f}, {:.2f}) Dist = {:.2f} t = {}" .format(xo, yo, x_pos[i], y_pos[i], bola.distance(robot), time[i]))
        
robot_data = []

#================================================
#------- função que armazena a distância  -------
#----- minima da posição relativa encontrada ----
#================================================
def min_distance():

    global new_time
    global ballx_pos
    global bally_pos

    min = relativeDist[0]
    for i in range(len(relativeDist)):
        if(relativeDist[i] < min):
            min = relativeDist[i] # menor distância minima no ponto dado
            ballx_pos = x_pos[i] # posição da bola em x no ponto distância minima
            bally_pos = y_pos[i] # posição da bola em y no ponto distância minima 
            new_time = time[i] # Tempo até a bola chegar ao ponto distância minima
        
    print("Min value is {:.2f} in time {:.2f} at bola = ({:.2f}, {:.2f})"  .format( min, new_time, ballx_pos, bally_pos))

min_distance()

if xo < 4.5 and yo > 3: # Bola no segundo quadrante
    robot_data = intersectionPoint(3.4, xo, yo, 7.26, 4.50)
else:
    robot_data = intersectionPoint(new_time, xo, yo, ballx_pos, bally_pos)

def gotBall():
    robotBallDist = []
    if xo < 4.5 and yo > 3: # Bola no segundo quadrante
        for i in range(len(robot_data[robot_xpos])):
            delta_x = 7.26 - robot_data[robot_xpos][i]
            delta_y = 4.50 - robot_data[robot_ypos][i]
            robotBallDist.append( np.sqrt( delta_x**2 + delta_y**2 ) )
    else:
        for i in range(len(robot_data[robot_xpos])):
            delta_x = ballx_pos - robot_data[robot_xpos][i]
            delta_y = bally_pos - robot_data[robot_ypos][i]
            robotBallDist.append( np.sqrt( delta_x**2 + delta_y**2 ) )

    for i in range(len(robotBallDist)):
        if raio_bolaRobo >= robotBallDist[i]:
            bola_intercept = 1
        else:
            bola_intercept = 0
    
    return bool(bola_intercept)


#===================================================
#--------- Gráfico da Trajetória da bola------------
#-------- e Posição de interceptação do Robô -------
#===================================================
fig1, ax = plt.subplots()

# Robô representado por um circulo no gráfico
ax.plot(xo, yo, color='none', linestyle = 'dashed', linewidth = 2,
marker = 'o', markersize = 6, markerfacecolor = 'blue', markeredgecolor = 'blue')

# Bola representado por um quadrado no gráfico
ax.plot(x_pos[0], y_pos[0], color='none', linestyle = 'dashed', linewidth = 2,
marker = 's', markersize = 6, markerfacecolor = 'red', markeredgecolor = 'red')

ax.plot(robot_data[robot_xpos], robot_data[robot_ypos], label='Trajetória do robô', color='blue', linewidth = 0.75)
ax.plot(x_pos, y_pos, label='Trajetória da bola', color='orange')

ax.legend(loc="upper left", shadow=True, fontsize="small")
ax.set_xlim(-1,9)
ax.set_ylim(0,7)
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title("Gráfico da trajetória da bola\n e do robô até a interceptção")
ax.text(xo, yo + 0.25, "robot", ha='center')
ax.text(x_pos[0], y_pos[0] + 0.25, "bola", ha='center')


if xo < 4.5 and yo > 3: # Bola no segundo quadrante
    ax.text(0, 5, f" {r'$tb$'} = {3.4:.2}{r'$s$'} ", ha='left')
    ax.text(0, 4.75, f" {r'$tr$'} = {robot_data[robot_time][-1]:.2}{r'$s$'} ", ha='left')
    ax.text(0, 4.50, f" {r'$x(tb)$'} = {7.26:.2}{r'$m$'} ", ha='left')
    ax.text(0, 4.25, f" {r'$y(tb)$'} = {4.50:.2}{r'$m$'} ", ha='left')
else:
    ax.text(0, 5, f" {r'$t_b$'} = {new_time:.2}{r'$s$'} ", ha='left')
    ax.text(0, 4.75, f" {r'$t_r$'} = {robot_data[robot_time][-1]:.2}{r'$s$'} ", ha='left')
    ax.text(0, 4.50, f" {r'$x(t_b)$'} = {ballx_pos:.2}{r'$m$'} ", ha='left')
    ax.text(0, 4.25, f" {r'$y(t_b)$'} = {bally_pos:.2}{r'$m$'} ", ha='left')

ax.grid(True)


fig2, axs = plt.subplots(nrows=2, ncols=2)

#===================================================
#--------- Gráfico da posição x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[0][0].plot(robot_data[robot_time], robot_data[robot_xpos], label=r'$xb(t)$')
axs[0][0].plot(robot_data[robot_time], robot_data[robot_ypos], label=r'$yb(t)$')

axs[0][0].legend(loc="upper right", shadow=True, fontsize="small")
axs[0][0].set_xlim(0, 4)
axs[0][0].set_ylim(0, 9)
axs[0][0].set_xlabel("temp t (s)")
axs[0][0].set_ylabel("posição em x (m)")
axs[0][0].set_title("Gráfico x e y da posição\n do robô em função do tempo")
axs[0][0].grid(True)


#===================================================
#--------- Gráfico da velocidade x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[0][1].plot(robot_data[robot_time], robot_data[robot_xvel], label='vr(x)')
axs[0][1].plot(robot_data[robot_time], robot_data[robot_yvel], label='vr(y)')

axs[0][1].legend(loc="upper right", shadow=True, fontsize="small")
axs[0][1].set_xlim(0, 4)
axs[0][1].set_ylim(-4, 4)
axs[0][1].set_xlabel("tempo [s]")
axs[0][1].set_ylabel("velocidade [m/s]")
axs[0][1].set_title("Gráfico da velocidade x e y\n do robô em função do tempo")
axs[0][1].text(2.75, -2, f" {r'$v(x)$'} = {robot_data[robot_xvel][0]:.2}{r'$m/s$'} ", ha='left')
axs[0][1].text(2.75, -3, f" {r'$v(y)$'} = {robot_data[robot_yvel][0]:.2}{r'$m/s$'} ", ha='left')
axs[0][1].grid()
axs[0][1].grid(True)


#====================================================
#--------- Gráfico da velocidade x e y do robô ------
#-------- em relação ao tempo de interceptação ------
#====================================================
axs[1][1].plot(time, ball_xvel, label='vb(x)')
axs[1][1].plot(time, ball_yvel, label='vb(y)')

axs[1][1].legend(loc="upper right", shadow=True, fontsize="small")
axs[1][1].set_xlabel("temp t (s)")
axs[1][1].set_ylabel("posição em x (m)")
axs[1][1].set_title("Gráfico da velocidade x\n da bola em função do tempo")
axs[1][1].grid(True)


fig3, ax3 = plt.subplots(nrows=2, ncols=1, sharex=True)
#=====================================================================
#---------Gráfico das Componentes da aceleração x e y da bola --------
#------------- em relação ao tempo de interceptação ------------------
#=====================================================================
ax3[0].plot(time, ball_xaccel, label=r'$a_x(t)$', color='blue', linewidth = 0.75)
ax3[1].plot(time, ball_yaccel, label=r'$a_y(t)$', color='orange')

ax3[0].legend(loc="upper left", shadow=True, fontsize="small")
ax3[0].set_xlabel(r'$t(s)$')
ax3[0].set_ylabel(r'$x(m)$')
ax3[0].set_title("Gráfico das componentes da aceleração\nda bola em função do tempo")
ax3[0].text(xo, yo + 0.25, "robot", ha='center')
ax3[0].grid(True)

ax3[1].legend(loc="upper left", shadow=True, fontsize="small")
ax3[1].set_ylabel(r'$y(m)$')
ax3[1].text(xo, yo + 0.25, "robot", ha='center')
ax3[1].grid(True)

plt.tight_layout()
plt.show()


#fig.savefig('fig1.png')





    