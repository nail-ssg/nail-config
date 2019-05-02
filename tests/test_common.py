import sys
from copy import deepcopy as copy

sys.path.append('./nail_config')
from nail_config.common import *

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
    result = dict_glue(a, b1)
    assert result == et1


def test_glue_2():
    result = dict_glue(a, b1, nochange=False)
    assert result == et2
    assert a == et1


def test_glue_3():
    result = dict_glue(a, b3)
    assert result == et3


def test_glue_4():
    result = dict_glue(a, b4, False)
    assert result == et4


def test_glue_5():
    result = dict_glue(a, b5)
    assert result == et5


def test_add_1():
    result = {'a': '1'}
    assert add_to_dict(result, 'b/c/d', 2)
    assert result == {'a': '1', 'b': {'c': {'d': 2}}}


def test_add_2():
    result = {'a': '1'}
    assert not add_to_dict(result, 'a/c/d', 2)
    assert result == {'a': '1'}


def test_add_3():
    result = {'a': {}}
    assert add_to_dict(result, 'a/c/d', 2)
    assert result == {'a': {'c': {'d': 2}}}


def test_add_4():
    result = {'a': None}
    assert add_to_dict(result, 'a/c/d', 2)
    assert result == {'a': {'c': {'d': 2}}}
