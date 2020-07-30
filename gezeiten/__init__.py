# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
This module contains all the business logic of the project "Gezeitenreibung", created during the lecture "Computational
Physics" at TU Darmstadt in 2020.

Various `gezeiten.differential_equations` may be solved by using a `gezeiten.solver.Solver` from `gezeiten.solvers`.
"""

# Don't create documentation for animations module
__pdoc__ = {
    'animations': False,
}
