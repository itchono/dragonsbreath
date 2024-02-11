import numpy as np
from scipy.optimize import minimize_scalar


def ramjet_specific_thrust(
    M: float,
    T04: float,
    r_d: float,
    r_c: float,
    r_n: float,
    gamma: float,
    R: float,
    T_a: float,
    f: float,
) -> float:
    """
    Specific Thrust of a Ramjet Engine, assuming perfect expansion in the nozzle
    (i.e. thrust (N) per unit mass flow of air (kg/s))

    Parameters
    ----------
    M : float
        Flight Mach number
    T04 : float
        Stagnation temperature at the end of the combustion chamber (K)
    r_d : float
        Diffuser efficiency (stagnaion pressure ratio)
    r_c : float
        Combustor efficiency (stagnation pressure ratio)
    r_n : float
        Nozzle efficiency (stagnation pressure ratio)
    gamma : float
        Specific heat ratio
    R : float
        Gas constant (J/kg-K) [specific to air]
    T_a : float
        Ambient temperature (K)
    f : float
        Fuel-air ratio (usually around 1/50)

    Returns
    -------
    float
        Specific thrust (N/kg/s)
    """
    m = (1 + (gamma - 1) / 2 * M**2) * (r_d * r_c * r_n) ** ((gamma - 1) / gamma)

    term_1 = (1 + f) * np.sqrt((2 * gamma * R * T04 * (m - 1) / ((gamma - 1) * m)))
    term_2 = -M * np.sqrt(gamma * R * T_a)

    return term_1 + term_2


def maximum_thrust_mach_number(
    T04: float,
    r_d: float,
    r_c: float,
    r_n: float,
    gamma: float,
    R: float,
    T_a: float,
    f: float,
) -> float:
    """
    Returns the Mach number at which the specific thrust is maximized

    Parameters
    ----------
    T04 : float
        Stagnation temperature at the end of the combustion chamber (K)
    r_d : float
        Diffuser efficiency (stagnaion pressure ratio)
    r_c : float
        Combustor efficiency (stagnation pressure ratio)
    r_n : float
        Nozzle efficiency (stagnation pressure ratio)
    gamma : float
        Specific heat ratio
    R : float
        Gas constant (J/kg-K) [specific to air]
    T_a : float
        Ambient temperature (K)
    f : float
        Fuel-air ratio (usually around 1/50)

    Returns
    -------
    float
        Mach number at which the specific thrust is maximized
    """

    def negative_specific_thrust(M: float) -> float:
        return -ramjet_specific_thrust(M, T04, r_d, r_c, r_n, gamma, R, T_a, f)

    result = minimize_scalar(negative_specific_thrust, bounds=(1, 10), method="bounded")
    return result.x
