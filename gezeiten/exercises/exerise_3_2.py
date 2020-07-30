# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains plots for exercise 3.2
"""

from gezeiten.differential_equations.n_body_problem import NBodyProblem

TIME_BOUNDARIES = (0, 5 * 10 ** 7)


def plot_3_2_solve_ivp():
    """
    Exercise 3.2: plot solve_ivp's solution of complex n body problem
    """
    print("Exercise 3.2, plots")
    data_points_amount = 5000
    n_body_problem = NBodyProblem(
        TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    n_body_problem.solve()
    n_body_problem.plot(f"Solved with scipy.integrate.solve_ivp, {data_points_amount} iterations")


def animate_3_2_solve_ivp():
    """
    Exercise 3.2: animate solve_ivp's solution of complex n body problem
    """
    print("Exercise 3.2, animation")
    data_points_amount = 5000
    n_body_problem = NBodyProblem(
        TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    n_body_problem.solve()
    n_body_problem.animate(f"Solved with scipy.integrate.solve_ivp, {data_points_amount} iterations")
