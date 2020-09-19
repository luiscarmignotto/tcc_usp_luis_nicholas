clear; clear all; close all; clc;

addpath("C:\\Users\\luisc\\Desktop\\octave_tcc")
setenv PYTHON C:\Users\luisc\Anaconda3\python.exe
pkg load symbolic
pkg load signal

#### PARAMETROS ESTIMULAÇÃO ###############
global frequencia = 15;                               # frequï¿½ncia do sinal de estï¿½mulo elï¿½trico de entrada
global periodo = 1/frequencia;                              # perï¿½odo do sinal de estï¿½muloelï¿½trico de entrada
global amplitude = 1.0;
global taxa_de_amostragem = 0.001;
global ratio_on_off = 1/3;                     # razï¿½o entre o tempo em que hï¿½ estï¿½mulo elï¿½trico e tempo de repouso
global tempo_treino = 2;                      # tempo disparo+descanso 
global n_treinos = 1;                       # numero de disparos + descanso 
global tempo_total = n_treinos*tempo_treino;    # tempo total do tratamento
global vetor_tempo = [0:taxa_de_amostragem:tempo_total];
global delay = 0; 
#----------------------------------------#

### PARÂMETROS SINAL DE REFERENCIA ###########
x0_referencia = [0.9423679, 0.9762052, 0.9712435, 0.0093602];

### PARÂMETROS OTIMIZAÇÃO ###################
x0_inicial = [0,0,0,0];
n_iteracoes = 300;

function erro_output = Erro(x)
  
  a1 = x(1);
  a2 = x(2);
  b1 = x(3);
  b2 = x(4);
  
  erro_output = 0;
  
  global y_referencia;
  global u; global delay; global frequencia; global vetor_tempo; global taxa_de_amostragem; global tempo_treino; global ratio_on_off;
  
  y_estimado = Wiener_Hammerstein_Modificado(u,x,delay,frequencia,vetor_tempo,taxa_de_amostragem,tempo_treino,ratio_on_off);
  for i=1:1:length(vetor_tempo)-1
    erro_output = erro_output + (y_referencia(i) - y_estimado(i))^2;
  end
end

##########################################

global u = Gerador_Sinal_De_Entrada(vetor_tempo, periodo, ratio_on_off, tempo_total, tempo_treino, amplitude);
global y_referencia = Wiener_Hammerstein_Modificado(u,x0_referencia,delay,frequencia,vetor_tempo,taxa_de_amostragem,tempo_treino, ratio_on_off)

tempo_execucao_otimizacao_i = time(); 
[xmin_final,fval] = fminsearch(@Erro, x0_inicial, optimset("MaxIter", n_iteracoes));
tempo_execucao_otimizacao_f = time();

y_estimado_final = Wiener_Hammerstein_Modificado(u, xmin_final, delay,frequencia,vetor_tempo,taxa_de_amostragem,tempo_treino,ratio_on_off);

figure
plot(vetor_tempo, y_referencia, 'lineWidth', 3, vetor_tempo, y_estimado_final, 'lineWidth', 2)
set(gca, "linewidth", 2.5, "fontsize", 20, "fontweight", "bold")
grid on;
title(['Sinal de saída y_{referência} e y_{estimado} (Nelder-Mead) - ',int2str(n_iteracoes),' Iterações'])
xlabel("Tempo (s)")
set (gca, "ygrid", "on")
set (gca, "xgrid", "on")
legend("y_{referência}","y_{estimado}")

printf("Erro Inicial: %u\n", Erro(x0_inicial))
printf("Erro Final: %u\n", fval)
printf("Parâmetros \"Reais\":\na1 = %u\na2 = %u\nb1 = %u\nb2 = %u\n", x0_referencia(1), x0_referencia(2), x0_referencia(3), x0_referencia(4))
printf("Parâmetros Iniciais:\na1 = %u\na2 = %u\nb1 = %u\nb2 = %u\n", x0_inicial(1),x0_inicial(2),x0_inicial(3),x0_inicial(4))
printf("Parâmetros finais:\na1 = %u\na2 = %u\nb1 = %u\nb2 = %u\n", xmin_final(1), xmin_final(2), xmin_final(3), xmin_final(4))
printf("Tempo de Execução: %u", tempo_execucao_otimizacao_f-tempo_execucao_otimizacao_i)

