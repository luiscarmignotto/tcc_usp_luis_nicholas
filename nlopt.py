x0 = np.array([0.0, 0.0, 0.0, 0.0])

opt = nlopt.opt(nlopt.LN_NELDERMEAD,len(x0))

#opt = nlopt.opt(nlopt.LN_SBPLX,len(x0))
opt.set_min_objective(Erro)
#opt.set_lower_bounds(0)
#opt.set_upper_bounds(1)
#opt.set_ftol_abs(2*np.max(yreal))
xopt = opt.optimize(x0)
fval = opt.last_optimum_value()
print(xopt,fval,"SLSQP w/ jacobian");

a1_opt = xopt[0]
a2_opt = xopt[1]
b1_opt = xopt[2]
b2_opt = xopt[3]

y_opt = Wiener_Hammerstein(u,a1_opt,a2_opt,b1_opt,b2_opt,d,f,totalTimeArray,samplingRate,tempoTreino, ratioOnOff)


plt.figure()
plt.plot(totalTimeArray, yreal, totalTimeArray, y_opt)
#plt.plot(totalTimeArray, yreal)
#plt.legend("Teste")

#plt.figure()
#plt.plot(totalTimeArray, y_opt)
#plt.show()