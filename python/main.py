import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal
import scipy.optimize
from scipy.optimize import Bounds

#### PARAMETROS ESTIMULAÇÃO ###############################
amplitude = 1
frequencia = 15                               
periodo = 1/frequencia                              
taxa_de_amostragem = 0.001
ratio_on_off = 1/3                     
tempo_treino = 2                       
n_treinos = 1       
tempo_total = n_treinos*tempo_treino    
vetor_tempo = np.arange(0,tempo_total,taxa_de_amostragem)
delay = 0

### PARAMETROS SINAL DE REFERENCIA##########################
x0_referencia = np.array([0.9423679,0.9762052,0.9712435,0.0093602], dtype='double')

### PARAMETROS OTIMIZAÇÃO ###################################
x0 = [0,0,0,0]
n_iteracoes = 50
algoritmo_otimizacao = 'trust-constr'
bounds=Bounds([0.0, 0.0, 0.0, 0.0], [1.0,1.0,1.0,1.0])


### MODELO DE WIENER-HAMMERSTEIN MODIFICADO
def Wiener_Hammerstein_Modificado(u,x):
    
    a1 = x[0]
    a2 = x[1]
    b1 = x[2]
    b2 = x[3]
   
    v = [0]*len(vetor_tempo)
    w = [0]*len(vetor_tempo)
    y = [0]*len(vetor_tempo)

    v[1] = 0;
    w[1] = 0;
    y[1] = 0;
    
    tau = ratio_on_off*tempo_treino + 1/frequencia +2*delay;
    
    for i in range (len(vetor_tempo)-1):
  
        if Decimal(i*taxa_de_amostragem) % Decimal(tempo_treino) > tau:
            a1_atual = 0;
        else:
            a1_atual = a1;
            
        v[i+1] = (a1_atual * v[i]) + (a2 * u[i]);
        w[i] = v[i]/(1 + v[i]);
        y[i+1] = (b1 * y[i]) + (b2 * w[i]);
    
    return y

### ERRO QUADRATICO
def Erro(x_estimado):
    
    erro_output = 0;
        
    y_estimado = Wiener_Hammerstein_Modificado(u,x_estimado)
    
    for i in range (len(vetor_tempo)-1):
        erro_output = erro_output + (y_referencia[i] - y_estimado[i])**2;
    
    return float(erro_output)   


### GERADOR DO SINAL DE ENTRADA
def Gerador_Sinal_De_Entrada():
       
    periodo_arredondado = round(periodo*1000)/1000
    vetor_tempo = np.arange(0,tempo_treino,taxa_de_amostragem);
    u_1Cicle = [];
    u = [];
    for i in vetor_tempo:
        if Decimal(i) % Decimal(tempo_treino) < tempo_treino*ratio_on_off:
            if Decimal(i) % Decimal(periodo_arredondado) == 0:
                u_1Cicle = np.concatenate((u_1Cicle,[amplitude]), axis=None);
            else:
                u_1Cicle = np.concatenate((u_1Cicle,[0]), axis=None);
        else:
            u_1Cicle = np.concatenate((u_1Cicle,[0]), axis=None);
        
    u = np.tile(u_1Cicle, n_treinos)
    return u
 
         
##########################################

### GERANDO O SINAL DE ENTRADA
u = Gerador_Sinal_De_Entrada();
y_referencia = Wiener_Hammerstein_Modificado(u,x0_referencia)

### OTIMIZACAO
xopt = scipy.optimize.minimize(Erro,x0=x0, bounds=bounds, method=algoritmo_otimizacao ,options={'maxiter': n_iteracoes})

### SINAL ESTIMADO FINAL 
y_estimado_final = Wiener_Hammerstein_Modificado(u,xopt.x)


### PLOT
plt.figure()
plt.plot(vetor_tempo, y_referencia, vetor_tempo, y_estimado_final)
plt.title('Sinal de saída $y_{referência}$ e $y_{estimado}$ (%s) - %i Iterações' % (algoritmo_otimizacao, n_iteracoes))
plt.xlabel("Tempo (s)")
plt.grid(linestyle='-', linewidth=0.5)
plt.legend(['$y_{referência}$', '$y_{estimado}$'])

#############################################################
