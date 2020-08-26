function y = Wiener_Hammerstein(u,x,d,f,timeArray,samplingRate,tempoTreino,ratioOnOff)
  
  a1 = x(1);
  a2 = x(2);
  b1 = x(3);
  b2 = x(4);
  
  v(1) = [0];
  w(1) = [0];
  y(1) = [0];
  
  for i=1:1:length(timeArray)-1
  tau = ratioOnOff*tempoTreino + 1/f +2*d;
  if mod((i*samplingRate), tempoTreino) > tau
    a1_atual = 0;
   else
    a1_atual = a1;
  endif
    
  v(i+1) = (a1_atual * v(i)) + (a2 * u(i));
  w(i) = v(i)/(1 + v(i));
  y(i+1) = ((b1 * y(i)) + (b2 * w(i)) );
 end
 
endfunction
