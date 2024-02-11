import numpy as np
from matplotlib import pyplot as plt

from dragonsbreath.engines.ramjet import ramjet_specific_thrust

T_a = 220
f = 1 / 50
gamma = 1.4
R = 287

M = np.linspace(1, 7, 100)

for i, T04 in enumerate([2000, 2500, 3000]):
    thrust_ideal = ramjet_specific_thrust(M, T04, 1, 1, 1, gamma, R, T_a, f)
    plt.plot(
        M, thrust_ideal, label=f"T04 = {T04} K (Ideal)", color=f"C{i}", linestyle="--"
    )

    thrust_real = ramjet_specific_thrust(M, T04, 0.7, 0.95, 0.98, gamma, R, T_a, f)
    plt.plot(M, thrust_real, label=f"T04 = {T04} K (Real)", color=f"C{i}")


plt.axvline(x=6.5, color="black", linestyle="--", label="_")

plt.xlabel("Mach number")
plt.ylabel("Specific thrust (N/kg/s)")
plt.title("Ramjet specific thrust as a function of Mach number")
plt.xlim(1, 7)
plt.legend()
plt.grid()
plt.show()
