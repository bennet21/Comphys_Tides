# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains `gezeiten.solver.Solver` based on `scipy.integrate.solve_ivp` function.
"""

import numpy as np
from scipy import integrate

from gezeiten.solver import Solver


class MagicSolver(Solver):
    """
    gezeiten.solver.Solver` based on `scipy.integrate.solve_ivp` function.

    Attributes
    ----------
    method: string or `OdeSolver`, optional
        Integration method to use. See `scipy.integrate.solve_ivp` for full documentation.
    """

    def __init__(self, method="Radau"):
        self.method = method

    def solve(self, differential_equation):
        a, b = differential_equation.time_boundaries
        t_points = np.linspace(a, b, differential_equation.data_points_amount)
        solution = integrate.solve_ivp(
            differential_equation.differential_equation_function,
            differential_equation.time_boundaries,
            differential_equation.initial_conditions,
            method=self.method,
            t_eval=t_points,
            vectorized=True
        )
        return [
            solution.t,
            solution.y.T
        ]
