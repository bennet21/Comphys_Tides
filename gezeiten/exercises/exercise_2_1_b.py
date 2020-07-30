# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains plots for exercise 2.1b
"""

from gezeiten.constants import DEFAULT_TIME_BOUNDARIES
from gezeiten.differential_equations.two_body_problem import TwoBodyProblem
from gezeiten.solvers.euler_solver import EulerSolver
from gezeiten.solvers.runge_kutta_solver import RungeKuttaSolver


def plot_2_1_b_solve_ivp():
    """
    Exercise 2.1b: plot `scipy.integrate.solve_ivp`'s solution of the two body problem
    """
    print("Exercise 2.1b, using scipy.integrate.solve_ivp")
    data_points_amount = 150
    two_body_problem = TwoBodyProblem(
        DEFAULT_TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    two_body_problem.solve()
    two_body_problem.plot(f"Solved by scipy.integrate.solve_ivp, {data_points_amount} datapoints")


def plot_2_1_b_runge_kutta():
    """
    Exercise 2.1b: plot `gezeiten.solvers.runge_kutta_solver.RungeKuttaSolver`'s solution of the two body problem
    """
    print("Exercise 2.1b, using Runge Kutta")
    data_points_amount = 5000
    two_body_problem = TwoBodyProblem(
        DEFAULT_TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    two_body_problem.solve(RungeKuttaSolver())
    two_body_problem.plot(f"Solved with Runge Kutta, {data_points_amount} iterations")


def plot_2_1_b_euler():
    """
    Exercise 2.1b: plot Euler's solution of the two body problem
    """
    print("Exercise 2.1b, using Euler")
    data_points_amount = 5000
    two_body_problem = TwoBodyProblem(
        DEFAULT_TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    two_body_problem.solve(EulerSolver())
    two_body_problem.plot(f"Solved with Euler, {data_points_amount} iterations")
