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

from gezeiten.animations.constants import ZOOM_OUT_MAX, RESOURCES_DIRECTORY


class Background:
    texture_id = -1

    def load_texture(self, path):
        background_image = pygame.image.load(os.path.join(RESOURCES_DIRECTORY, path))
        background_image_data = pygame.image.tostring(background_image, "RGBX", 1)

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, background_image.get_width(), background_image.get_height(), 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, background_image_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

    def draw(self, quadratic):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        gluSphere(quadratic, ZOOM_OUT_MAX, 5, 5)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
