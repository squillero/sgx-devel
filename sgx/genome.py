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

__all__ = ['Genome']

from base import Pedantic, Paranoid
from genotype import Genotype
from sgx.allele.base import Allele


class Genome(list, Pedantic, Paranoid):
    """A tuple of Alleles, each one specifying a set of alternative genes."""

    def __init__(self, *args):
        super().__init__(*args)
        assert self.run_paranoia_checks()
        self._is_squeezable = all(a.is_squeezable for a in list(self))

    def __repr__(self):
        return object.__repr__(self)

    @property
    def is_squeezable(self):
        return self._is_squeezable

    def run_paranoia_checks(self) -> bool:
        for i, a in enumerate(self):
            assert isinstance(a, Allele), f"Locus[{i}] is not {Allele} but {type(a)}"
        return super().run_paranoia_checks()

    def is_valid(self, genotype: Genotype) -> bool:
        if any(not a.is_valid(g) for a, g in zip(list(self), genotype)):
            return False
        return super().is_valid(genotype)

    def format_genotype(self, genotype: Genotype) -> str:
        if self._is_squeezable:
            return genotype.squeeze()
        else:
            return str(genotype)
