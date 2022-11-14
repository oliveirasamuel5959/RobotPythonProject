from cProfile import label
from glob import glob
from operator import ne
from tkinter import font
from turtle import color
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
    global min_dist

    min_dist = relativeDist[0]
    for i in range(len(relativeDist)):
        if(relativeDist[i] < min_dist):
            min_dist = relativeDist[i] # menor distância minima no ponto dado
            ballx_pos = x_pos[i] # posição da bola em x no ponto distância minima
            bally_pos = y_pos[i] # posição da bola em y no ponto distância minima 
            new_time = time[i] # Tempo até a bola chegar ao ponto distância minima
        
    print("Min value is {:.2f} in time {:.2f} at bola = ({:.2f}, {:.2f})" .format(min_dist, new_time, ballx_pos, bally_pos))


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


print(robot_data[vel_absolute])
print(gotBall())


font_dict = {'family': 'serif',
             'color': 'darkblue',
             'size': 10}

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
ax.plot(x_pos, y_pos, label='Trajetória da bola', color='c')

ax.legend(loc="upper left", shadow=True, fontsize=14, ncol=2, facecolor="lightgray")
ax.set_xlim(-1,9)
ax.set_ylim(0,7)
ax.set_xlabel(r'$x[m]$')
ax.set_ylabel(r'$y[m]$')
ax.set_title("Gráfico da trajetória da bola\n e do robô até o ponto de interceptção", fontsize=16, fontweight='bold')
ax.text(xo, yo + 0.25, "robot", ha='center', fontweight='bold')
ax.text(xo, yo - 0.25, f"({xo}, {yo})", ha='center') # posição do robô no gráfico (xo, yo)
ax.text(x_pos[0], y_pos[0] + 0.25, "bola", ha='center', fontweight='bold')
ax.text(x_pos[0], y_pos[0] - 0.25, f"({x_pos[0]}, {y_pos[0]})", ha='center')



if xo < 4.5 and yo > 3: # Bola no segundo quadrante
    ax.text(4.5, 6.5, f" {r'$t_b$'} = {3.4:.2f}{r'$s$'} ", ha='left', fontdict=font_dict)
    ax.text(5.5, 6.5, f" {r'$t_r$'} = {robot_data[robot_time][-1]:.2f}{r'$s$'} ", ha='left', fontdict=font_dict)
    ax.text(6.5, 6.5, f" {r'$x(t_b)$'} = {7.26:.2f}{r'$m$'} ", ha='left', fontdict=font_dict)
    ax.text(7.8, 6.5, f" {r'$y(t_b)$'} = {4.50:.2f}{r'$m$'} ", ha='left', fontdict=font_dict)
    ax.text(6, 6.15, f" {r'$|v_r|$'} = {robot_data[vel_absolute]:.2f}{r'$m/s$'} ", ha='left', fontdict=font_dict)

    ax.annotate('Interceptação', (7.26, 4.50),
            xytext=(0.8, 0.8), textcoords='axes fraction', 
            arrowprops=dict(arrowstyle="->", facecolor='red'))

    if robot_data[vel_absolute] < vmax_robot and gotBall():
        ax.text(1, 3.5, f"Bola interceptada na posição: ({7.26 - 0.215:.2f}, {4.50 - 0.215:.2f})", ha='center', fontsize=13, color="black")
