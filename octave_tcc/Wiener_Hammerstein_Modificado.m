function y = Wiener_Hammerstein_Modificado(u,x,delay,frequencia,vetor_tempo,taxa_de_amostragem,tempo_treino,ratio_on_off)
  
  a1 = x(1);
  a2 = x(2);
  b1 = x(3);
  b2 = x(4);
  
  v(1) = [0];
  w(1) = [0];
  y(1) = [0];
  
  for i=1:1:length(vetor_tempo)-1
  tau = ratio_on_off*tempo_treino + 1/frequencia + 2*delay;
  if mod((i*taxa_de_amostragem), tempo_treino) > tau
    a1_atual = 0;
   else
    a1_atual = a1;
  endif
    
  v(i+1) = (a1_atual * v(i)) + (a2 * u(i));
  w(i) = v(i)/(1 + v(i));
  y(i+1) = ((b1 * y(i)) + (b2 * w(i)) );
 end
 
endfunction
