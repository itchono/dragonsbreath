import numpy as np
from matplotlib import pyplot as plt

from dragonsbreath.engines.ramjet import maximum_thrust_mach_number

T_a = 220
f = 1 / 50
gamma = 1.4
R = 287

# T04 sweep

T04_range = np.linspace(1500, 3000, 100)
M_max_ideal = [
    maximum_thrust_mach_number(T04, 1, 1, 1, gamma, R, T_a, f) for T04 in T04_range
]
M_max_real = [
    maximum_thrust_mach_number(T04, 0.7, 0.95, 0.98, gamma, R, T_a, f)
    for T04 in T04_range
]

plt.plot(T04_range, M_max_ideal, color="C0", label="Ideal")
plt.plot(
    T04_range, M_max_real, color="C0", label="65% Overall P_0 Ratio", linestyle="--"
)
plt.xlabel("T04 (K)")
plt.ylabel("Maximum thrust Mach number")
plt.title("Mach number at which specific thrust is maximized as a function of T04")
plt.legend()
plt.grid()
plt.show()


# efficiency sweep
efficiency_range = np.linspace(0.7, 1, 100)
for T_04 in [2000, 2500, 3000]:
    M_max = [
        maximum_thrust_mach_number(T_04, r_d, 1, 1, gamma, R, T_a, f)
        for r_d in efficiency_range
    ]
    plt.plot(efficiency_range, M_max, label=f"T04 = {T_04} K")

plt.xlabel("Overall Stagnation Pressure Ratio")
plt.ylabel("Maximum thrust Mach number")
plt.title("Max thrust Mach number vs overall stagnation pressure ratio")
plt.grid()
plt.legend()
plt.show()
