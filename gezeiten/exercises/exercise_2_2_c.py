# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains plots for exercise 2.2c
"""

from gezeiten.differential_equations.four_body_problem_simple import FourBodyProblemSimple

TIME_BOUNDARIES = (0, 5 * 10 ** 7)


def plot_2_2_c_solve_ivp():
    """
    Exercise 2.2c: plot solve_ivp's solution of simple four body problem
    """
    print("Exercise 2.2c, plots")
    data_points_amount = 5000
    four_body_problem_simple = FourBodyProblemSimple(
        TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    four_body_problem_simple.solve()
    four_body_problem_simple.plot(f"Solved with scipy.integrate.solve_ivp, {data_points_amount} iterations")


def animate_2_2_c_solve_ivp():
    """
    Exercise 2.2c: animate solve_ivp's solution of simple four body problem
    """
    print("Exercise 2.2c, animation")
    data_points_amount = 5000
    four_body_problem_simple = FourBodyProblemSimple(
        TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    four_body_problem_simple.solve()
    four_body_problem_simple.animate(f"Solved with scipy.integrate.solve_ivp, {data_points_amount} iterations")
