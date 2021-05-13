# -*- coding: utf-8 -*-
# ______________   ______   __
# |____/|____|| \  ||   \\_/
# |R  \_|A   ||N \_||D__/ |Y
#
#    @..@    古池や
#   (----)    蛙飛び込む
#  ( >__< )    水の音
#
# ( ! ) 2021 Giovanni Squillero. Public Domain.
# Project page: https://github.com/squillero/randy

import math
import warnings
from typing import Optional, Sequence, List, Any

import numpy as np
from scipy.stats import truncnorm


class Randy:
    """Safe, reproducible random numbers for EA applications."""

    SMALL_NUMBER = 1e-9

    __slots__ = ['_generator', '_calls']

    def __getstate__(self):
        return self._generator, self._calls

    def __setstate__(self, state):
        _generator, _calls = state

    def __init__(self, seed: Optional[Any] = 42, croak: Optional[bool] = True) -> None:
        if seed is None and croak:
            warnings.warn("Initializing Randy with entropy from the OS: results will not be reproducible.",
                          RuntimeWarning,
                          stacklevel=2)
        self._generator = np.random.default_rng(seed)
        self._calls = 0

    def __str__(self) -> str:
        description = ', '.join(f"{a}={b!r}" for a, b in self._generator.__getstate__().items())
        return f"Randy @ {hex(id(self))} (calls={self._calls}, {description})"

    def __repr__(self) -> str:
        return f"Randy_{hex(id(self))[2:]}"

    def __bool__(self):
        return self.boolean()

    @staticmethod
    def _strength_to_sigma(strength: float) -> Optional[float]:
        """Stretches [0,1] on a standard deviation ]0, 20.8[."""
        if strength is None:
            return None
        assert 0 <= strength <= 1, "Invalid sigma (must be [0, 1])"
        x = strength / 2 + .5
        x = min(x, 1 - Randy.SMALL_NUMBER)
        val = math.log(x / (1 - x))
        if math.isclose(val, 0):
            val = Randy.SMALL_NUMBER
        return val

    def sigma_random(self, a: float, b: float, loc: Optional[float] = None, strength: Optional[float] = None) -> float:
        """Returns a value in [a, b] by perturbing loc with a given strength."""
        return self.scale_random(a, b, loc=loc, scale=Randy._strength_to_sigma(strength))

    def scale_random(self, a: float, b: float, loc: Optional[float] = None, scale: Optional[float] = None) -> float:
        """Returns a value from a standard normal truncated to [a, b] with mean loc and standard deviation scale."""
        self._calls += 1
        assert a <= b, "a must precede b"
        assert scale is None or 0 <= scale <= 1, "strength must be in [0, 1]"
        assert (loc is None and scale is None) or (
                loc is not None and
                scale is not None), "loc and strength should be specified together (either both or neither)"
        assert loc is None or a <= loc <= b, "loc must be in [a, b]"
        if scale is None:
            val = self._generator.random()
            val = val * (b - a) + a
        elif scale == 0:
            val = loc
        else:
            clip_a, clip_b = (a - loc) / scale, (b - loc) / scale
            val = truncnorm.rvs(clip_a, clip_b, loc=loc, scale=scale, random_state=self._generator)
        return val

    def random(self, a: Optional[float] = 0, b: Optional[float] = 1) -> float:
        """Returns a random value in [a, b], default is [0, 1]."""
        return self.sigma_random(a=a, b=b, loc=None, strength=None)

    def sigma_choice(self, seq: Sequence[Any], loc: Optional[int] = None, strength: Optional[float] = None) -> Any:
        """Returns a random element from seq by perturbing index loc with a given strength."""
        self._calls += 1
        assert strength is None or 0 <= strength <= 1, "strength must be in [0, 1]"
        assert (loc is None and strength is None) or (
            loc is not None and
            strength is not None), "loc and strength should be specified together (either both or neither)"
        assert loc is None or 0 <= loc < len(seq), "loc must be a valid index of seq"
        if strength == 1 or strength is None:
            return self._generator.choice(seq)
        elif strength == 0:
            return seq[loc]
        else:
            i = self.sigma_random(0, len(seq) - Randy.SMALL_NUMBER, loc=loc + .5, strength=strength)
            return seq[int(i)]

    def weighted_choice(self, seq: Sequence[Any], p: Sequence[float]) -> Any:
        """Returns a random element from seq using the probabilities in p."""
        assert len(seq) == len(p), "seq and weight must contain the same number of elements"
        assert math.isclose(sum(p), 1), "weights must sum to 1"
        r = self._generator.random()
        return next(val for val, cp in ((v, sum(p[0:i + 1])) for i, v in enumerate(seq)) if cp >= r)

    def choice(self,
               seq: Sequence[Any],
               loc: Optional[int] = None,
               strength: Optional[float] = None,
               p: Optional[Sequence[float]] = None) -> Any:
        """Returns a random element from seq, either using weighted_ or sigma_choice."""
        if loc is not None and strength is not None:
            assert p is None, "p cannot be specified with loc and strength"
            return self.sigma_choice(seq, loc=loc, strength=strength)
        elif p is not None:
            assert loc is None and strength is None, "loc and strength cannot be specified with p"
            return self.weighted_choice(seq, p)
        else:
            assert loc is None and strength is None, "loc and strength should be specified together (either both or neither)"
            return self._generator.choice(seq)

    def boolean(self, p_true: Optional[float] = None, p_false: Optional[float] = None) -> bool:
        """Returns a boolean value with the given probability."""
        self._calls += 1
        assert p_true is None or 0 <= p_true <= 1, "p_true must be on [0, 1]"
        assert p_false is None or 0 <= p_false <= 1, "p_false must be on [0, 1]"
        assert p_true is None or p_false is None or math.isclose(p_true + p_false,
                                                                 1), "p_true + p_false must be equal to 1"
        if p_true is None and p_false is None:
            p_true = .5
        elif p_true is None and p_false is not None:
            p_true = 1 - p_false
        return self._generator.random() < p_true

    def randint(self, a, b) -> int:
        """Returns a random integer in [a, b]."""
        assert a <= b, "a must be <= b."
        r = self._generator.random() * (b - a + 1) + a
        return int(r)

    def shuffle(self, seq: List[Any]) -> None:
        """Shuffle list x in place, and return None."""
        self._generator.shuffle(seq)

    def shuffled(self, seq: Sequence[Any]) -> List[Any]:
        """Returns a shuffled list with the element of seq."""
        y = list(seq)
        self.shuffle(y)
        return y
