# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.solver.Solver` based on Runge Kutta 4th order algorithm.
"""

from gezeiten.solver import Solver
import numpy as np


class RungeKuttaSolver(Solver):
    """
    `gezeiten.solver.Solver` based on Runge Kutta 4th order algorithm.
    """

    def solve(self, differential_equation):
        a, b = differential_equation.time_boundaries
        h = (b - a) / differential_equation.data_points_amount
        t_points = np.arange(a, b, h)
        r = np.array(differential_equation.initial_conditions)
        r_points = [r]
        for t in t_points[1:]:
            k_1 = h * np.array(differential_equation.differential_equation_function(t, r))
            k_2 = h * np.array(differential_equation.differential_equation_function(t + h / 2, r + k_1 / 2))
            k_3 = h * np.array(differential_equation.differential_equation_function(t + h / 2, r + k_2 / 2))
            k_4 = h * np.array(differential_equation.differential_equation_function(t + h, r + k_3))
            r += (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6
            r_points = np.append(r_points, [r], axis=0)
        return [
            t_points,
            r_points
        ]
