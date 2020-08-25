import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from decimal import Decimal

#### PARAMETROS AJUSTAVEIS ###############
f = 15;                               # frequência do sinal de estímulo elétrico de entrada
T = 1/f;                              # período do sinal de estímuloelétrico de entrada
samplingRate = 0.001;
#ratioOnOff = 1/3;                     # razão entre o tempo em que há estímulo elétrico e tempo de repouso
ratioOnOff = 0.33;
tempoTreino = 2;                      # tempo disparo+descanso 
nTreinos = 1;                       # numero de disparos + descanso 
tempoTotal = nTreinos*tempoTreino;    # tempo total do tratamento
timeArray = np.arange(0,tempoTotal+samplingRate,samplingRate);

#----------------------------------------#

def Erro(a1,a2,b1,b2):
  
    erro_output = 0;
  
    ywiener = Wiener_Hammerstein(u,a1,a2,b1,b2,d,f,timeArray,samplingRate,tempoTreino,ratioOnOff);
    for i in range (len(timeArray)-1):
        erro_output = erro_output + (yreal(i) - ywiener(i))^2;
        
        
def CreateInputArray(timeArray, period, samplingRate,  ton, t_total, t_treino):
    decimals_of_sampling_rate = int(str(samplingRate)[::-1].find('.'))
    print(decimals_of_sampling_rate)
    period_rounded = round(period*pow(10,decimals_of_sampling_rate))/pow(10,decimals_of_sampling_rate);
    #period_rounded = round(period*1000)/1000
    
    u = [];
    for i in timeArray:
        if Decimal(i) % Decimal(t_treino) < t_treino*ratioOnOff:
        #if (i/(t_treino*ratioOnOff)) < 1:
           
          if (i/period_rounded).is_integer():
            u = np.concatenate((u,[1]), axis=None);
          else:
            u = np.concatenate((u,[0]), axis=None);
        else:
          u = np.concatenate((u,[0]), axis=None);
    return u

def Wiener_Hammerstein(u,a1,a2,b1,b2,d,f,timeArray,samplingRate,tempoTreino,ratioOnOff):
  
    v = [0]*len(timeArray)
    w = [0]*len(timeArray)
    y = [0]*len(timeArray)

    v[1] = 0;
    w[1] = 0;
    y[1] = 0;
    
    
    
    tau = round((ratioOnOff*tempoTreino + 1/f +2*d)*1000)/1000;
    for i in range (len(timeArray)-1):
  
        #if (i*samplingRate)/tau < 1:
        if Decimal(i*samplingRate) % Decimal(tempoTreino) > tau:
        #if (i*samplingRate) % tempoTreino > tau:
            a1_atual = 0;
          
        else:
            a1_atual = a1;
            
        v[i+1] = (a1_atual * v[i]) + (a2 * u[i]);
        w[i] = v[i]/(1 + v[i]);
        y[i+1] = (b1 * y[i]) + (b2 * w[i]);
    
    return y
 


##########################################

u = CreateInputArray(timeArray, T, samplingRate, ratioOnOff, tempoTotal, tempoTreino);

#figure
#plot(timeArray,u)

a1_real = 0.9423679;
a2_real = 0.9762052;
b1_real = 0.9712435;
b2_real = 0.0093602;



d = 0;

yreal = Wiener_Hammerstein(u,a1_real,a2_real,b1_real,b2_real,d,f,timeArray,samplingRate,tempoTreino, ratioOnOff)

plt.figure()
plt.plot(timeArray, yreal)
plt.show()










