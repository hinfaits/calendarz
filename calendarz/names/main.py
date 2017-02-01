"""
This entire module is essentially a mirror of this repo
https://github.com/concentricsky/python-randomnames
"""

from nouns import NOUNS
from adjectives import ADJECTIVES

import random


def random_adjective():
    """
    695 available adjectives
    """
    return random.choice(ADJECTIVES)


def random_noun():
    """
    267 available nouns
    """
    return random.choice(NOUNS)


def random_pair(digits=None):
    """
    Generates a random adjective noun pair with optional numeric
    digits seperated with hyphens
    """
    ret = "-".join((random_adjective(), random_noun(),))
    if digits:
        n = random.randint(10**(digits-1), (10**digits)-1)
        ret = "-".join((ret, str(n),))
    return ret
