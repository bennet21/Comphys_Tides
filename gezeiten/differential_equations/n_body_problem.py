# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.differential_equation.DifferentialEquation` for n body problem.
"""

import numpy as np
from matplotlib import animation
from numpy import sin, cos
import matplotlib.pyplot as plt

from gezeiten.constants import G, m_E, m_M, r_C, r_M, T_M, DEFAULT_PLOT_TITLE, r_E, m_O, k
from gezeiten.differential_equations.four_body_problem_complex import FourBodyProblemComplex
from gezeiten.solvers.magic_solver import MagicSolver


class NBodyProblem(FourBodyProblemComplex):
    """
    Although being named generically as "n body problem", this class actually is quite specific to
    the earth-moon system by default. The initial conditions provided and constants used in the
    differential equation are based on values observed in space and should be changed for other n
    body problems.
    In contrast to FourBodyProblemComplex, this class takes into account more than two tide particles.
    """

    N = 10

    initial_conditions = [
        -r_C,  # x component of Earth
        0,  # x component of velocity of Earth
        0,  # y component of Earth
        -2 * np.pi * r_C / T_M,  # y component of velocity of Earth
        r_M - r_C,  # x component of Moon
        0,  # x component of velocity of Moon
        0,  # y component of Moon
        2 * np.pi * (r_M - r_C) / T_M,  # y component of velocity of Moon
        0,  # angle of intrinsic Earth rotation
        2 * np.pi / (24 * 60 * 60)  # angular velocity of intrinsic Earth rotation
    ]

    for i in range(0, 2 * N, 2):
        initial_conditions.append(np.pi / N * i)    # angle of High Tide i/2
        initial_conditions.append(2 * np.pi / T_M)  # angular velocity of High Tide i/2

    @staticmethod
    def f(t, r):
        """
        Actual differential equation of n-body problem

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
        x_E, vx_E, y_E, vy_E, x_M, vx_M, y_M, vy_M, phi_E, vphi_E = r[:10]
        r_N = r[10:]
        distance_earth_moon = np.sqrt((x_M - x_E) ** 2 + (y_M - y_E) ** 2)
        distance_FN_moon = np.sqrt((r_E * cos(r_N[::2]) + x_E - x_M) ** 2 + (r_E * sin(r_N[::2]) + y_E - y_M) ** 2)
        f_1 = vx_E
        f_2 = -G * m_M * (x_E - x_M) / distance_earth_moon ** 3
        f_3 = vy_E
        f_4 = -G * m_M * (y_E - y_M) / distance_earth_moon ** 3

        sum_M_x = 0
        sum_M_y = 0
        sum_E = 0
        f_N = []
        for i in range(0, 2 * NBodyProblem.N, 2):
            f_N.append(r_N[i + 1])
            f_N.append(
                1 / r_E * (
                    (-G * m_M * (x_E - x_M) / distance_earth_moon ** 3) * sin(r_N[i])
                    - (-G * m_M * (y_E - y_M) / distance_earth_moon ** 3) * cos(r_N[i])
                    - m_M * G * ((r_E * sin(r_N[i]) + y_E - y_M) * cos(r_N[i]) - (r_E * cos(r_N[i]) + x_E - x_M)
                    * sin(r_N[i])) / distance_FN_moon[int(i / 2)] ** 3)
                - r_E * k * abs(r_N[i + 1] - vphi_E) * (r_N[i + 1] - vphi_E)
            )
            sum_M_x += (x_M - r_E * cos(r_N[i]) - x_E) / distance_FN_moon[int(i / 2)] ** 3
            sum_M_y += (y_M - r_E * sin(r_N[i]) - y_E) / distance_FN_moon[int(i / 2)] ** 3
            sum_E += abs(r_N[i + 1] - vphi_E) * (r_N[i + 1] - vphi_E)
        f_5 = vx_M
        f_6 = -G * (m_E * (x_M - x_E) / distance_earth_moon ** 3 + m_O / NBodyProblem.N * sum_M_x)
        f_7 = vy_M
        f_8 = -G * (m_E * (y_M - y_E) / distance_earth_moon ** 3 + m_O / NBodyProblem.N * sum_M_y)
        f_9 = vphi_E
        f_10 = 5 / 2 * r_E * m_O / (NBodyProblem.N * m_E) * k * sum_E

        return [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8, f_9, f_10, *f_N]

    def solve(self, solver=MagicSolver()):
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
            "phi_E": solution[1].T[8],
            "vphi_E": solution[1].T[9],
            "r_N":  solution[1].T[10:],
            "phi1": solution[1].T[10],
            "vphi1": solution[1].T[11],
            "phi2": solution[1].T[12],
            "vphi2": solution[1].T[13],
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
        plt.xlabel("x coordinates in m")
        plt.ylabel("y coordinates in m")
        plt.title(plot_title)
        fig.canvas.set_window_title(window_title)
        plt.legend(loc="upper right")
        earth, = ax.plot([], [], 'o', label="Earth")
        moon, = ax.plot([], [], 'o', label=f"Moon (1/{moon_scale})")
        high_tides = []
        for i in range(self.N):
            high_tides.append(ax.plot([], [], 'o')[0])
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
            for j in range(self.N):
                high_tides[j].set_data(
                    self._x_points_phi(self.solution["r_N"][2 * j])[i],
                    self._y_points_phi(self.solution["r_N"][2 * j])[i]
                )
            time_text.set_text(f"{np.ceil(self.solution['t'][i] / (24 * 60 * 60))} days")
            return (earth, moon, *high_tides, time_text)

        animation.FuncAnimation(fig, animate, frames=self.solution['t'].size,
                                interval=1, blit=True)
        plt.show()
