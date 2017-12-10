#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :PID.py
# description     :python pid controller
# author          :Caner Durmusoglu
# date            :20151218
# version         :0.1
# notes           :
# python_version  :2.7
# ==============================================================================

"""Ivmech PID Controller - простая реализация контроллера пропорционального интеграла-производного (PID) на языке программирования Python.
Дополнительная информация о PID-контроллере: http://en.wikipedia.org/wiki/PID_controller
"""
import time

class PID:
    """PID Controller
    """

    def __init__(self, P=0.2, I=0.0, D=0.0):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Очищает вычисления и коэффициенты PID"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value):
        """Вычисляет значение PID для заданной эталонной обратной связи

        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}

           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        """
        error = self.SetPoint - feedback_value

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Помните последнюю и последнюю ошибку для следующего расчета
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        """Определяет, насколько агрессивно PID реагирует на текущую ошибку с установкой пропорционального усиления"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Определяет, насколько агрессивно PID реагирует на текущую ошибку с установкой Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Определяет, насколько агрессивно PID реагирует на текущую ошибку с установкой Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Интегральная ветровая линия, также известная как ветвление интегратора или сброс, 
        ссылается на ситуацию в контроллере обратной связи с ПИД-регулятором, где происходит значительное 
        изменение заданного значения (скажем, положительное изменение), а интегральные члены накапливают 
        значительную ошибку во время подъема (выключения), таким образом, превышение и продолжает увеличиваться 
        по мере того, как эта накопленная ошибка разматывается (компенсируется ошибками в другом направлении).
        Конкретной проблемой является избыточное превышение.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID, который должен обновляться с регулярным интервалом. Основываясь на заранее определенном времени времени,
        ПИД-регулятор решает, должен ли он немедленно вычислить или вернуть.
        """
        self.sample_time = sample_time
