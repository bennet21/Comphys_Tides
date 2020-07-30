# Copyright (c) 2016-2019 elbanic <elbanic12@naver.com>
# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Original source code at:
# https://github.com/elbanic/SolarSystem
#

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame

from gezeiten.animations.constants import RESOURCES_DIRECTORY


class AstronomicalObject:
    texture_id = -1
    radius = -1
    x_position, y_position, z_position = 0.0, 0.0, 0.0
    x_rotation, y_rotation, z_rotation = 0.0, 0.0, 0.0

    def __init__(self, radius, x_points, y_points, orbit_color=(1, 0.5, 0.0)):
        """
        Astronomical object used for Earth and Moon
        :param orbit_color: Default orbit color is orange
        """
        self.radius = radius
        self.x_points = x_points
        self.y_points = y_points
        self.orbit_points = []
        self.orbit_color = orbit_color

    def update_position(self, point_iterator):
        self.x_position = self.x_points[point_iterator]
        self.y_position = self.y_points[point_iterator]

    def update_rotation(self, period):
        self.z_rotation = self.z_rotation + period

    def load_texture(self, path):
        texture_surface = pygame.image.load(os.path.join(RESOURCES_DIRECTORY, path))
        texture_data = pygame.image.tostring(texture_surface, "RGBX", 1)

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(), texture_surface.get_height(), 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

    def draw(self, quadratic):
        glPushMatrix()
        glTranslatef(self.x_position, self.y_position, self.z_position)
        glColor3f(1.0, 0.0, 0.0)
        self._rotate()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        gluSphere(quadratic, self.radius, 128, 128)
        glDisable(GL_TEXTURE_2D)  # a pair or needs removing to show the texture
        glPopMatrix()

    def _rotate(self):
        glRotatef(self.x_rotation, 1.0, 0.0, 0.0)
        glRotatef(self.y_rotation, 0.0, 1.0, 0.0)
        glRotatef(self.z_rotation, 0.0, 0.0, 1.0)

    def update_orbit_points(self, point_iterator):
        self._reset_orbit_at_start(point_iterator)
        self.orbit_points.append((self.x_position, self.y_position, self.z_position))

    def _reset_orbit_at_start(self, point_iterator):
        if point_iterator == 0:
            self.orbit_points = []

    def draw_orbit(self):
        glPushMatrix()
        glColor3f(self.orbit_color[0], self.orbit_color[1], self.orbit_color[2])
        glDisable(GL_LIGHTING)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glLineWidth(1.0)
        self._draw_orbit_points()
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def _draw_orbit_points(self):
        glBegin(GL_LINES)
        for i in range(len(self.orbit_points)):
            glVertex3f(self.orbit_points[i][0], self.orbit_points[i][1], self.orbit_points[i][2])
        glEnd()
