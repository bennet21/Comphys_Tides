# Copyright (c) 2016-2019 elbanic <elbanic12@naver.com>
# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
#
# Original source code at:
# https://github.com/elbanic/SolarSystem
#

import pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE

from gezeiten.animations.constants import WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT, VIDEO_FLAGS, DEFAULT_WINDOW_TITLE
from gezeiten.animations.interface import input_key
from gezeiten.animations.scene import Scene


class ThreeDimensionsAnimation:

    def __init__(self, earth_moon_problem, title=DEFAULT_WINDOW_TITLE):
        """
        3D animation of earth-moon problem with pygame and OpenGL

        :param earth_moon_problem: Already solved differential equation object
        """
        self.earth_moon_problem = earth_moon_problem
        self.title = title
        self.rendered_frames = 0

    def render(self):
        """
        Renders the earth-moon problem with pygame and OpenGL and prints fps at the end
        """
        self._initialize_pygame()

        time_animation_started = self._get_time_since_start()
        self._start_rendering()
        self._show_fps(time_animation_started)

    def _initialize_pygame(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT), VIDEO_FLAGS)
        pygame.display.set_caption(self.title)

    @staticmethod
    def _get_time_since_start():
        return pygame.time.get_ticks()

    def _start_rendering(self):
        scene = Scene(self.earth_moon_problem)
        points_amount = self._get_points_amount()
        point_iterator = -1
        running = True
        while running:
            point_iterator = self._increment_checked_iterator(point_iterator, points_amount)
            running = self._react_on_event(running, scene)
            scene.draw(point_iterator)
            self._render_update()
            self.rendered_frames += 1

    def _get_points_amount(self):
        return len(self.earth_moon_problem.solution["x_E"])

    @staticmethod
    def _increment_checked_iterator(point_iterator, points_amount):
        point_iterator += 1
        if point_iterator >= points_amount - 1:
            point_iterator = 0
        return point_iterator

    @staticmethod
    def _react_on_event(running, scene):
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
        else:
            input_key(scene)
        return running

    @staticmethod
    def _render_update():
        pygame.display.flip()

    def _show_fps(self, time_animation_started):
        fps = self._calculate_fps(time_animation_started)
        print(f"fps:  {fps}")

    def _calculate_fps(self, time_animation_started):
        fps = (self.rendered_frames * 1000) / (self._get_time_since_start() - time_animation_started)
        return round(fps, 2)
