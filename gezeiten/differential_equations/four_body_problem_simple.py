# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.differential_equation.DifferentialEquation` for "simple" four body problem.
"""

import numpy as np
from numpy import sin, cos
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from gezeiten.constants import G, m_E, r_C, m_M, r_E, r_M, T_M, m_O, DEFAULT_PLOT_TITLE
from gezeiten.differential_equations.two_body_problem import TwoBodyProblem
from gezeiten.solvers.magic_solver import MagicSolver


class FourBodyProblemSimple(TwoBodyProblem):
    """
    Although being named generically as "four body problem", this class actually is quite specific to
    the earth-moon system by default. The initial conditions provided and constants used in the
    differential equation are based on values observed in space and should be changed for other four
    body problems.
    In contrast to TwoBodyProblem, this class respects the influence of tidal forces on the system.
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
        2 * np.pi / T_M  # angular velocity of second high tide
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

    @staticmethod
    def f(t, r):  # Constraint: x_F ** 2 + y_F ** 2 = r_E ** 2
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
        x_E, vx_E, y_E, vy_E, x_M, vx_M, y_M, vy_M, phi1, vphi1, phi2, vphi2 = r
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
                    + 1/2 * m_O * (
                        (x_M - r_E * cos(phi1) - x_E) / distance_F1_moon ** 3
                        + (x_M - r_E * cos(phi2) - x_E) / distance_F2_moon ** 3)
                    )
                )
        f_7 = vy_M
        f_8 = (
                -G * (
                    m_E * (y_M - y_E) / distance_earth_moon ** 3
                    + 1/2 * m_O * (
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
                )
        f_11 = vphi2
        f_12 = (
                1/r_E * (
                    (-G * m_M * (x_E - x_M) / distance_earth_moon ** 3) * sin(phi2)
                    - (-G * m_M * (y_E - y_M) / distance_earth_moon ** 3) * cos(phi2)
                    - m_M * G * ((r_E * sin(phi2) + y_E - y_M) * cos(phi2) - (r_E * cos(phi2) + x_E - x_M) * sin(phi2))
                    / distance_F2_moon ** 3)
                )
        return [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, f_11, f_12]

    def solve(self, solver=MagicSolver()):
        """
        Solves the differential equation of the four body problem by using the solver passed as an argument.

        Once finished, the two body problem will have a solution field which is a dictionary with entries
        t, x_E, y_E, vx_E, vy_E, x_M, y_M, vx_M, vy_M, phi1, vphi1, phi2, vphi2, each containing a list of floats.

        Attributes
        ----------
        solver: gezeiten.solver.Solver
            Solver which solves the differential equation; by default MagicSolver
        """
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
            "vphi2": solution[1].T[11]
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
        self.plot_distance_earth_tide(plot_title, window_title)

    def animate(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Animates `solution` with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        ax.grid()
        ax.plot(
            self.solution["x_E"],
            self.solution["y_E"],
            "blue",
            label="Earth"
        )
        moon_scale = 14
        ax.plot(
            self.solution["x_M"] / moon_scale,
            self.solution["y_M"] / moon_scale,
            "orange",
            label=f"Moon (1/{moon_scale})"
        )
        plt.plot(
            self._x_points_phi(self.solution["phi1"]),
            self._y_points_phi(self.solution["phi1"]),
            "green",
            label="1st High Tide"
        )
        plt.plot(
            self._x_points_phi(self.solution["phi2"]),
            self._y_points_phi(self.solution["phi2"]),
            "pink",
            label="2nd High Tide"
        )
        plt.xlabel("x coordinates in m")
        plt.ylabel("y coordinates in m")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper right")
        earth, = ax.plot([], [], 'o', label="Earth")
        moon, = ax.plot([], [], 'o', label=f"Moon (1/{moon_scale})")
        high_tide_1, = ax.plot([], [], 'o', label="1st High Tide")
        high_tide_2, = ax.plot([], [], 'o', label="2nd High Tide")
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

        def animate(i):
            earth.set_data(
                self.solution["x_E"][i],
                self.solution["y_E"][i]
            )
            moon.set_data(
                self.solution["x_M"][i] / moon_scale,
                self.solution["y_M"][i] / moon_scale
            )
            high_tide_1.set_data(
                self._x_points_phi(self.solution["phi1"])[i],
                self._y_points_phi(self.solution["phi1"])[i]
            )
            high_tide_2.set_data(
                self._x_points_phi(self.solution["phi2"])[i],
                self._y_points_phi(self.solution["phi2"])[i]
            )
            time_text.set_text(f"{np.ceil(self.solution['t'][i] / (24 * 60 * 60))} days")
            return earth, moon, high_tide_1, high_tide_2, time_text

        animation.FuncAnimation(fig, animate, frames=self.solution['t'].size,
                                interval=30, blit=True)
        plt.show()

    def plot_2d(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots positions of Earth, Moon and high tides with matplotlib

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
        plt.plot(
            self._x_points_phi(self.solution["phi1"]),
            self._y_points_phi(self.solution["phi1"]),
            "green",
            label="1st High Tide"
        )
        plt.plot(
            self._x_points_phi(self.solution["phi2"]),
            self._y_points_phi(self.solution["phi2"]),
            "pink",
            label="2nd High Tide"
        )
        plt.xlabel("x coordinates in m")
        plt.ylabel("y coordinates in m")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def _x_points_phi(self, phi_points):
        return r_E * cos(phi_points) + self.solution["x_E"]

    def _y_points_phi(self, phi_points):
        return r_E * sin(phi_points) + self.solution["y_E"]

    def _x_points_velocity_phi(self, phi_points, phi_velocity_points):
        return -1 * self._y_points_phi(phi_points) * phi_velocity_points

    def _y_points_velocity_phi(self, phi_points, phi_velocity_points):
        return self._x_points_phi(phi_points) * phi_velocity_points

    def plot_time_series_high_tide_1(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of first high tide with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        self.plot_time_series_high_tide(self.solution["phi1"], self.solution["vphi1"], "1st", plot_title, window_title)

    def plot_time_series_high_tide_2(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of first high tide with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        self.plot_time_series_high_tide(self.solution["phi2"], self.solution["vphi2"], "2nd", plot_title, window_title)

    def plot_time_series_high_tide(self, phi_points, vphi_points, number, plot_title="",
                                   window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of high tide with matplotlib

        Attributes
        ----------
        phi_points: array
            Containing values of angle phi
        vphi_points: array
            Containing values of angular velocity phi
        number: string
            "1st" or "2nd" high tide
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        plt.plot(
            self.solution["t"],
            self._x_points_phi(phi_points),
            label=f"x coordinates {number} high tide"
        )
        plt.plot(
            self.solution["t"],
            self._y_points_phi(phi_points),
            label=f"y coordinates {number} high tide"
        )
        plt.plot(
            self.solution["t"],
            10e5 * self._x_points_velocity_phi(phi_points, vphi_points),
            label=f"x velocity {number} high tide"
        )
        plt.plot(
            self.solution["t"],
            10e5 * self._y_points_velocity_phi(phi_points, vphi_points),
            label=f"y velocity {number} high tide"
        )
        plt.xlabel("time in s")
        plt.ylabel("position in m, velocity in 10^5 m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_phase_high_tide_1(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of Moon with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        self.plot_phase_high_tide(self.solution["phi1"], self.solution["vphi1"], "1st", plot_title, window_title)

    def plot_phase_high_tide_2(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of Moon with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        self.plot_phase_high_tide(self.solution["phi2"], self.solution["vphi2"], "2nd", plot_title, window_title)

    def plot_phase_high_tide(self, phi_points, vphi_points, number, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots time series of Moon with matplotlib
        """
        fig = plt.figure()
        plt.plot(
            self._x_points_phi(phi_points),
            self._x_points_velocity_phi(phi_points, vphi_points),
            label=f"x coordinates {number} high tide"
        )
        plt.plot(
            self.solution["y_E"],
            self.solution["vy_E"],
            label=f"y coordinates {number} high tide"
        )
        plt.xlabel("position in m")
        plt.ylabel("velocity in m/s")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_high_tide_angles(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots angles of high tides with matplotlib

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
            self.solution["phi1"],
            "green",
            label="1st High Tide"
        )
        plt.plot(
            self.solution["t"],
            self.solution["phi2"],
            "pink",
            label="2nd High Tide"
        )
        plt.xlabel("time in s")
        plt.ylabel("φ in rad")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def plot_high_tide_velocity_of_angles(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots high tide velocity with matplotlib

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
            self.solution["vphi1"],
            "green",
            label="1st High Tide"
        )
        plt.plot(
            self.solution["t"],
            self.solution["vphi2"],
            "pink",
            label="2nd High Tide"
        )
        plt.xlabel("time in s")
        plt.ylabel("velocity of φ in rad")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper left")
        plt.show()

    def _render_center_of_mass(self):
        x_points_earth = self.solution["x_E"]
        y_points_earth = self.solution["y_E"]
        x_points_moon = self.solution["x_M"]
        y_points_moon = self.solution["y_M"]
        x_points_F1 = self._x_points_phi(self.solution["phi1"])
        y_points_F1 = self._y_points_phi(self.solution["phi1"])
        x_points_F2 = self._x_points_phi(self.solution["phi2"])
        y_points_F2 = self._y_points_phi(self.solution["phi2"])
        self.r_points_center = (
                                       m_E * np.array([x_points_earth, y_points_earth])
                                       + m_M * np.array([x_points_moon, y_points_moon])
                                       + 0.5 * m_O * np.array([x_points_F1, y_points_F1])
                                       + 0.5 * m_O * np.array([x_points_F2, y_points_F2])
                               ) / (m_E + m_M + m_O)

    def plot_distance_earth_tide(self, plot_title="", window_title=DEFAULT_PLOT_TITLE):
        """
        Plots distance of high tides to Earth with matplotlib

        Attributes
        ----------
        plot_title: string
            Title to be attached to the plots
        window_title: string
            Title to be attached to the window
        """
        fig = plt.figure()
        x_rel1 = self._x_points_phi(self.solution["phi1"]) - self.solution["x_E"]
        y_rel1 = self._y_points_phi(self.solution["phi1"]) - self.solution["y_E"]
        x_rel2 = self._x_points_phi(self.solution["phi2"]) - self.solution["x_E"]
        y_rel2 = self._y_points_phi(self.solution["phi2"]) - self.solution["y_E"]
        r_rel1 = np.sqrt(x_rel1 ** 2 + y_rel1 ** 2)
        r_rel2 = np.sqrt(x_rel2 ** 2 + y_rel2 ** 2)
        plt.plot(self.solution["t"], r_rel1, label="1st High Tide", color="green")
        plt.plot(self.solution["t"], r_rel2, label="2nd High Tide", color="pink")
        plt.title(plot_title)
        plt.xlabel("time in s")
        plt.ylabel("Distance to Earth in m")
        plt.legend(loc="upper left")
        fig.canvas.set_window_title(window_title)
        plt.show()
