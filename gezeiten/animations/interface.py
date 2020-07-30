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
import pygame
from pygame.constants import K_SPACE, K_q, K_w, K_e, K_r, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_a, K_s

from gezeiten.animations.constants import WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT, DEFAULT_OBSERVER_POSITION
from gezeiten.animations.scene import Scene

ROTATE_FRACTION = 0.2
TURN_FRACTION = 0.005
ZOOM_FRACTION = 0.1


def input_key(scene_obj):
    pressed_keys = pygame.key.get_pressed()
    _normalize_angels(scene_obj)
    _react_on_key_events(pressed_keys, scene_obj)
    scene_obj.resize(WINDOW_SIZE_WIDTH, WINDOW_SIZE_HEIGHT)


def _react_on_key_events(pressed_keys, scene_obj):
    _reset_view(pressed_keys, scene_obj)
    _rotate_positive_x(pressed_keys, scene_obj)
    _rotate_negative_x(pressed_keys, scene_obj)
    _rotate_positive_y(pressed_keys, scene_obj)
    _rotate_negative_y(pressed_keys, scene_obj)
    _turn_up(pressed_keys, scene_obj)
    _turn_down(pressed_keys, scene_obj)
    _turn_left(pressed_keys, scene_obj)
    _turn_right(pressed_keys, scene_obj)
    _zoom_in(pressed_keys, scene_obj)
    _zoom_out(pressed_keys, scene_obj)


def _normalize_angels(scene_obj):
    if np.rad2deg(scene_obj.x_angle) > 90.0:
        scene_obj.x_angle = np.deg2rad(90)
    if np.rad2deg(scene_obj.x_angle) < -90.0:
        scene_obj.x_angle = np.deg2rad(-90)
    if np.rad2deg(scene_obj.y_angle) >= 360.0:
        scene_obj.y_angle = 0.0
    if np.rad2deg(scene_obj.y_angle) <= -360.0:
        scene_obj.y_angle = 0.0


def _reset_view(pressed_keys, scene_obj):
    if pressed_keys[K_SPACE]:
        _reset_angle(scene_obj)
        _reset_rotation(scene_obj)
        _reset_zoom(scene_obj)


def _reset_angle(scene_obj):
    scene_obj.x_angle = 0.0
    scene_obj.y_angle = 0.0
    scene_obj.x_length_center = np.sin(scene_obj.y_angle)
    scene_obj.y_length_center = np.sin(scene_obj.x_angle)
    scene_obj.z_length_center = -np.cos(scene_obj.x_angle)


def _reset_rotation(scene_obj):
    scene_obj.x_rotation = Scene.x_rotation
    scene_obj.y_rotation = Scene.y_rotation
    scene_obj.z_rotation = Scene.z_rotation


def _reset_zoom(scene_obj):
    scene_obj.observer_position[0] = DEFAULT_OBSERVER_POSITION[0]
    scene_obj.observer_position[2] = DEFAULT_OBSERVER_POSITION[2]


def _rotate_positive_x(pressed_keys, scene_obj):
    if pressed_keys[K_e]:
        scene_obj.x_rotation += ROTATE_FRACTION


def _rotate_negative_x(pressed_keys, scene_obj):
    if pressed_keys[K_r]:
        scene_obj.x_rotation -= ROTATE_FRACTION


def _rotate_positive_y(pressed_keys, scene_obj):
    if pressed_keys[K_q]:
        scene_obj.y_rotation += ROTATE_FRACTION


def _rotate_negative_y(pressed_keys, scene_obj):
    if pressed_keys[K_w]:
        scene_obj.y_rotation -= ROTATE_FRACTION


def _turn_up(pressed_keys, scene_obj):
    if pressed_keys[K_UP]:
        scene_obj.x_angle += TURN_FRACTION
        scene_obj.y_length_center = np.sin(scene_obj.x_angle)
        scene_obj.z_length_center = -np.cos(scene_obj.x_angle)


def _turn_down(pressed_keys, scene_obj):
    if pressed_keys[K_DOWN]:
        scene_obj.x_angle -= TURN_FRACTION
        scene_obj.y_length_center = np.sin(scene_obj.x_angle)
        scene_obj.z_length_center = -np.cos(scene_obj.x_angle)


def _turn_left(pressed_keys, scene_obj):
    if pressed_keys[K_LEFT]:
        scene_obj.y_angle -= TURN_FRACTION
        scene_obj.x_length_center = np.sin(scene_obj.y_angle)
        scene_obj.z_length_center = -np.cos(scene_obj.y_angle)


def _turn_right(pressed_keys, scene_obj):
    if pressed_keys[K_RIGHT]:
        scene_obj.y_angle += TURN_FRACTION
        scene_obj.x_length_center = np.sin(scene_obj.y_angle)
        scene_obj.z_length_center = -np.cos(scene_obj.y_angle)


def _zoom_in(pressed_keys, scene_obj):
    if pressed_keys[K_a]:
        scene_obj.observer_position[0] += scene_obj.x_length_center * ZOOM_FRACTION
        scene_obj.observer_position[2] += scene_obj.z_length_center * ZOOM_FRACTION


def _zoom_out(pressed_keys, scene_obj):
    if pressed_keys[K_s]:
        scene_obj.observer_position[0] -= scene_obj.x_length_center * ZOOM_FRACTION
        scene_obj.observer_position[2] -= scene_obj.z_length_center * ZOOM_FRACTION