else:
    ax.text(4.5, 6.5, f" {r'$t_b$'} = {new_time:.2f}{r'$s$'} ", ha='left', fontdict=font_dict)
    ax.text(5.5, 6.5, f" {r'$t_r$'} = {robot_data[robot_time][-1]:.2f}{r'$s$'} ", ha='left', fontdict=font_dict)
    ax.text(6.5, 6.5, f" {r'$x(t_b)$'} = {ballx_pos:.2f}{r'$m$'} ", ha='left', fontdict=font_dict)
    ax.text(7.8, 6.5, f" {r'$y(t_b)$'} = {bally_pos:.2f}{r'$m$'} ", ha='left', fontdict=font_dict)
    ax.text(6, 6.15, f" {r'$|v_r|$'} = {robot_data[vel_absolute]:.2f}{r'$m/s$'} ", ha='left', fontdict=font_dict)

    ax.annotate('Interceptação', (ballx_pos, bally_pos),
            xytext=(0.8, 0.8), textcoords='axes fraction', 
            arrowprops=dict(arrowstyle="->", facecolor='red', color='red'))
    
    if robot_data[vel_absolute] < vmax_robot and gotBall():
        ax.text(1, 3.5, f"Bola interceptada na posição: ({ballx_pos - 0.215:.2f}, {bally_pos - 0.215:.2f})", ha='center', fontsize=13, color="black")


if robot_data[vel_absolute] > vmax_robot:
    ax.text(4.5, 3.5, f"Velocidade máxima ultrapassada: {r'$v_m$'} = {robot_data[vel_absolute]:.2f}{r'$m/s$'}", ha='center', fontsize=16, color="red")

ax.minorticks_on()
ax.grid(b=True, which="minor")

print(relativeDist)

fig2, axs = plt.subplots(nrows=2, ncols=2, layout="constrained")
#===================================================
#--------- Gráfico da posição x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[0][0].plot(robot_data[robot_time], robot_data[robot_xpos], label=r'$x_r(t)$', color='m')
axs[0][0].plot(robot_data[robot_time], robot_data[robot_ypos], label=r'$y_r(t)$', color='c')

axs[0][0].legend(loc="upper right", shadow=True, fontsize=10, bbox_to_anchor=(-0.05, 1.5))
axs[0][0].set_xlim(0, robot_data[robot_time][-1] + 0.5)
axs[0][0].set_ylim(0.0, 9.0)
axs[0][0].set_xlabel(r'$t[s]$')
axs[0][0].set_ylabel(r'$s[m]$')
axs[0][1].xaxis.set_ticks(np.arange(0, robot_data[robot_time][-1], 0.25))
axs[0][0].yaxis.set_ticks(np.arange(0, 9, 0.75))
axs[0][0].set_title("Gráfico da posição x e y\n do robô em função do tempo de interceptação", fontweight='bold')
axs[0][0].minorticks_on()
axs[0][0].grid(b=True, which="minor")

#===================================================
#--------- Gráfico da velocidade x e y do robô --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[0][1].plot(robot_data[robot_time], robot_data[robot_xvel], label=f" {r'$v_r(x)$'} = {robot_data[robot_xvel][-1]:.2f}{r'$m/s$'}", color='m')
axs[0][1].plot(robot_data[robot_time], robot_data[robot_yvel], label=f" {r'$v_r(y)$'} = {robot_data[robot_yvel][-1]:.2f}{r'$m/s$'}", color='c')

axs[0][1].legend(loc="upper left", shadow=True, fontsize=10, bbox_to_anchor=(1.00, 1.5))
axs[0][1].set_xlim(0, robot_data[robot_time][-1] + 0.5)
axs[0][1].set_ylim(-4, 4)
axs[0][1].set_xlabel(r'$t[s]$')
axs[0][1].xaxis.set_ticks(np.arange(0, robot_data[robot_time][-1], 0.25))
axs[0][1].yaxis.set_ticks(np.arange(-4, 4, 0.75))
axs[0][1].set_ylabel(r'$v[m/s]$')
axs[0][1].set_title("Gráfico da velocidade x e y\n do robô em função do tempo de interceptação",fontweight='bold')
axs[0][1].minorticks_on()
axs[0][1].grid(b=True, which="minor")


#===================================================
#--------- Gráfico da posição x e y da bola --------
#-------- em relação ao tempo de interceptação -----
#===================================================
axs[1][0].plot(time, x_pos, label=r'$x_b(x)$', color='r')
axs[1][0].plot(time, y_pos, label=r'$y_b(y)$', color='g')

