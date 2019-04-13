import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#  A + B + C -->  D + E
#  D + C  -->  E
#  E + B  --> F

#  dCa/dt = -k1*[A][B][C]
#  dCb/dt = -k1*[A][B][C] - k3[E][B]
#  dCc/dt = -k1*[A][B][C] - k2[D][C]
#  dCd/dt = k1[A][B][C] - k2[D][C]
#  dCe/dt = k2[D][C] - k3[E][B]


def diffeq(Conc,t):

    k1 = 1
    k2 = 2
    k3 = 3

    A = Conc[0]
    B = Conc[1]
    C = Conc[2]
    D = Conc[3]
    E = Conc[4]

    Adt = -k1 * A*B*C
    Bdt = -k1 *A*B*C - k3*E*B
    Cdt = -k1 *A*B*C -k2*D*C
    Ddt = k1*A*B*C - k2*D*C
    Edt = k2*D*C - k3*E*B

    return [Adt,Bdt,Cdt,Ddt,Edt]

tspan = np.linspace(0,5,100)
C0 = [1, 1, 1, 0, 0]
Conc = odeint(diffeq,C0,tspan)
#print(Conc)

plt.ylim(0,1.05)

for i in range(5):
    labels = ['A', 'B', 'C', 'D', 'E'] 
    plt.plot(tspan, Conc[:,i], label = labels[i])

plt.legend(loc='best')
plt.xlabel("Time (sec)")
plt.ylabel("Concentrations (mol/L)")
plt.title("Concentration Profile")
plt.show()
