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

from typing import Tuple, Sequence, Any, Callable, Optional, Hashable, Union

from sgx import randy

from utils import logging
from fitness import FitnessFunction
from genome import Genome
from genotype import Genotype
from allele.base import Allele
from fitness.base import Fitness


class Species:
    """Missing"""

    _genome: Genome
    _fitness_function: FitnessFunction
    _uncertain_evaluation: bool

    def __init__(self,
                 genome: Sequence[Any],
                 fitness_function: FitnessFunction,
                 mutation_rate: Optional[float] = None,
                 uncertain_evaluation: Optional[bool] = False) -> None:

        self._genome = Genome(genome)
        self._fitness_function = fitness_function
        self._uncertain_evaluation = uncertain_evaluation

        if mutation_rate is None:
            self._mutation_rate = 1 / len(self._genome)

    @property
    def genome(self) -> Genome:
        return self._genome

    @property
    def fitness_function(self) -> FitnessFunction:
        return self._fitness_function

    def sample(self, sample_type: Optional[str] = Allele.DEFAULT_SAMPLE_TYPE) -> Genotype:
        genotype = list()
        for a in self._genome:
            if randy.boolean(p_true=self._mutation_rate):
                genotype.append(a.sample(sample_type='uniform'))
            else:
                genotype.append(a.sample(sample_type='sample'))
        return Genotype(genotype)

    def update(self, winner: Genotype, loser: Genotype):
        for a, w, l in zip(self._genome, winner, loser):
            a.update(winner=w, loser=l)

    def evaluate(self, genotype: Genotype) -> Fitness:
        return self._fitness_function(genotype)

    def _simple_compare(self, first: Genotype, second: Genotype) -> int:
        # TODO: Add Caching
        f1 = self._fitness_function(first)
        f2 = self._fitness_function(second)
        if f1 > f1:
            return 1
        elif f2 > f1:
            return -1
        else:
            return 0

    def _stochastic_compare(self, first: Genotype, second: Genotype) -> int:
        f1 = self._fitness_function(first)
        f2 = self._fitness_function(second)
        if f1 > f1:
            return 1
        elif f2 > f1:
            return -1
        else:
            return 0

    def compare(self, first: Genotype, second: Genotype) -> int:
        if not self._uncertain_evaluation:
            return self._simple_compare(first, second)
        else:
            return self._stochastic_compare(first, second)
