# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains base class used for differential equations.
"""

from gezeiten.solvers.magic_solver import MagicSolver


class DifferentialEquation:
    """
    Base class used for differential equations.

    Attributes
    ----------
    data_points_amount: int
        Amount of points created by `gezeiten.solvers`.

    differential_equation_function : callable
        Right-hand side of the system. The calling signature is ``fun(t, y)``.
        Here `t` is a scalar, and there are two options for the ndarray `y`:
        It can either have shape (n,); then `fun` must return array_like with
        shape (n,). Alternatively, it can have shape (n, k); then `fun`
        must return an array_like with shape (n, k), i.e., each column
        corresponds to a single column in `y`. The choice between the two
        options is determined by `vectorized` argument (see below). The
        vectorized implementation allows a faster approximation of the Jacobian
        by finite differences (required for stiff solvers).

        (Copied from `scipy.integrate.solve_ivp`'s docs)

    initial_conditions : array_like, shape (n,)
        Initial state. For problems in the complex domain, pass `y0` with a
        complex data type (even if the initial value is purely real).

        (Copied from `scipy.integrate.solve_ivp`'s docs)

    time_boundaries : 2-tuple of floats
        Interval of integration (t0, tf). The solver starts with t=t0 and
        integrates until it reaches t=tf.

        (Copied from `scipy.integrate.solve_ivp`'s docs)

    solution : array_like, shape (n + 1,)
        Array containing the solution computed by `gezeiten.solver.Solver`.
    """
    data_points_amount = 1
    differential_equation_function = None
    initial_conditions = (0,)
    time_boundaries = (0, 1)

    solution = None

    def __init__(self, differential_equation_function, initial_conditions, time_boundaries, data_points_amount):
        self.differential_equation_function = differential_equation_function
        self.initial_conditions = initial_conditions
        self.time_boundaries = time_boundaries
        self.data_points_amount = data_points_amount

    def solve(self, solver=MagicSolver()):
        """
        Solves the differential equation by using the solver passed as an argument.

        Once finished, the differential equation object will have a `solution` field which contains
        the solution.

        Attributes
        ----------
        solver: gezeiten.solver.Solver
            Solver which solves the differential equation; by default MagicSolver
        """
        self.solution = solver.solve(self)

    def plot(self):
        """
        Plots the differential equation.
        """
        pass
