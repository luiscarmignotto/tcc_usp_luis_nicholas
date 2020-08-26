function u = CreateInputArray(timeArray, period, samplingRate,  ton, t_total, t_treino, amplitude)
    period_rounded = round(period*100)/100;
    u = [];
    for i = timeArray
        r = round(mod(i, t_treino)*100)/100;
        if r < t_treino*ton
          rr = round(mod(r,period_rounded)*100)/100;
          if rr == 0
            u = vertcat(u,[amplitude]);
          else
            u = vertcat(u,[0]);
          endif
        else
          u = vertcat(u,[0]);
        endif
    endfor
    return
endfunction

