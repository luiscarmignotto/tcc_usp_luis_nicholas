import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
import scipy.optimize
from scipy.optimize import Bounds
import nlopt

#### PARAMETROS AJUSTAVEIS ###############
f = 15;                               # frequência do sinal de estímulo elétrico de entrada
T = 1/f;                              # período do sinal de estímuloelétrico de entrada
samplingRate = 0.001;
ratioOnOff = 1/3;                     # razão entre o tempo em que há estímulo elétrico e tempo de repouso
tempoTreino = 2;                      # tempo disparo+descanso 
nTreinos = 1;                       # numero de disparos + descanso 
tempoTotal = nTreinos*tempoTreino;    # tempo total do tratamento
totalTimeArray = np.arange(0,tempoTotal,samplingRate);

#----------------------------------------#

def Erro(x):
    erro_output = 0;
    
    a1 = x[0];
    a2 = x[1];
    b1 = x[2];
    b2 = x[3];
        
    ywiener = Wiener_Hammerstein(u,x,d,f,totalTimeArray,samplingRate,tempoTreino,ratioOnOff);
    
    for i in range (len(totalTimeArray)-1):
        erro_output = erro_output + (yreal[i] - ywiener[i])**2;
    
    return float(erro_output)    
        
def CreateInputArray(period, samplingRate,  ton, n_treinos, t_treino):
   
    period_rounded = round(period*1000)/1000
    timeArray = np.arange(0,t_treino,samplingRate);
    u_1Cicle = [];
    u = [];
    for i in timeArray:
        if Decimal(i) % Decimal(t_treino) < t_treino*ratioOnOff:
            if Decimal(i) % Decimal(period_rounded) == 0:
                u_1Cicle = np.concatenate((u_1Cicle,[1]), axis=None);
            else:
                u_1Cicle = np.concatenate((u_1Cicle,[0]), axis=None);
        else:
            u_1Cicle = np.concatenate((u_1Cicle,[0]), axis=None);
        
   
    u = np.tile(u_1Cicle, n_treinos)
    return u

def Wiener_Hammerstein(u,x,d,f,timeArray,samplingRate,tempoTreino,ratioOnOff):
  
    a1 = x[0];
    a2 = x[1];
    b1 = x[2];
    b2 = x[3];
    
    v = [0]*len(timeArray)
    w = [0]*len(timeArray)
    y = [0]*len(timeArray)

    v[1] = 0;
    w[1] = 0;
    y[1] = 0;
    
  
    tau = ratioOnOff*tempoTreino + 1/f +2*d;
    
    for i in range (len(timeArray)-1):
  
        if Decimal(i*samplingRate) % Decimal(tempoTreino) > tau:
            a1_atual = 0;
        else:
            a1_atual = a1;
            
        v[i+1] = (a1_atual * v[i]) + (a2 * u[i]);
        w[i] = v[i]/(1 + v[i]);
        y[i+1] = (b1 * y[i]) + (b2 * w[i]);
    
    return y
 
def nmae(yreal, y_opt):
    
    N = len(yreal)-1
    sum = 0;
    for i in range (N):
         sum = sum + abs(yreal[i] - y_opt[i])
    
    return (1/N)*sum/np.max(yreal)

##########################################

u = CreateInputArray(T, samplingRate, ratioOnOff, nTreinos, tempoTreino);

#figure
#plot(timeArray,u)

a1_real = 0.9423679;
a2_real = 0.9762052;
b1_real = 0.9712435;
b2_real = 0.0093602;

x0_real = np.array([0.9423679,0.9762052,0.9712435,0.0093602], dtype='double')

#a1_real = 0.98281309;
#a2_real = 0.88814498;
#b1_real = 0.98360935;
#b2_real = 0.88108429;

d = 0;

yreal = Wiener_Hammerstein(u,x0_real,d,f,totalTimeArray,samplingRate,tempoTreino, ratioOnOff)


def ineq_constraint_a1_lower(x):
    a1 = x[0];
    return a1
def ineq_constraint_a2_lower(x):
    a2 = x[1];
    return a2

def ineq_constraint_b1_lower(x):
    b1 = x[2];
    return b1

def ineq_constraint_b2_lower(x):
    b2 = x[3];
    return b2 

def ineq_constraint_a1_upper(x):
    a1 = x[0]
    return a1 -1.0 
def ineq_constraint_a2_upper(x):
    a2 = x[1]
    return a2 -1.0 
def ineq_constraint_b1_upper(x):
    b1 = x[2]
    return b1 -1.0 
def ineq_constraint_b2_upper(x):
    b2 = x[3]
    return b2 -1.0 


#########################################################################
constraint_a1_1 = {'type': 'ineq', 'fun': ineq_constraint_a1_lower}
constraint_a1_2 = {'type': 'ineq', 'fun': ineq_constraint_a1_upper}
constraint_a2_1 = {'type': 'ineq', 'fun': ineq_constraint_a2_lower}
constraint_a2_2 = {'type': 'ineq', 'fun': ineq_constraint_a2_upper}
constraint_b1_1 = {'type': 'ineq', 'fun': ineq_constraint_b1_lower}
constraint_b1_2 = {'type': 'ineq', 'fun': ineq_constraint_b1_upper}
constraint_b2_1 = {'type': 'ineq', 'fun': ineq_constraint_b2_lower}
constraint_b2_2 = {'type': 'ineq', 'fun': ineq_constraint_b2_upper}

constraints_optm = [constraint_a1_1, \
               constraint_a1_2, \
               constraint_a2_1, \
               constraint_a2_2, \
               constraint_b1_1, \
               constraint_b1_2, \
               constraint_b2_1, \
               constraint_b2_2]
    
erro_base = Erro([0,0,0,0])
bounds=Bounds([0.0, 0.0, 0.0, 0.0], [1.0,1.0,1.0,1.0])
xopt = scipy.optimize.minimize(Erro,x0=[0,0,0,0], method='SLSQP',constraints=constraints_optm,options={'ftol': 1.5})

print (xopt.x)

y_opt = Wiener_Hammerstein(u,xopt.x,d,f,totalTimeArray,samplingRate,tempoTreino, ratioOnOff)


plt.figure()
#plt.plot(totalTimeArray, yreal, totalTimeArray, y_opt)
#plt.plot(totalTimeArray, yreal)
plt.legend("Teste")

plt.figure()
plt.plot(totalTimeArray, y_opt)
plt.show()

plt.figure()
plt.subplot(221)
plt.plot(totalTimeArray, y_opt)
plt.title('Y Opt')
plt.subplot(222)
plt.title('Y Real')
plt.plot(totalTimeArray, yreal)

print(nmae(yreal, y_opt))

#############################################################
