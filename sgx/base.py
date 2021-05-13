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

__all__ = ['Pedantic', 'Paranoid']

from typing import Any
from abc import ABC, abstractmethod


class Paranoid():
    """Abstract class: Paranoid classes do implement `run_paranoia_checks()`."""

    def run_paranoia_checks(self) -> bool:
        """Check the internal consistency of a "paranoid" object.

        The function should be overridden by the sub-classes to implement the
        required, specific checks. It always returns `True`, but throws an
        exception whenever an inconsistency is detected.

        **Notez bien**: Sanity checks may be computationally intensive,
        paranoia checks are not supposed to be used in production environments
        (i.e., when `-O` is used for compiling). Their typical usage is:
        `assert foo.run_paranoia_checks()`

        Returns:
            True (always)

        Raise:
            AssertionError if some internal data structure is incoherent
        """
        return True


class Pedantic(ABC):
    """Abstract class: Pedantic classes do implement `is_valid()`."""

    @abstractmethod
    def is_valid(self, obj: Any) -> bool:
        """Check an object against a specification.

        The function may be used to check a value against a parameter definition, a node against a section definition).

        Returns:
            True if the object is valid, False otherwise
        """
        raise NotImplementedError("Abstract method not implemented")
