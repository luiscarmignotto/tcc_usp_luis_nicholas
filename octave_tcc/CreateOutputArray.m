function y = CreateOutputArray(period, samplingRate,  ton, t_total, t_treino, peakForce, decayRate)
    period_rounded = round(period*100)/100;
    y = [];
    decay = 0;
    for i = 0:samplingRate:t_total
      r = round(mod(i, t_treino)*100)/100;
      if mod(i,t_treino) == 0
        peakForce = peakForce - (peakForce * decay)
        decay = decay + decayRate;
      endif
      if r < t_treino*ton
        rr = round(mod(r,period_rounded)*100)/100;
        if rr == 0
          y = horzcat(y,[peakForce]);
        else
          y = horzcat(y,[0]);
        endif
      else
         y = horzcat(y,[0]);
      endif
    endfor
    return
endfunction