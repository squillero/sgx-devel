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

import numpy as np
from scipy.optimize import rosen
import seaborn as sns

import sgx
import randy
import matplotlib.pyplot as plt

a = sgx.allele.FloatingPoint(-1, 1, mixture_size=4)

x = np.linspace(a._interval[0], a._interval[1], 100)
y = np.zeros(x.shape)
for f in a._mixture:
    pdf = randy.get_rvs(f.a, f.b, f.loc, f.scale)
    t = pdf(x)
    plt.plot(x, t, ',')
    y += t / len(a._mixture)
plt.plot(x, y, 'k-', lw=2)
plt.show()

SAMPLES = 10_000
r = [a.sample() for _ in range(SAMPLES)]
#plt.hist(r, density=True, histtype='stepfilled', alpha=0.2)
sns.histplot(r, bins=50)
plt.show()

