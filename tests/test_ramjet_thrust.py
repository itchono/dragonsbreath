import pytest

from dragonsbreath.engines.ramjet import ramjet_specific_thrust


def test_ramjet_specific_thrust():
    M = 6.5
    T04 = 2079
    f = 0
    r_d = 1
    r_c = 1
    r_n = 1
    gamma = 1.4
    R = 287
    T_a = 220
    assert ramjet_specific_thrust(
        M, T04, r_d, r_c, r_n, gamma, R, T_a, f
    ) == pytest.approx(0)
