# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
Contains base class used for solvers.
"""


class Solver:
    """
    Base class for solvers implemented in `gezeiten.solvers`.
    """

    def solve(self, differential_equation):
        """
        Integrate a system of ordinary differential equations.

        Parameters
        ----------
        differential_equation : Instance of `gezeiten.differential_equation.DifferentialEquation`
            Differential equation to be solved

        Returns
        -------
        array of arrays, shape of 2nd array (len(t), len(y0))
            1st array containing the values of time.
            2nd array containing the value of y for each desired time in t,
            with the initial value `y0` in the first row.
        """
        pass
