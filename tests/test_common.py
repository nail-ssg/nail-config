import pytest
import sys
from copy import deepcopy as copy
sys.path += ['./nail_config']
from common import *

a = {
    'a': 1, 'b': 'c', 'd': None,
    'e': {
        'x': {'y': 'z'}
    }
}
et1 = copy(a)
b1 = {'a': 2}
et2 = copy(et1)
et2['a'] = 2
b3 = {'-b': None}
et3 = copy(et1)
del et3['b']
b4 = {'e': {'x': None}}
et4 = copy(et1)
et4['e']['x'] = None
b5 = b4
et5 = et1


def test_glue_1():
    rslt = dict_glue(a, b1)
    assert rslt == et1


def test_glue_2():
    rslt = dict_glue(a, b1, nochange=False)
    assert rslt == et2
    assert a == et1


def test_glue_3():
    rslt = dict_glue(a, b3)
    assert rslt == et3


def test_glue_4():
    rslt = dict_glue(a, b4, False)
    assert rslt == et4


def test_glue_5():
    rslt = dict_glue(a, b5)
    assert rslt == et5


def test_add_1():
    rslt = {'a': '1'}
    assert add_to_dict(rslt, 'b/c/d', 2)
    assert rslt == {'a': '1', 'b': {'c': {'d': 2}}}


def test_add_2():
    rslt = {'a': '1'}
    assert not add_to_dict(rslt, 'a/c/d', 2)
    assert rslt == {'a': '1'}


def test_add_3():
    rslt = {'a': {}}
    assert add_to_dict(rslt, 'a/c/d', 2)
    assert rslt == {'a': {'c': {'d': 2}}}


def test_add_4():
    rslt = {'a': None}
    assert add_to_dict(rslt, 'a/c/d', 2)
    assert rslt == {'a': {'c': {'d': 2}}}
