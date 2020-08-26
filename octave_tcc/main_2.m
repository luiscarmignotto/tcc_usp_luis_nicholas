clear; clear all; close all; clc;

addpath("C:\\Users\\luisc\\Desktop\\octave_tcc")
setenv PYTHON C:\Users\luisc\Anaconda3\python.exe
pkg load symbolic
pkg load signal

x = dlmread ('real_signal.csv', ";"); 
global timeArray = x(:,1);
global yreal = x(:,2);
global u = x(:,3);

#### PARAMETROS AJUSTAVEIS ###############
global f = 15.6210937502;                               # frequência do sinal de estímulo elétrico de entrada
global T = 1/f;                              # período do sinal de estímuloelétrico de entrada
global samplingRate = 0.002;
global ratioOnOff = 1/3;                     # razão entre o tempo em que há estímulo elétrico e tempo de repouso
global tempoTreino = 2;                      # tempo disparo+descanso 
global nTreinos = 1;                       # numero de disparos + descanso 
global tempoTotal = nTreinos*tempoTreino;    # tempo total do tratamento
global timeArray = [0:samplingRate:tempoTotal];

#----------------------------------------#

##########################################

#figure
#plot(timeArray,u)

#a1_real = 0.9984;
#a2_real = 0.2090;
#b1_real = 0.8;
#b2_real = 0.0356;

a1_real = 0.9423679;
a2_real = 0.9762052;
b1_real = 0.9712435;
b2_real = 0.0093602;

v(1) = 0;
w(1) = 0;
y(1) = 0;

d = 0;


figure
plot(timeArray, yreal)

global a1 = 0;
global a2 = 0;
global b1 = 0;
global b2 = 0;




function erro_output = Erro(x)
  
  a1 = x(1);
  a2 = x(2);
  b1 = x(3);
  b2 = x(4);
  
  erro_output = 0;
  
  global yreal;
  global u; global d; global f; global timeArray; global samplingRate; global tempoTreino; global ratioOnOff;
  
  ywiener = Wiener_Hammerstein(u,x,d,f,timeArray,samplingRate,tempoTreino,ratioOnOff);
  for i=1:1:length(timeArray)-1
    erro_output = erro_output + (yreal(i) - ywiener(i))^2;
  end
  erro_output;
end

#errodf = Erro([0;0;0;0]);

[xmin,fval] = fminsearch(@Erro, [0,0,0,0])
     
a1_min = xmin(1);
a2_min = xmin(2);
b1_min = xmin(3);
b2_min = xmin(4);

fval

y_opt = Wiener_Hammerstein(u, xmin, d,f,timeArray,samplingRate,tempoTreino,ratioOnOff);

figure
subplot(2,2,1)
plot(timeArray, yopt, timeArray, yreal)
subplot(2,2,2)
plot(timeArray, yopt)