axs[1][0].legend(loc="upper right", shadow=True, fontsize=10, bbox_to_anchor=(-0.05, 1.5))
axs[1][0].set_xlabel(r'$t[s]$')
axs[1][0].set_ylabel(r'$s[m]$')
axs[1][0].set_title("Gráfico da posição x e y\n da bola em função do tempo", fontweight='bold')
axs[1][0].minorticks_on()
axs[1][0].grid(b=True, which="minor")


#====================================================
#--------- Gráfico da velocidade x e y da bola ------
#-------- em relação ao tempo de interceptação ------
#====================================================
axs[1][1].plot(time, ball_xvel, label=r'$v_b(x)$', color='r')
axs[1][1].plot(time, ball_yvel, label=r'$v_b(y)$', color='g')

axs[1][1].legend(loc="upper left", shadow=True, fontsize=10, bbox_to_anchor=(1.00, 1.5))
axs[1][1].set_xlabel(r'$t[s]$')
axs[1][1].set_ylabel(r'$v[m/s]$')
axs[1][1].set_title("Gráfico da velocidade x e y\n da bola em função do tempo", fontweight='bold')
axs[1][1].minorticks_on()
axs[1][1].grid(b=True, which="minor")



fig3, ax3 = plt.subplots(nrows=2, ncols=1, sharex=True)
#=====================================================================
#---------Gráfico das Componentes da aceleração x e y da bola --------
#------------- em relação ao tempo de interceptação ------------------
#=====================================================================
ax3[0].plot(time, ball_xaccel, label=r'$a_x(t)$', color='r', linewidth = 0.75)
ax3[1].plot(time, ball_yaccel, label=r'$a_y(t)$', color='g')

ax3[0].legend(loc="upper right", shadow=True, fontsize=14)
ax3[0].set_ylabel(r'$a_x [m/s^2]$')
ax3[0].set_title("Gráfico das componentes da aceleração\nda bola em função do tempo", fontsize=16,fontweight='bold')
ax3[0].text(xo, yo + 0.25, "robot", ha='center')
ax3[0].minorticks_on()
ax3[0].grid(b=True, which="minor")

ax3[1].legend(loc="upper right", shadow=True, fontsize=14)
ax3[1].set_xlabel(r'$t [s]$')
ax3[1].set_ylabel(r'$a_y [m/s^2]$')
ax3[1].text(xo, yo + 0.25, "robot", ha='center')
ax3[1].minorticks_on()
ax3[1].grid(b=True, which="minor")




fig5, ax4 = plt.subplots(nrows=1, ncols=1)
#=====================================================================
#---------Gráfico da distancia relativa entre a bola e o robô --------
#------------- em relação ao tempo de interceptação ------------------
#=====================================================================
ax4.plot(time, relativeDist, label=r'$D(m)$', color='r', linewidth = 0.95)
ax4.plot(new_time, min_dist, color='none', linestyle = 'dashed', linewidth = 2,
marker = 'o', markersize = 5, markerfacecolor = 'blue', markeredgecolor = 'blue')

#ax4.axhline(y = min_dist, color = 'b', linestyle = '-')
ax4.text(new_time, min_dist + 1.5, f"({new_time:.2f},{min_dist:.2f})", ha='center')

ax4.legend(loc="upper right", shadow=True, fontsize=14)
ax4.set_ylabel(r'$distancia[m]$')
ax4.set_xlabel(r'$t[s]$')
ax4.set_xlim(0, 20)
ax4.set_ylim(0, 95)
ax4.yaxis.set_ticks(np.arange(0, 95, 5))
ax4.xaxis.set_ticks(np.arange(0, 20, 1))
ax4.set_title("Gráfico da distânica relativa entre bola e robô \nem função do tempo", fontsize=16,fontweight='bold')
ax4.minorticks_on()
ax4.grid(b=True, which="minor")


plt.show()


#fig.savefig('fig1.png')





    
