# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
"""
This file contains various (mostly natural) constants used all around this project.
"""

DEFAULT_TIME_BOUNDARIES = (0, 60 * 24 * 60 * 60)
"""
Default time boundaries used for solving a `gezeiten.differential_equation.DifferentialEquation`
"""
DEFAULT_PLOT_TITLE = "Numerically solved earth-moon problem - Bennet Weiss and Nico Alt"
"""
Default title used for plots and animations
"""

m_E = 5.9721986e24
"""
Mass of Earth
"""

m_O = 0.0014e24
"""
Mass of Oceans
"""

r_E = 6.3675e6
"""
Radius of Earth
"""

m_M = 7.3459e22
"""
Mass of Moon
"""

r_M = 3.836e8
"""
Radius of Moon's orbit around Earth
"""

T_M = 27.32166140 * 24 * 3600
"""
Time for moon to do a full turn around Earth
"""

T_E = 86164.100
"""
Time of Earth's intrinsic rotation
"""

tau = 0.0021
"""
Amount of Earth day length's increment in 100 years
"""

G = 6.67430e-11
"""
Gravitational constant
"""

r_C = r_M * m_M / (m_M + m_E)
"""
Distance of center of mass of earth-moon system, from Earth
"""

k = 2e-12
"""
Constant of friction in complex 4 body problem
"""
