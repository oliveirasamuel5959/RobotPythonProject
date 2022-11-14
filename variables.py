#===================================================
#----- Variaveis declaradas para a posição ---------
#---- da lista de dados do robô nos gráficos -------
#===================================================
robot_xpos = 0
robot_ypos = 1
robot_time = 2
robot_xvel = 3
robot_yvel = 4
vel_absolute = 5


timeToBall = 0
time = [] # Tempo de trjetória da bola no campo [0, 20s]
x_pos = [] # Posição x da bola no campo
y_pos = [] # posição y da bola no campo

ball_xvel = [] # componente x da velocidade da bola
ball_yvel = [] # componente y da velocidade da bola
ball_xaccel = []
ball_yaccel = []

relativeDist = [] # lista com as posições relativas entre a bola e o robô em [0, 20s]
min_dist = 0 # menor distância relativa entre a bola e o robô


vmax_robot = 2.5 # velocidade máxima do robô em y
amax_robot = 0.55
raio_bolaRobo = 0.3 # raio de interceptação
