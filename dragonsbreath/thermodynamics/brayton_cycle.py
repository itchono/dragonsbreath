from dataclasses import dataclass

import numpy as np


@dataclass
class ThermodynamicProcess:
    T_start: float
    T_end: float

    @property
    def change_in_entropy(self) -> float:
        raise NotImplementedError


@dataclass
class IsentropicProcess(ThermodynamicProcess):
    P_start: float
    P_end: float

    @property
    def change_in_entropy(self) -> float:
        return 0


@dataclass
class IsobaricProcess(ThermodynamicProcess):
    P_process: float

    @property
    def change_in_entropy(self) -> float:
        """
        Minus scaling factor
        """
        return np.log(self.T_end / self.T_start)


@dataclass
class EngineCycle:
    s_start: float
    processes: list[ThermodynamicProcess]

    @property
    def change_in_entropy(self) -> float:
        return sum(process.change_in_entropy for process in self.processes)

    def isobar_points(
        self, T_start: float, T_end: float, s_start: float, num_points
    ) -> tuple[list[float], list[float]]:
        """
        Returns the temperature-entropy coordinates for an isobaric process
        """

        T_values = np.linspace(T_start, T_end, num_points)
        s_values = [s_start]

        for T in T_values[1:]:
            s_values.append(s_values[-1] + np.log(T / T_values[0]))

        return s_values, T_values

    def ts_coordinates(self, num_points: int) -> tuple[list[float], list[float]]:
        """
        Returns the temperature-entropy coordinates for the cycle, returning num_points points per segment
        """

        s_values = [self.s_start]
        T_values = [self.processes[0].T_start]

        for process in self.processes:
            if isinstance(process, IsentropicProcess):
                s_values.append(process.change_in_entropy)
                T_values.append(process.T_end)
            elif isinstance(process, IsobaricProcess):
                # constant pressure process; plot isobar, which is an exponential curve
                s_values_, T_values_ = self.isobar_points(
                    process.T_start, process.T_end, s_values[-1], num_points
                )
                s_values.extend(s_values_)
                T_values.extend(T_values_)

        return s_values, T_values


@dataclass
class RamjetCycle(EngineCycle):
    M: float
    T04: float
    r_d: float
    r_c: float
    r_n: float
    gamma: float
    R: float
    T_a: float
    f: float
    p_a: float

    @property
    def processes(self) -> list[ThermodynamicProcess]:
        # stagnation pressure is constant throughout the engine
        p_0 = self.p_a * (1 + (self.gamma - 1) / 2 * self.M**2) ** (
            self.gamma / (self.gamma - 1)
        )

        # inlet
        T02 = self.T_a * (1 + (self.gamma - 1) / 2 * self.M**2)
        inlet_process = IsentropicProcess(
            T_start=self.T_a, T_end=T02, P_start=self.p_a, P_end=p_0
        )

        # combustor
        combustor_process = IsobaricProcess(P_process=p_0, T_start=T02, T_end=self.T04)

        # nozzle
        T_6 = self.T04 * (1 + (self.gamma - 1) / 2 * self.M**2)
        nozzle_process = IsentropicProcess(
            T_start=self.T04,
            T_end=T_6,
            P_start=p_0,
            P_end=self.p_a,
        )

        return [inlet_process, combustor_process, nozzle_process]
