import sys
import pytest
sys.path += ['.\\nail_config']
from config import Config


@pytest.fixture(scope='function')
def empty_conf():
    conf = Config()
    return conf
    del conf


@pytest.fixture(scope='function')
def two_conf():
    conf1 = Config()
    conf2 = Config()
    return (conf1, conf2)
    del conf


def test_set_value(empty_conf):
    old_value = empty_conf.set_option('level1.level2.level3', 'value')
    assert old_value is None
    value = empty_conf.get_option('level1.level2.level3')
    assert value == 'value'
    comment = empty_conf.get_comment('level1.level2.level3')
    assert comment is None


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


def test_set_value3(two_conf):
    conf1, conf2 = two_conf
    old_value1 = conf1.set_option('level1.level2.level3', 'value1')
    old_value2 = conf2.set_option('level1.level2.level3', 'value2')
    value1 = conf1.get_option('level1.level2.level3')
    assert old_value1 is None
    assert old_value2 is None
    assert value1 == 'value1'


def test_set_comment(empty_conf):
    empty_conf.set_option('level1.level2.level3', 'value1', 'comment1')
    empty_conf.set_comment('level1.level2.level3', 'comment2')
    comment = empty_conf.get_comment('level1.level2.level3')
    assert comment == 'comment2'