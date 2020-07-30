# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.differential_equation.DifferentialEquation` for "complex" four body problem.
"""

import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt

from gezeiten.constants import G, m_E, r_C, m_M, r_E, r_M, T_M, m_O, k, DEFAULT_PLOT_TITLE
from gezeiten.differential_equations.four_body_problem_simple import FourBodyProblemSimple
from gezeiten.solvers.magic_solver import MagicSolver


class FourBodyProblemComplex(FourBodyProblemSimple):
    """
    Although being named generically as "four body problem", this class actually is quite specific to
    the earth-moon system by default. The initial conditions provided and constants used in the
    differential equation are based on values observed in space and should be changed for other four
    body problems.
    In contrast to FourBodyProblemSimple, this class takes into account the intrinsic rotation of Earth
    and the friction caused by the high tides on the surface of Earth.
    """
    initial_conditions = (
        -r_C,  # x component of Earth
        0,  # x component of velocity of Earth
        0,  # y component of Earth
        -2 * np.pi * r_C / T_M,  # y component of velocity of Earth
        r_M - r_C,  # x component of Moon
        0,  # x component of velocity of Moon
        0,  # y component of Moon
        2 * np.pi * (r_M - r_C) / T_M,  # y component of velocity of Moon
        0,  # angle of first high tide
        2 * np.pi / T_M,  # angular velocity of first high tide
        np.pi,  # angle of second high tide
        2 * np.pi / T_M,  # angular velocity of second high tide
        0,  # angle of intrinsic Earth rotation
        2 * np.pi / (24 * 60 * 60)  # angular velocity of intrinsic Earth rotation
    )

    def __init__(self, time_boundaries, data_points_amount):
        """
        Initializes the four body problem, by default with initial conditions of the earth-moon system.

        Attributes
        ----------
        time_boundaries: 2-tuple of floats
            Describes start and end time
        data_points_amount: int
            Amount of points solvers should use as data points
        """
        self.differential_equation_function = self.f
        self.time_boundaries = time_boundaries
        self.data_points_amount = data_points_amount
        self.m_O = m_O

    def f(self, t, r):  # Constraint: x_F ** 2 + y_F ** 2 = r_E ** 2
        """
        Actual differential equation of four body problem

        Attributes
        ----------
        t: float
            Time
        r: array
            Vector containing positions and velocities of earth and moon
            and angles and angular velocity of high tides
        Returns
        -------
        array
            Updated r vector
        """
        x_E, vx_E, y_E, vy_E, x_M, vx_M, y_M, vy_M, phi1, vphi1, phi2, vphi2, phi_E, vphi_E = r
        distance_earth_moon = np.sqrt((x_M - x_E) ** 2 + (y_M - y_E) ** 2)
        distance_F1_moon = np.sqrt((r_E * cos(phi1) + x_E - x_M) ** 2 + (r_E * sin(phi1) + y_E - y_M) ** 2)
        distance_F2_moon = np.sqrt((r_E * cos(phi2) + x_E - x_M) ** 2 + (r_E * sin(phi2) + y_E - y_M) ** 2)
        f_1 = vx_E
        f_2 = -G * m_M * (x_E - x_M) / distance_earth_moon ** 3
        f_3 = vy_E
        f_4 = -G * m_M * (y_E - y_M) / distance_earth_moon ** 3
        f_5 = vx_M
        f_6 = (
                -G * (
                    m_E * (x_M - x_E) / distance_earth_moon ** 3
                    + 1/2 * self.m_O * (
                        (x_M - r_E * cos(phi1) - x_E) / distance_F1_moon ** 3
                        + (x_M - r_E * cos(phi2) - x_E) / distance_F2_moon ** 3)
                    )
                )
        f_7 = vy_M
        f_8 = (
                -G * (
                    m_E * (y_M - y_E) / distance_earth_moon ** 3
                    + 1/2 * self.m_O * (
                        (y_M - r_E * sin(phi1) - y_E) / distance_F1_moon ** 3
                        + (y_M - r_E * sin(phi2) - y_E) / distance_F2_moon ** 3)
                    )
                )
        f_9 = vphi1
        f_10 = (
                1/r_E * (
                    (-G * m_M * (x_E - x_M) / distance_earth_moon ** 3) * sin(phi1)
                    - (-G * m_M * (y_E - y_M) / distance_earth_moon ** 3) * cos(phi1)
                    - m_M * G * ((r_E * sin(phi1) + y_E - y_M) * cos(phi1) - (r_E * cos(phi1) + x_E - x_M) * sin(phi1))
                    / distance_F1_moon ** 3)
                - r_E * k * abs(vphi1 - vphi_E) * (vphi1 - vphi_E)
                )
        f_11 = vphi2
        f_12 = (
                1/r_E * (
                    (-G * m_M * (x_E - x_M) / distance_earth_moon ** 3) * sin(phi2)
                    - (-G * m_M * (y_E - y_M) / distance_earth_moon ** 3) * cos(phi2)
                    - m_M * G * ((r_E * sin(phi2) + y_E - y_M) * cos(phi2) - (r_E * cos(phi2) + x_E - x_M) * sin(phi2))
                    / distance_F2_moon ** 3)
                - r_E * k * abs(vphi2 - vphi_E) * (vphi2 - vphi_E)
                )
        f_13 = vphi_E
        f_14 = 5 / 4 * r_E * self.m_O / m_E * k * (
                abs(vphi1 - vphi_E) * (vphi1 - vphi_E) + abs(vphi2 - vphi_E) * (vphi2 - vphi_E))

        return [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12, f_13, f_14]

    def solve(self, solver=MagicSolver(), m_O=m_O):
        """
        Solves the differential equation of the four body problem by using the solver passed as an argument.

        Once finished, the two body problem will have a solution field which is a dictionary with entries
        t, x_E, y_E, vx_E, vy_E, x_M, y_M, vx_M, vy_M, phi1, vphi1, phi2, vphi2, phi_E, vphi_E, each containing
        a list of floats.

        Attributes
        ----------
        solver: gezeiten.solver.Solver
            Solver which solves the differential equation; by default MagicSolver
        """
        self.m_O = m_O
        solution = solver.solve(self)
        self.solution = {
            "t": solution[0],
            "x_E": solution[1].T[0],
            "vx_E": solution[1].T[1],
            "y_E": solution[1].T[2],
            "vy_E": solution[1].T[3],
            "x_M": solution[1].T[4],
            "vx_M": solution[1].T[5],
            "y_M": solution[1].T[6],
            "vy_M": solution[1].T[7],
            "phi1": solution[1].T[8],
            "vphi1": solution[1].T[9],
            "phi2": solution[1].T[10],
            "vphi2": solution[1].T[11],
            "phi_E": solution[1].T[12],
            "vphi_E": solution[1].T[13]
        }

    def plot(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        self.plot_2d(plot_title, window_title)
        self.plot_time_series_earth(plot_title, window_title)
        self.plot_time_series_moon(plot_title, window_title)
        self.plot_time_series_high_tide_1(plot_title, window_title)
        self.plot_time_series_high_tide_2(plot_title, window_title)
        self.plot_phase_earth(plot_title, window_title)
        self.plot_phase_moon(plot_title, window_title)
        self.plot_phase_high_tide_1(plot_title, window_title)
        self.plot_phase_high_tide_2(plot_title, window_title)
        self.plot_center_of_mass(plot_title, window_title)
        self.plot_high_tide_angles(plot_title, window_title)
        self.plot_high_tide_velocity_of_angles(plot_title, window_title)
        self.plot_intrinsic_rotation(plot_title, window_title)
        self.plot_distance_earth_tide(plot_title, window_title)
        self.plot_velocity_high_tides(plot_title, window_title)

    def plot_intrinsic_rotation(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots intrinsic rotation of Earth with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        plt.plot(
            self.solution["t"],
            self.solution["vphi_E"],
            "green",
            label="Angular velocity of Earth rotation"
        )
        plt.xlabel("time in s")
        plt.ylabel("ω in rad/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_velocity_high_tides(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots velocity of high tides with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        vx_1 = self._x_points_velocity_phi(self.solution["phi1"], self.solution["vphi1"])
        vy_1 = self._y_points_velocity_phi(self.solution["phi1"], self.solution["vphi1"])
        vx_2 = self._x_points_velocity_phi(self.solution["phi2"], self.solution["vphi2"])
        vy_2 = self._y_points_velocity_phi(self.solution["phi2"], self.solution["vphi2"])
        plt.plot(
            self.solution["t"],
            np.sqrt(vx_1 ** 2 + vy_1 ** 2),
            label="1st High Tide",
            color="green"
        )
        plt.plot(
            self.solution["t"],
            np.sqrt(vx_2 ** 2 + vy_2 ** 2),
            label="2nd High Tide",
            color="pink"
        )
        plt.xlabel("time in s")
        plt.ylabel("absolute value of velocity of High Tides in m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="center right")
        plt.show()
