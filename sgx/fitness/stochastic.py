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

from typing import Sequence, Any, Type
from math import isclose

from sgx.utils import logging
from numbers import Number
from sgx.fitness.base import Fitness


class Vector(Fitness):
    """A generic vector of Fitness values.

    fitness_type is the subtype, **kwargs are passed to fitness init

    Examples:
        f1 = sgx.fitness.Vector([23, 10], fitness_type=Approximate, abs_tol=.1)
        f2 = sgx.fitness.Vector([23, 10], fitness_type=Approximate, abs_tol=.001)

        f1 > sgx.fitness.Vector([23, 9.99], fitness_type=Approximate, abs_tol=.1) is False
        f2 > sgx.fitness.Vector([23, 9.99], fitness_type=Approximate, abs_tol=.001) is True

    """

    def __init__(self, value: Sequence, fitness_type: Type[Fitness] = Scalar, **kwargs):
        self._values = tuple(fitness_type(e, **kwargs) for e in value)
        self.run_paranoia_checks()

    def is_distinguishable(self, other: 'Vector') -> bool:
        self.check_comparable(other)
        return any(e1 != e2 for e1, e2 in zip(self._values, other._values))

    def is_fitter(self, other: 'Fitness') -> bool:
        self.check_comparable(other)
        return Vector.compare_vectors(self._values, other._values) > 0

    @staticmethod
    def compare_vectors(v1: Sequence[Fitness], v2: Sequence[Fitness]) -> int:
        """Compare Fitness values in v1 and v2.

        Return -1 if v1 < v2; +1 if v1 > v2; 0 if v1 == v2"""
        for e1, e2 in zip(v1, v2):
            if e1 > e2:
                return 1
            elif e2 > e1:
                return -1
        return 0

    def decorate(self) -> str:
        return ', '.join(e.decorate() for e in self._values)

    def check_comparable(self, other: 'Vector'):
        super().check_comparable(other)
        assert len(self._values) == len(
            other._values), f"Can't is_fitter Fitness Vectors of different size ({self} vs. {other})"

    def __iter__(self):
        return iter(self._values)

    def __hash__(self):
        return hash(self._values)
