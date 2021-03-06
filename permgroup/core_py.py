#!/usr/bin/python

__author__ = "Jason B. Hill (jason@jasonbhill.com)"
__copyright__ = "Copyright 2016, Jason B. Hill"
__license__ = "GPLv3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)"
__version__ = "0.1.0"
__notes__ = """
Provides the underlying Python code to turn lists of tuples into permutations.

methods:

    _verify_tuples_ - verifies that an action is a list of tuples of positive integers.

    _has_unique_points_ - verifies that not point is repeated in an action.

    _get_max_support_ - returns the maximum integer in the support of an action.

    _get_degree_ - returns the number of points in the support of an action.

    _is_identity_action - returns True if the action is trivial.

    _make_map_ - forms a Python list representing the action.
"""


def _verify_tuples_(action):
    """
    Verifies that `action` is a list of tuples of positive integers.

    INPUT:
        action (list) - a list of tuples of positive integers

    OUTPUT:
        True or False - True when `action` is a list of tuples of positive integers.

    EXAMPLE/TESTS:
    >>> P = [(1,2,3),(4,5)]
    >>> _verify_tuples_(P)
    True
    >>> P = [(0,1),(2,3)]
    >>> _verify_tuples_(P)
    False
    >>> P = [('a',1)]
    >>> _verify_tuples_(P)
    False
    >>> P = [()]
    >>> _verify_tuples_(P)
    True
    >>> P = []
    >>> _verify_tuples_(P)
    False
    """
    if not isinstance(action, list):
        return False
    if len(action) == 0:
        return False
    if not all(isinstance(t, tuple) for t in action):
        return False
    for t in action:
        if not all(isinstance(pnt, (int,long)) and pnt > 0 for pnt in t):
            return False
    return True


def _has_unique_points_(action):
    """
    Verifies that no point is repeated in a list of tuples of positive integers.

    INPUT:
        action (list) - a (verified) list of tuples of positive integers

    OUTPUT:
        True or False - True exactly when no integer is repeated.

    EXAMPLES/TESTS:
    >>> P = [(1,2),(3,4)]
    >>> _has_unique_points_(P)
    True
    >>> P = [(1,2,3),(3,4)]
    >>> _has_unique_points_(P)
    False
    >>> P = [()]
    >>> _has_unique_points_(P)
    True
    """
    S = set()
    for t in action:
        for pnt in t:
            if pnt in S:
                return False
            else:
                S.add(pnt)
    return True


def _get_max_support_(action):
    """
    Returns the maximum integer in the support of `action`.

    A returned value of 0 indicates `action` is the identity action.

    INPUT:
        action (list) - a (verified) list of tuples of positve integers

    OUTPUT:
        int or long - the maximum value in the support of `action`

    EXAMPLES/TESTS:
    >>> P = [(1,2,3),(4,5)]
    >>> _get_max_support_(P)
    5
    >>> P = [()]
    >>> _get_max_support_(P)
    0
    """
    m = 0
    for t in action:
        for pnt in t:
            if pnt > m:
                m = pnt
    return m


def _get_degree_(action):
    """
    From a (verified) action, find the degree.

    The degree of a permutation is the size of the support of the action.

    INPUT:
        action (list) - a (verified) list of tuples of positive integers.

    OUTPUT:
        int - an integer representing the size of the support of the action.

    EXAMPLES/TESTS:
    >>> P = [(1,2)]
    >>> _get_degree_(P)
    2
    >>> P = [(1,8)]
    >>> _get_degree_(P)
    2
    >>> P = [(1,5),(4,7)]
    >>> _get_degree_(P)
    4
    >>> P = [()]
    >>> _get_degree_(P)
    0
    """
    degree = 0
    for t in action:
        for pnt in t:
            degree += 1
    return degree


def _is_identity_action_(action):
    """
    Determines if `action` represents the identity permutation.

    INPUT:
        action (list) - a (verified) list of tuples of positive integers

    OUTPUT:
        True or False - True exactly when `action` represents the identity permutation.

    EXAMPLES/TESTS:
    >>> P = [(1,2,3),(4,5)]
    >>> _is_identity_action_(P)
    False
    >>> P = [()]
    >>> _is_identity_action_(P)
    True
    >>> P = [(),()]
    >>> _is_identity_action_(P)
    True
    """
    if _get_max_support_(action) == 0:
        return True
    else:
        return False


def _make_map_(action):
    """
    From a (verified) action, construct a map array.

    INPUT:
        action (list) - a (verified) list of tuples of positive integers.

    OUTPUT:
        list - a list `L` where `L[index]` gives the action on `index` and `L[0]` is the max integer
            in the support of the action.

    EXAMPLES/TESTS:
    >>> P = [(1,2,3,6)]
    >>> _make_map_(P)
    [6, 2, 3, 6, 4, 5, 1]
    >>> P = [(1,2),(3,4)]
    >>> _make_map_(P)
    [4, 2, 1, 4, 3]
    >>> P = [()]
    >>> _make_map_(P)
    [0]
    """
    # In the case of the identity action, return immediately
    if _is_identity_action_(action):
        return [0]
    # Otherwise, compute the map
    max_support = _get_max_support_(action)
    L = range(max_support + 1)
    L[0] = max_support
    for t in action:
        for i in range(len(t)):
            L[t[i]] = t[(i + 1) % len(t)]
    return L
