# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains plots for exercise 2.3b
"""

from gezeiten.differential_equations.four_body_problem_complex import FourBodyProblemComplex

TIME_BOUNDARIES = (0, 5 * 10 ** 7)


def plot_2_3_b_solve_ivp():
    """
    Exercise 2.3b: plot solve_ivp's solution of complex four body problem
    """
    print("Exercise 2.3b, plots")
    data_points_amount = 5000
    four_body_problem_complex = FourBodyProblemComplex(
        TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    four_body_problem_complex.solve()
    four_body_problem_complex.plot(f"Solved with scipy.integrate.solve_ivp, {data_points_amount} iterations")


def animate_2_3_b_solve_ivp():
    """
    Exercise 2.3b: animate solve_ivp's solution of complex four body problem
    """
    print("Exercise 2.3b, animation")
    data_points_amount = 5000
    four_body_problem_complex = FourBodyProblemComplex(
        TIME_BOUNDARIES,
        data_points_amount=data_points_amount
    )
    four_body_problem_complex.solve()
    four_body_problem_complex.animate(f"Solved with scipy.integrate.solve_ivp, {data_points_amount} iterations")
