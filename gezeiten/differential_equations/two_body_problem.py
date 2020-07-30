# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.differential_equation.DifferentialEquation` for two body problem.
"""

import numpy as np
import matplotlib.pyplot as plt

from gezeiten.constants import G, m_E, m_M, r_C, r_M, T_M, DEFAULT_PLOT_TITLE
from gezeiten.differential_equation import DifferentialEquation
from gezeiten.solvers.magic_solver import MagicSolver


class TwoBodyProblem(DifferentialEquation):
    """
    Although being named generically as "two body problem", this class actually is quite specific to
    the earth-moon system by default. The initial conditions provided and constants used in the
    differential equation are based on values observed in space and should be changed for other two
    body problems.
    """
    initial_conditions = (
        -r_C,  # x component of Earth
        0,  # x component of velocity of Earth
        0,  # y component of Earth
        -2 * np.pi * r_C / T_M,  # y component of velocity of Earth
        r_M - r_C,  # x component of Moon
        0,  # x component of velocity of Moon
        0,  # y component of Moon
        2 * np.pi * (r_M - r_C) / T_M  # y component of velocity of Moon
    )

    def __init__(self, time_boundaries, data_points_amount):
        """
        Initializes the two body problem, by default with initial conditions of the earth-moon system.

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

    @staticmethod
    def f(t, r):
        """
        Actual differential equation of two body problem

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
        x_E, vx_E, y_E, vy_E, x_M, vx_M, y_M, vy_M = r
        abs_r = np.sqrt((x_E - x_M) ** 2 + (y_E - y_M) ** 2)
        f_1 = vx_E
        f_2 = -G * m_M * (x_E - x_M) / abs_r ** 3
        f_3 = vy_E
        f_4 = -G * m_M * (y_E - y_M) / abs_r ** 3
        f_5 = vx_M
        f_6 = -G * m_E * (x_M - x_E) / abs_r ** 3
        f_7 = vy_M
        f_8 = -G * m_E * (y_M - y_E) / abs_r ** 3
        return [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8]

    def solve(self, solver=MagicSolver()):
        """
        Solves the differential equation of the two body problem by using the solver passed as an argument.

        Once finished, the two body problem will have a solution field which is a dictionary with entries
        t, x_E, y_E, vx_E, vy_E, x_M, y_M, vx_M, vy_M each containing a list of floats.

        Attributes
        ----------
        solver: gezeiten.solver.Solver
            Solver which solves the differential equation; by default MagicSolver
        """
        solution = solver.solve(self)
        self.solution = {
            "t": solution[0],
            "x_E": solution[1].T[0],
            "y_E": solution[1].T[2],
            "vx_E": solution[1].T[1],
            "vy_E": solution[1].T[3],
            "x_M": solution[1].T[4],
            "y_M": solution[1].T[6],
            "vx_M": solution[1].T[5],
            "vy_M": solution[1].T[7],
        }

    def plot(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Creates various plots with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        self.plot_2d(plot_title, window_title)
        self.plot_time_series_earth(plot_title, window_title)
        self.plot_time_series_moon(plot_title, window_title)
        self.plot_phase_earth(plot_title, window_title)
        self.plot_phase_moon(plot_title, window_title)

    def plot_2d(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots positions of Earth and Moon with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        plt.plot(
            self.solution["x_E"],
            self.solution["y_E"],
            "blue",
            label="Earth"
        )
        plt.plot(
            self.solution["x_M"],
            self.solution["y_M"],
            "orange",
            label="Moon"
        )
        plt.xlabel("x coordinates in m")
        plt.ylabel("y coordinates in m")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_time_series_earth(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of Earth with matplotlib

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
            self.solution["x_E"],
            label="x coordinates Earth"
        )
        plt.plot(
            self.solution["t"],
            self.solution["y_E"],
            label="y coordinates Earth"
        )
        plt.plot(
            self.solution["t"],
            10e5 * self.solution["vx_E"],
            label="x velocity Earth"
        )
        plt.plot(
            self.solution["t"],
            10e5 * self.solution["vy_E"],
            label="y velocity Earth"
        )
        plt.xlabel("time in s")
        plt.ylabel("position in m, velocity in 10^5 m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_time_series_moon(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of moon with matplotlib

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
            self.solution["x_M"],
            label="x coordinates Moon"
        )
        plt.plot(
            self.solution["t"],
            self.solution["y_M"],
            label="y coordinates Moon"
        )
        plt.plot(
            self.solution["t"],
            10e5 * self.solution["vx_M"],
            label="x velocity Moon"
        )
        plt.plot(
            self.solution["t"],
            10e5 * self.solution["vy_M"],
            label="y velocity Moon"
        )
        plt.xlabel("time in s")
        plt.ylabel("position in m, velocity in 10^5 m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_phase_earth(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of Moon with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        plt.plot(
            self.solution["x_E"],
            self.solution["vx_E"],
            label="x coordinates Earth"
        )
        plt.plot(
            self.solution["y_E"],
            self.solution["vy_E"],
            label="y coordinates Earth"
        )
        plt.xlabel("position in m")
        plt.ylabel("velocity in m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_phase_moon(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of moon with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        plt.plot(
            self.solution["x_M"],
            self.solution["vx_M"],
            label="x coordinates Moon"
        )
        plt.plot(
            self.solution["y_M"],
            self.solution["vy_M"],
            label="y coordinates Moon"
        )
        plt.xlabel("position in m")
        plt.ylabel("velocity in m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_center_of_mass(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots position of center of mass with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        self._render_center_of_mass()
        fig = plt.figure()
        plt.plot(
            self.r_points_center[0],
            self.r_points_center[1],
            "black",
            label="Center of mass"
        )
        plt.xlabel("x coordinates in m")
        plt.ylabel("y coordinates in m")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def _render_center_of_mass(self):
        x_points_earth = self.solution["x_E"]
        y_points_earth = self.solution["y_E"]
        x_points_moon = self.solution["x_M"]
        y_points_moon = self.solution["y_M"]
        self.r_points_center = (m_E * np.array([x_points_earth, y_points_earth])
                                + m_M * np.array([x_points_moon, y_points_moon])) / (m_E + m_M)
