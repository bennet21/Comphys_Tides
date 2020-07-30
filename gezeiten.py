#!/usr/bin/env python3
# Copyright (c) 2020 Bennet Weiss
# Copyright (c) 2020 Nico Alt
# SPDX-License-Identifier: AGPL-3.0-only
# License-Filename: LICENSE.md
from gezeiten.exercises.exercise_2_1_b import plot_2_1_b_solve_ivp, plot_2_1_b_runge_kutta, plot_2_1_b_euler
from gezeiten.exercises.exercise_2_1_c import plot_2_1_c_solve_ivp
from gezeiten.exercises.exercise_2_2_c import plot_2_2_c_solve_ivp, animate_2_2_c_solve_ivp
from gezeiten.exercises.exercise_2_3_b import plot_2_3_b_solve_ivp, animate_2_3_b_solve_ivp
from gezeiten.exercises.exercise_2_3_c import fit_2_3_c_solve_ivp
from gezeiten.exercises.exerise_3_2 import plot_3_2_solve_ivp, animate_3_2_solve_ivp


def start():
    plot_2_1_b_solve_ivp()
    plot_2_1_b_runge_kutta()
    plot_2_1_b_euler()
    plot_2_1_c_solve_ivp()
    plot_2_2_c_solve_ivp()
    animate_2_2_c_solve_ivp()
    plot_2_3_b_solve_ivp()
    animate_2_3_b_solve_ivp()
    fit_2_3_c_solve_ivp()
    plot_3_2_solve_ivp()
    animate_3_2_solve_ivp()


start()
