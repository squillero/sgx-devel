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

__all__ = [
    'get_rvs', 'seed', 'boolean', 'choice', 'randint', 'random', 'shuffle', 'shuffled', 'sigma_choice', 'scale_random', 'sigma_random', 'weighted_choice'
]

import logging
from typing import Optional, Any, Sequence, List, Callable
import numpy as np
from scipy.stats import truncnorm

from sgx.randy.core import Randy

try:
    # Ok, I may admit it's a little bit paranoid...
    _default
    assert False, f"Panic: The default random generator has already be initialized: {_default!r}"
except NameError:
    _default = Randy(None, croak=False)  # None, but w/o warning
    logging.debug(f"Initialized Randy: {_default!r}")


# static utilz

def get_rvs(a: float, b: float, loc: float, scale: float) -> Callable:
    """Return the pdf for a standard normal truncated to [a, b] with mean loc and standard deviation scale"""
    clip_a, clip_b = (a - loc) / scale, (b - loc) / scale
    rv = truncnorm(clip_a, clip_b, loc=loc, scale=scale)
    return rv.pdf


# shortcuts

def seed(new_seed: Optional[Any] = None) -> None:
    """Restart default Randy wih the given seed"""
    global _default
    _default = Randy(new_seed)

def sigma_random(a: float, b: float, loc: Optional[float] = None, strength: Optional[float] = None) -> float:
    """Returns a value in [a, b] by perturbing loc with a given strength."""
    return _default.scale_random(a, b, loc=loc, scale=Randy._strength_to_sigma(strength))


def scale_random(a: float, b: float, loc: Optional[float] = None, scale: Optional[float] = None) -> float:
    """Returns a value from a standard normal truncated to [a, b] with mean loc and standard deviation scale."""
    return _default.scale_random(a, b, loc=loc, scale=scale)


def random(a: Optional[float] = 0, b: Optional[float] = 1) -> float:
    """Returns a random value in [a, b], default is [0, 1]."""
    return _default.random(a, b)


def sigma_choice(seq: Sequence[Any], loc: Optional[int] = None, strength: Optional[float] = None) -> Any:
    """Returns a random element from seq by perturbing index loc with a given strength."""
    return _default.sigma_choice(seq, loc=loc, strength=strength)


def weighted_choice(seq: Sequence[Any], p: Sequence[float]) -> Any:
    """Returns a random element from seq using the probabilities in p."""
    return _default.weighted_choice(seq, p)


def choice(seq: Sequence[Any],
           loc: Optional[int] = None,
           strength: Optional[float] = None,
           p: Optional[Sequence[float]] = None) -> Any:
    """Returns a random element from seq, either using weighted_ or sigma_choice."""
    return _default.choice(seq, loc=loc, strength=strength, p=p)


def boolean(p_true: Optional[float] = None, p_false: Optional[float] = None) -> bool:
    """Returns a boolean value with the given probability."""
    return _default.boolean(p_true=p_true, p_false=p_false)


def randint(a, b) -> int:
    """Returns a random integer in [a, b]."""
    return _default.randint(a, b)


def shuffled(seq: Sequence[Any]) -> List[Any]:
    """Returns a shuffled list with the element of seq."""
    return _default.shuffled(seq)


def shuffle(seq: List[Any]) -> None:
    """Shuffle list x in place, and return None."""
    _default.shuffle(seq)
