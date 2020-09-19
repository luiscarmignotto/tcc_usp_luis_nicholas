function u = Gerador_Sinal_De_Entrada(vetor_tempo, periodo, ratio_on_off, tempo_treino, amplitude)
    periodo_rounded = round(periodo*100)/100;
    u = [];
    for i = vetor_tempo
        r = round(mod(i, tempo_treino)*100)/100;
        if r < tempo_treino*ratio_on_off
          rr = round(mod(r,periodo_rounded)*100)/100;
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

