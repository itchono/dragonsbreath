import numpy as np
from matplotlib import pyplot as plt

from dragonsbreath.engines.ramjet import ramjet_specific_thrust

T_a = 220
f = 1 / 50
gamma = 1.4
R = 287

M = np.linspace(0.1, 7, 100)

for T04 in [2000, 2500, 3000]:
    thrust = ramjet_specific_thrust(M, T04, 1, 1, 1, gamma, R, T_a, f)
    plt.plot(M, thrust, label=f"T04 = {T04} K")

plt.axvline(x=6.5, color="black", linestyle="--", label="Mach 6.5")

plt.xlabel("Mach number")
plt.ylabel("Specific thrust (N/kg/s)")
plt.title("Ideal ramjet specific thrust as a function of Mach number")
plt.legend()
plt.grid()
plt.show()
