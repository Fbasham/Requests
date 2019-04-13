import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy.integrate import odeint



def rxn(c,t):

    k = 10
    A = c[0]
    B = c[1]
    C = c[2]
    D = c[3]
    dAdt = -k * A
    dBdt = k * A
    dCdt = k * A * B
    dDdt = -k * C * B


    return [dAdt, dBdt, dCdt, dDdt]

c0=[1, 0, 0,1.5]
tspan = np.linspace(0,1,50)

c = odeint(rxn,c0,tspan)

plt.plot(tspan,c[:,0],"r--")
plt.plot(tspan,c[:,1],"g:")
plt.plot(tspan,c[:,2],"bo")
plt.plot(tspan,c[:,3],"ko-")
plt.show()
