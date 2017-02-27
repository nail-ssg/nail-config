import sys
import pytest
sys.path += ['.\\nail_config']
from config import Config


@pytest.fixture(scope='function')
def empty_conf():
    print('start')
    conf = Config()
    return conf
    del conf
    print('stop')


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
