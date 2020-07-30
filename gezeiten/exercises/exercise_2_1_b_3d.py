# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains animations for exercise 2.1b
"""

from gezeiten.animations.constants import DEFAULT_WINDOW_TITLE
from gezeiten.animations.three_dimensions import ThreeDimensionsAnimation
from gezeiten.constants import DEFAULT_TIME_BOUNDARIES
from gezeiten.differential_equations.two_body_problem import TwoBodyProblem


def animate_2_1_b_solve_ivp_3d():
    """
    Exercise 2.1b: render 3D animation of two body problem with correct initial conditions.
    """
    print("Exercise 2.1b, 3D animation with correct initial conditions")
    _render()


def animate_2_1_b_solve_ivp_3d_moon_too_fast():
    """
    Exercise 2.1b: render 3D animation of two body problem with modified velocity of the moon's orbit.
    """
    print("Exercise 2.1b, 3D animation with modified velocity of the moon's orbit")
    modified_initial_conditions = list(TwoBodyProblem.initial_conditions)
    modified_initial_conditions[7] *= 1.3
    _render(
        "Animation of numerically solved earth-moon problem with moon rotating 1.3 times as fast - "
        "Bennet Weiss and Nico Alt",
        modified_initial_conditions
    )


def _render(title=DEFAULT_WINDOW_TITLE, initial_conditions=TwoBodyProblem.initial_conditions):
    two_body_problem = TwoBodyProblem(
        DEFAULT_TIME_BOUNDARIES,
        data_points_amount=5000
    )
    two_body_problem.initial_conditions = initial_conditions
    two_body_problem.solve()
    animation = ThreeDimensionsAnimation(two_body_problem, title)
    animation.render()
