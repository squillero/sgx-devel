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

from collections import abc
from typing import Callable, Any, Optional, Type, Union

from sgx.genotype import Genotype
from sgx.fitness.base import Fitness
from sgx.fitness.simple import Scalar


class FitnessFunction(abc.Callable):
    def __init__(self,
                 fitness_function: Callable[[Genotype], Any],
                 type_: Optional[Type[Fitness]] = Type[Scalar],
                 best_fitness: Optional[Fitness] = None,
                 cook: Optional[Callable[[Genotype], Any]] = None):
        if cook is not None:
            self._fitness_function = lambda g: fitness_function(cook(g))
        else:
            self._fitness_function = fitness_function
        self._fitness_type = type_
        if best_fitness:
            self._best_fitness = type_(best_fitness)
        else:
            self._best_fitness = None

    def __call__(self, genotype: Genotype) -> Fitness:
        return self._fitness_type(self._fitness_function(genotype))

    @property
    def fitness_type(self):
        return self._fitness_type

    @property
    def best_fitness(self):
        return self._best_fitness
