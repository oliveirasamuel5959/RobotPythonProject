'''
*****************************************
WELCOME TO PYTHON CLASSES AND INHERITANCE
COURSE FROM MICHIGAN UNIVERSITY
*****************************************
'''
import matplotlib.pyplot as plt
import numpy as np
from pyparsing import lineStart

xo = int(input("Digite o valor inicial xo: "))
yo = int(input("Digite o valor inicial yo: "))





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
    x_pos.append(x)

'''
*
Equação de movimento em y em função do tempo 
com os valores da posição para o intervalo de [0,20,0.02]
*
'''
for i in range(len(time)):
    #y(t) = -0.2t² + 1.8t + 0.7

    y = -0.2*time[i]**2 + 1.8*time[i] + 0.7
    y_pos.append(y)






dt = 0.002
t = 0
vx = 2.12
vy = 1
x = 0
y = 0

data_x = []
data_y = []
data_t = []
velx = 0.53
vely = -0.90

while t < 1.84:

    #calculo feito para x0 = 4 e y0 = 5
    x = xo + velx * t
    data_x.append(x)

    y = yo + vely * t
    data_y.append(y)

    t = t + dt
    data_t.append(t)

fig1, ax1 = plt.subplots()

ax1.plot(xo, yo, color='none', linestyle = 'dashed', linewidth = 2,
marker = 'o', markersize = 6, markerfacecolor = 'blue', markeredgecolor = 'blue')

ax1.plot(data_x, data_y, label='Bola (x,y) pos', color='blue', linewidth = 0.75)
ax1.plot(x_pos, y_pos, label='Bola (x,y) pos', color='orange')


ax1.legend(loc="upper left", shadow=True, fontsize="small")
ax1.set_xlim(0,9)
ax1.set_ylim(0,6)
ax1.set_xlabel("x (s)")
ax1.set_ylabel("y (s)")
ax1.set_title("Gráfico da Posição da Bola no campo")
ax1.grid()

plt.grid()
plt.show()



