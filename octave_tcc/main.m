clear; clear all; close all; clc;

addpath("C:\\Users\\luisc\\Desktop\\octave_tcc")
setenv PYTHON C:\Users\luisc\Anaconda3\python.exe
pkg load symbolic
pkg load signal

#### PARAMETROS AJUSTAVEIS ###############
global f = 15;                               # frequência do sinal de estímulo elétrico de entrada
global T = 1/f;                              # período do sinal de estímuloelétrico de entrada
global amplitude = 1.0;
global samplingRate = 0.001;
global ratioOnOff = 1/3;                     # razão entre o tempo em que há estímulo elétrico e tempo de repouso
global tempoTreino = 2;                      # tempo disparo+descanso 
global nTreinos = 1;                       # numero de disparos + descanso 
global tempoTotal = nTreinos*tempoTreino;    # tempo total do tratamento
global timeArray = [0:samplingRate:tempoTotal];

#----------------------------------------#

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
end

##########################################

global u = CreateInputArray(timeArray, T, samplingRate, ratioOnOff, tempoTotal, tempoTreino, amplitude);

x0_real = [0.9423679, 0.9762052, 0.9712435, 0.0093602];

d = 0;

global yreal = Wiener_Hammerstein(u,x0_real,d,f,timeArray,samplingRate,tempoTreino, ratioOnOff)

x0_inicial = [0,0,0,0];

[xmin,fval] = fminsearch(@Erro, x0_inicial);
     
yopt = Wiener_Hammerstein(u, xmin, d,f,timeArray,samplingRate,tempoTreino,ratioOnOff);

scale = 4.3/max(yreal)

for i=1:1:length(yreal)-1
  u(i) = 5.5*u(i);
  yreal(i) = scale*yreal(i);
  yopt(i) = scale*yopt(i);
end

figure
subplot(1,2,1)
plot(timeArray, yreal, timeArray, u)
set (gca, "ygrid", "on")
set (gca, "xgrid", "on")
xlabel("Tempo (s)")
ylabel("Força (N)")
legend("u", "y")
subplot(1,2,2)
plot(timeArray, yreal, timeArray, yopt)
xlabel("Tempo (s)")
ylabel("Força (N)")
set (gca, "ygrid", "on")
set (gca, "xgrid", "on")


printf("Erro Inicial: %u\n", Erro(x0_inicial))
printf("Erro Final: %u\n", fval)
printf("Parâmetros \"Reais\":\na1 = %u\na2 = %u\nb1 = %u\nb2 = %u\n", x0_real(1), x0_real(2), x0_real(3), x0_real(4))
printf("Parâmetros Iniciais:\na1 = %u\na2 = %u\nb1 = %u\nb2 = %u\n", x0_inicial(1),x0_inicial(2),x0_inicial(3),x0_inicial(4))
printf("Parâmetros finais:\na1 = %u\na2 = %u\nb1 = %u\nb2 = %u\n", xmin(1), xmin(2), xmin(3), xmin(4))



