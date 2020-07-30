# Copyright (c) 2016-2019 elbanic <elbanic12@naver.com>
# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Original source code at:
# https://github.com/elbanic/SolarSystem
#

from pygame.constants import OPENGL, DOUBLEBUF

WINDOW_SIZE_WIDTH = 1920
WINDOW_SIZE_HEIGHT = 980
DEFAULT_WINDOW_TITLE = "Animation of numerically solved earth-moon problem - Bennet Weiss and Nico Alt"

VIDEO_FLAGS = OPENGL | DOUBLEBUF

RESOURCES_DIRECTORY = 'resources'
ZOOM_OUT_MAX = 20
BACKGROUND_TEXTURE_FILE = 'stars_milky_way.jpg'

DEFAULT_OBSERVER_POSITION = (0.0, -1.6, 10.0)
DEFAULT_OBSERVER_TURN = (0.0, 1.0, 0.0)
DEFAULT_LENGTH_TO_CENTER = (0.0, 0.0, -30.0)
DEFAULT_ANGLE = (0, 0)
DEFAULT_OBSERVER_ROTATION = (-60.0, 0.0, 0.0)

EARTH_RADIUS = 0.25
EARTH_ORBIT_COLOR = (0.90, 0.91, 0.98)  # silver
EARTH_TEXTURE_FILE = 'earth.bmp'
EARTH_ROTATION_SPEED = 0.5
MOON_RADIUS = 0.1
MOON_ORBIT_COLOR = (0.858824, 0.858824, 0.439216)  # goldenrod
MOON_TEXTURE_FILE = 'moon.bmp'
MOON_ROTATION_SPEED = 1
