import sys
import os
import pytest
from .prints import yprint
sys.path += ['.\\nail_config']
from config import Config


@pytest.fixture(scope='function')
def empty_conf():
    conf = Config()
    return conf
    del conf


def test_set_value(empty_conf):
    old_value = empty_conf.set_option('level1.level2.level3', 'value')
    assert old_value is None
    value = empty_conf.get_option('level1.level2.level3')
    assert value == 'value'
    comment = empty_conf.get_comment('level1.level2.level3')
    assert comment is None
    value2 = empty_conf('level1')
    assert value2 == {'level2': {'level3': 'value'}}
    assert type(value2) == dict


def test_set_value_and_comment(empty_conf):
    # print(empty_conf.as_yamlstr())
    old_value = empty_conf.set_option('level1.level2.level3', 'value', 'comment')
    assert old_value is None
    value = empty_conf.get_option('level1.level2.level3')
    assert value == 'value'
    comment = empty_conf.get_comment('level1.level2.level3')
    assert comment == 'comment'


def test_set_value2(empty_conf):
    # print(empty_conf.as_yamlstr())
    empty_conf.set_option('level1.level2.level3', 'value1')
    old_value = empty_conf.set_option('level1.level2.level3', 'value2')
    assert old_value == 'value1'


def test_set_comment(empty_conf):
    empty_conf.set_option('level1.level2.level3', 'value1', 'comment1')
    empty_conf.set_comment('level1.level2.level3', 'comment2')
    show_conf(empty_conf)
    comment = empty_conf.get_comment('level1.level2.level3')
    assert comment == 'comment2'


def test_set_default_config(empty_conf):
    def_conf1 = {
        'a': 'b',
        'c': {
            'd': 'e'
        }
    }
    def_conf2 = {
        'a': 'bb',
        'f': 'g',
        'c': {
            'd': 'ee',
            'i': 'j'
        }
    }
    result_conf1 = {
        'a': 'b',
        'c': {
            'd': 'e',
            'i': 'j'
        },
        'f': 'g'
    }
    result_conf2 = {
        'a': 'b',
        'c': {
            'd': 'eee',
            'i': 'j'
        },
        'f': 'g'
    }
    empty_conf.add_default_config(def_conf1, None)
    empty_conf.add_default_config(def_conf2, None)
    assert empty_conf() == result_conf1
    empty_conf.set_option('c.d', 'eee')
    assert empty_conf() == result_conf2


def test_set_default_config_with_comments(empty_conf):
    def_conf1 = {
        'a': 'b',
        'c': {
            'd': 'e'
        }
    }
    comments = {
        'a': 'comment1',
        'c.d': 'comment2',
    }
    empty_conf.add_default_config(def_conf1, comments)
    assert empty_conf.get_comment('a') == 'comment1'
    assert empty_conf.get_comment('c.d') == 'comment2'


@pytest.fixture(scope='function')
def two_conf():
    conf1 = Config()
    conf2 = Config()
    return (conf1, conf2)
    del conf


def test_set_value3(two_conf):
    conf1, conf2 = two_conf
    old_value1 = conf1.set_option('level1.level2.level3', 'value1')
    old_value2 = conf2.set_option('level1.level2.level3', 'value2')
    value1 = conf1.get_option('level1.level2.level3')
    assert old_value1 is None
    assert old_value2 is None
    assert value1 == 'value1'


@pytest.fixture()
def conf_with_comments1():
    conf = Config()
    conf.set_option('a', None, 'comment1')
    conf.set_option('b', '', ' comment2')
    conf.set_option('c', 'd', '   comment3')
    conf.set_option('e', 1)
    conf.set_option('f', 2, None)
    # conf.set_option('g', 3, '') - пустые коментарии не допустимы
    # conf.set_option('h', [], 'comment4') - пустые массивы не допустимы
    conf.set_option('i', [4], 'comment5')
    conf.set_option('j', [5, 6], 'comment6')
    conf.set_option('k.l', 'm', ' comment7 # ')
    conf.set_option('k.l', 'n', '  # comment8')
    return conf


def test_separate(conf_with_comments1):
    conf_with_comments1._separate()
    print()
    yprint(conf_with_comments1._comments)
    yprint(conf_with_comments1._config)


@pytest.fixture()
def conf_with_comments2(empty_conf):
    s = """
a: 1 # comment1
b:
  c: 3 # comment2
  d: 1 # comment3
  e: '#' # comment4
c:
- a # comment5
"""
    empty_conf.loads(s)
    return empty_conf


def show_conf(conf):
    print()
    yprint(conf._comments)
    yprint(conf._config)
    print('changed:', conf._changed)


def test_loads(conf_with_comments2):
    show_conf(conf_with_comments2)


def test_load():
    path1 = os.path.abspath('./tests/data/config.yml')
    path2 = os.path.abspath('./tests/data/config1.yml')
    conf = Config()
    assert conf.load(path1) == False
    assert conf.load(path2) == True
    yprint(conf._comments)
    assert conf('a') == 1
    assert conf('b') == {'c': 3, 'd': 1, 'e': '#'}
