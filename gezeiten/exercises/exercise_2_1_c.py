# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains plots for exercise 2.1c
"""

from gezeiten.constants import DEFAULT_TIME_BOUNDARIES
from gezeiten.differential_equations.two_body_problem import TwoBodyProblem


def plot_2_1_c_solve_ivp():
    """
    Exercise 2.1c: plot solve_ivp's solution of the center of mass of the two body problem
    """
    print("Exercise 2.1c")
    two_body_problem = TwoBodyProblem(
        DEFAULT_TIME_BOUNDARIES,
        data_points_amount=500000
    )
    two_body_problem.solve()
    two_body_problem.plot_center_of_mass("Solved by scipy.integrate.odeint, 5000 datapoints")
