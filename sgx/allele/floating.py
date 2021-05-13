# -*- coding: utf-8 -*-
#############################################################################
#   _________ ____________  ___                                             #
#  /   _____//  _____/\   \/  /  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  #
#  \_____  \/   \  ___ \     /   THE E(X)TENDED (S)ELFISH (G)ENE ALGORITHM  #
#  /        \    \_\  \/     \   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  #
# /_________/\________/___/\  \  https://github.com/squillero/sgx           #
#                           \_/                                             #
#                                                                           #
# A quick 'n dirty versatile population-less evolutionary optimizer loosely #
# inspired by a cool interpretation of the Darwinian theory.                #
#                                                                           #
#############################################################################

# Copyright 2021 Giovanni Squillero
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Sequence, Hashable, Union, Dict, Tuple, List
from math import isclose

import numpy as np

from sgx import randy

from sgx.utils import logging
from sgx.allele.base import Allele


class UnitDistribution:
    a: float
    b: float
    loc: float
    scale: float

    def __init__(self, a, b, loc, scale) -> None:
        self.a, self.b = a, b
        self.loc, self.scale = loc, scale

    def sample(self) -> float:
        return randy.scale_random(self.a, self.b, loc=self.loc, scale=self.scale)


class FloatingPoint(Allele):

    DEFAULT_MIXTURE_SIZE = 10
    DEFAULT_SCALE = .5

    _mixture: List[UnitDistribution]
    _learning_rate: float
    _interval: Tuple[float, float]

    def __init__(self, a: float, b: float, mixture_size: int = DEFAULT_MIXTURE_SIZE, learning_rate: float = Allele.DEFAULT_LEARNING_RATE):
        assert a < b, f"Illegal interval [{a}, {b}]"
        assert mixture_size > 0, f"Mixture size must be poitive (found {mixture_size})"
        assert 0 < learning_rate < 1, f"Learning rate must be ]0, 1[ (found {learning_rate})"
        self._interval = (a, b)
        self._learning_rate = learning_rate
        if mixture_size == 1:
            self._mixture = [UnitDistribution(a, b, loc=(a+b)/2, scale=FloatingPoint.DEFAULT_SCALE)]
        else:
            self._mixture = list()
            step = (b-a)/(mixture_size-1)
            for m in range(mixture_size):
                self._mixture.append(UnitDistribution(a, b, loc=a+step*m, scale=FloatingPoint.DEFAULT_SCALE))

    def sample(self, sample_type: Optional[str] = Allele.DEFAULT_SAMPLE_TYPE) -> Hashable:
        if sample_type == Allele.SAMPLE_TYPE__SAMPLE:
            dist = randy.choice(self._mixture)
            return dist.sample()
        elif sample_type == Allele.SAMPLE_TYPE__UNIFORM:
            return randy.random(self._interval[0], self._interval[1])
        elif sample_type == Allele.SAMPLE_TYPE__MODE:
            assert NotImplementedError
            return None
        else:
            assert sample_type in Allele.VALID_SAMPLE_TYPES, f"Unknown sample type: {sample_type!r} vs. {Allele.VALID_SAMPLE_TYPES}"

    def update(self, winner: Hashable, loser: Hashable) -> None:
        loc = np.array([m.loc for m in self._mixture])
        loser_index = np.argmin(abs(loc - loser))
        self._mixture[loser_index].loc = winner
        assert self.run_paranoia_checks()

    def describe(self) -> str:
        return f'[{self._interval[0]},{self._interval[1]}]/{len(self._mixture)}'

    def is_valid(self, value: Hashable) -> bool:
        return self._interval[0] <= value <= self._interval[1];

    def run_paranoia_checks(self) -> bool:
        return super().run_paranoia_checks()
