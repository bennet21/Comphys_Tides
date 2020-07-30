# Copyright (c) 2016-2019 elbanic <elbanic12@naver.com>
# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Original source code at:
# https://github.com/elbanic/SolarSystem
#
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from gezeiten.animations.background import Background
from gezeiten.animations.constants import WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT, DEFAULT_OBSERVER_POSITION, \
    DEFAULT_OBSERVER_ROTATION, DEFAULT_OBSERVER_TURN, DEFAULT_ANGLE, DEFAULT_LENGTH_TO_CENTER, EARTH_RADIUS, \
    MOON_RADIUS, EARTH_ORBIT_COLOR, MOON_ORBIT_COLOR, EARTH_TEXTURE_FILE, MOON_TEXTURE_FILE, BACKGROUND_TEXTURE_FILE, \
    EARTH_ROTATION_SPEED, MOON_ROTATION_SPEED
from gezeiten.animations.astronomical_object import AstronomicalObject


class Scene:
    observer_position = list(DEFAULT_OBSERVER_POSITION)
    observer_turn = list(DEFAULT_OBSERVER_TURN)
    x_length_center, y_length_center, z_length_center = DEFAULT_LENGTH_TO_CENTER
    x_angle, y_angle = DEFAULT_ANGLE

    x_rotation, y_rotation, z_rotation = DEFAULT_OBSERVER_ROTATION
    quadratic = gluNewQuadric()
    background = Background()

    def __init__(self, earth_moon_problem):
        """
        Initializes the intergalactic scenery with earth and moon as a couple moving in front of the Milky Way.

        :param earth_moon_problem: Already solved differential equation object
        """
        self._calculate_lengths_to_center()
        self._initialize_astronomical_objects(earth_moon_problem)
        self._load_textures()
        self._initialize_opengl()

    @staticmethod
    def resize(width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)

    def draw(self, point_iterator):
        self._update_perspective()
        self._prepare_opengl()
        self._draw_scene(point_iterator)

    def _calculate_lengths_to_center(self):
        self.x_length_center = np.sin(self.y_angle)
        self.y_length_center = np.sin(self.x_angle)
        self.z_length_center = -np.cos(self.x_angle)

    def _initialize_astronomical_objects(self, earth_moon_problem):
        x_scale, y_scale = self._calculate_scale(earth_moon_problem)
        self.earth = AstronomicalObject(
            EARTH_RADIUS,
            x_scale * earth_moon_problem.solution["x_E"],
            y_scale * earth_moon_problem.solution["y_E"],
            EARTH_ORBIT_COLOR
        )
        self.moon = AstronomicalObject(
            MOON_RADIUS,
            x_scale * earth_moon_problem.solution["x_M"],
            y_scale * earth_moon_problem.solution["y_M"],
            MOON_ORBIT_COLOR
        )

    @staticmethod
    def _calculate_scale(earth_moon_problem):
        x_scale = 5 / max(earth_moon_problem.solution["x_M"])
        y_scale = 5 / max(earth_moon_problem.solution["y_M"])
        return x_scale, y_scale

    def _load_textures(self):
        self.earth.load_texture(EARTH_TEXTURE_FILE)
        self.moon.load_texture(MOON_TEXTURE_FILE)
        self.background.load_texture(BACKGROUND_TEXTURE_FILE)

    def _initialize_opengl(self):
        gluQuadricNormals(self.quadratic, GLU_SMOOTH)
        gluQuadricTexture(self.quadratic, GL_TRUE)
        glEnable(GL_TEXTURE_2D)

        glShadeModel(GL_SMOOTH)
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        self._set_light_conditions()

        glEnable(GL_DEPTH_TEST)

    @staticmethod
    def _set_light_conditions():
        light_ambient = [0.0, 0.0, 0.0, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_position = [1.0, 1.0, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def _update_perspective(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1.0 * WINDOW_SIZE_WIDTH / WINDOW_SIZE_HEIGHT, 0.5, 300.0)
        gluLookAt(self.observer_position[0], self.observer_position[1], self.observer_position[2],
                  self.observer_position[0] + self.x_length_center, self.observer_position[1] + self.y_length_center,
                  self.observer_position[2] + self.z_length_center,
                  self.observer_turn[0], self.observer_turn[1], self.observer_turn[2])

    def _prepare_opengl(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glColor3f(1.0, 0.0, 0.0)

    def _draw_scene(self, point_iterator):
        glPushMatrix()
        self._rotate_observer()
        self._draw_background()
        self._draw_astronomical_objects(point_iterator)
        glPopMatrix()

    def _rotate_observer(self):
        glTranslatef(0.0, 0.0, 0.0)
        glRotatef(self.x_rotation, 1.0, 0.0, 0.0)
        glRotatef(self.y_rotation, 0.0, 1.0, 0.0)
        glRotatef(self.z_rotation, 0.0, 0.0, 1.0)

    def _draw_background(self):
        self.background.draw(self.quadratic)

    def _draw_astronomical_objects(self, point_iterator):
        self._update_earth(point_iterator)
        self._update_moon(point_iterator)

        self.earth.draw(self.quadratic)
        self.moon.draw(self.quadratic)
        self._draw_orbit(self.earth, point_iterator)
        self._draw_orbit(self.moon, point_iterator)

    def _update_earth(self, point_iterator):
        self.earth.update_position(point_iterator)
        self.earth.update_rotation(EARTH_ROTATION_SPEED)

    def _update_moon(self, point_iterator):
        self.moon.update_position(point_iterator)
        self.moon.update_rotation(MOON_ROTATION_SPEED)

    @staticmethod
    def _draw_orbit(astronomical_object, point_iterator):
        astronomical_object.update_orbit_points(point_iterator)
        astronomical_object.draw_orbit()
