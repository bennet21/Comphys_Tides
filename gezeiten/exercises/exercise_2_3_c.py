# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains exercise 2.3c
"""
import numpy as np

from gezeiten.constants import DEFAULT_TIME_BOUNDARIES, tau, m_O
from gezeiten.differential_equations.four_body_problem_complex import FourBodyProblemComplex


def fit_2_3_c_solve_ivp():
    """
    Exercise 2.3c: fit mass of oceans to match `gezeiten.constants.tau`
    """
    print("Exercise 2.3c")
    data_points_amount = 5000
    four_body_problem_complex = FourBodyProblemComplex(
        (0, 2 * 365.24 * 24 * 3600),
        data_points_amount=data_points_amount
    )
    _fit_mass_oceans(four_body_problem_complex)


def _fit_mass_oceans(four_body_problem_complex):
    current_m_O = m_O
    accuracy = 0.01
    four_body_problem_complex.solve(m_O=current_m_O)
    current_tau = _calculate_current_tau(four_body_problem_complex)
    print(f"Current tau ratio: {round(current_tau / tau)}")
    while abs(1 - current_tau / tau) > accuracy:
        current_m_O /= (current_tau / tau)
        four_body_problem_complex.solve(m_O=current_m_O)
        current_tau = _calculate_current_tau(four_body_problem_complex)
        print(f"Current tau ratio: {current_tau / tau}")
    print(f"Final ocean mass: {round(current_m_O / 10 ** 12)} Gt")
    print(f"Ocean mass ratio: {current_m_O / m_O}")


def _calculate_current_tau(four_body_problem_complex):
    t_one_year = int(len(four_body_problem_complex.solution["t"]) / 2)  # to respect settling time of system
    final_angular_velocity = (
            four_body_problem_complex.solution["vphi_E"][t_one_year]
            + 100 * 365.24 * 24 * 3600  # 100 years
            * (
                    (
                            four_body_problem_complex.solution["vphi_E"][-1]
                            - four_body_problem_complex.solution["vphi_E"][t_one_year]
                    ) /
                    (
                            four_body_problem_complex.solution["t"][-1]
                            - four_body_problem_complex.solution["t"][t_one_year]
                    )
            )
    )
    current_tau = (
            2 * np.pi
            * (
                    1 / final_angular_velocity
                    - 1 / four_body_problem_complex.solution["vphi_E"][t_one_year]
            )
    )
    return current_tau
