# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.solver.Solver` based on Euler algorithm.
"""

import numpy as np

from gezeiten.solver import Solver


class EulerSolver(Solver):
    """
    `gezeiten.solver.Solver` based on Euler algorithm.
    """

    def solve(self, differential_equation):
        a, b = differential_equation.time_boundaries
        h = (b - a) / differential_equation.data_points_amount

        t_points = np.arange(a, b, h)

        r = np.array(differential_equation.initial_conditions, float)
        r_points = np.array([r])
        for t in t_points[1:]:
            r += h * np.array(differential_equation.differential_equation_function(t, r), float)
            r_points = np.append(r_points, [np.array(r)], axis=0)
        return [
            t_points,
            r_points
        ]
