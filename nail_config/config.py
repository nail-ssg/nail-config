import os

import ruamel.yaml as yaml
from nail_config.common import dict_glue, dict_update


class Config(object):
    """docstring for Config"""
    _default_config = {}
    _default_config_list = []
    _config = {}
    _yaml_config = None
    _comments = {}
    _changed = False
    delimiter = '/'
    filename = ''
    auto_save = False

    def __init__(self):
        self._yaml_config = yaml.comments.CommentedMap()
        self._config = {}
        self._comments = {}

    def __call__(self, option: str = None, default_value=None):
        return self.get_option(option, default_value)

    def _assemble(self, forced=False):
        """ default-config + config + comments = yaml-config """
        if not self._changed and not forced:
            return
        self._changed = False
        _default_config = {}
        for dconf in self._default_config_list:
            dict_update(_default_config, dconf)
        result = dict_glue(_default_config, self._config, nochange=False)
        self._yaml_config = yaml.load(yaml.dump(result, Dumper=yaml.Dumper), Loader=yaml.RoundTripLoader)
        self._set_comments(self._yaml_config, self._comments)

    def _set_comments(self, node, comments):
        for key in node:
            if key in comments:
                comment = comments[key]
                if comment is not None:
                    if '#eol' in comment and comment['#eol'] is not None:
                        node.yaml_add_eol_comment(comment['#eol'], key)
                    if '#before' in comment and comment['#before'] is not None:
                        node.yaml_set_comment_before_after_key(key, before=comment['#before'])
                sub_node = node[key]
                if isinstance(sub_node, yaml.comments.CommentedMap):
                    self._set_comments(sub_node, comments[key])

    def _extract_comments(self, yaml_branch):
        result = {}
        for key in yaml_branch:
            before_comment, after_comment = self._get_round_comment(yaml_branch, key)
            eol_comment = self._get_comment(yaml_branch, key)
            if isinstance(yaml_branch[key], yaml.comments.CommentedMap):
                result[key] = self._extract_comments(yaml_branch[key])
            if before_comment is not None or after_comment is not None or eol_comment is not None:
                if key not in result:
                    result[key] = {}
                if before_comment is not None:
                    result[key]['#before'] = before_comment
                if after_comment is not None:
                    result[key]['#after'] = after_comment
                if eol_comment is not None:
                    result[key]['#eol'] = eol_comment
        return result

    def _separate(self):
        """ yaml-config -> (config, comments) """
        s = self.as_yamlstr()
        self._config = yaml.load(s, Loader=yaml.Loader)
        self._comments = self._extract_comments(self._yaml_config)

    def _get_node(self, option_name: str):
        node = self._yaml_config
        if not option_name:
            return node
        value = None
        options = option_name.split(self.delimiter)
        last_opt = options[-1]
        for option in options[:-1]:
            if not (option in node and isinstance(node[option], yaml.comments.CommentedMap)):
                return None
            node = node[option]
        return node

    def loads(self, s):
        self._yaml_config = yaml.load(s, Loader=yaml.RoundTripLoader)
        self._separate()

    def load(self, filename):
        self.filename = filename
        self._yaml_config = yaml.comments.CommentedMap()
        if os.path.exists(filename):
            # noinspection PyBroadException
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.loads(f)
                return True
            except Exception as e:
                return False
        return False

    def save(self):
        self._assemble()
        with open(self.filename, 'w', encoding='utf-8') as f:
            yaml.dump(self._yaml_config, f, Dumper=yaml.RoundTripDumper)

    def do_autosave(self):
        if not self.filename or not self.auto_save:
            return
        self.save()

    def add_default_config(self, default_config, comments):
        self._changed = True
        if default_config not in self._default_config_list:
            self._default_config_list += [default_config]
        dict_update(self._default_config, default_config)
        if comments:
            for key in comments:
                if self.get_comment(key) is None:
                    self.set_comment(key, comments[key])

    def as_yamlstr(self):
        self._assemble()
        return yaml.dump(self._yaml_config, Dumper=yaml.RoundTripDumper)

    def set_option(self, option_name: str, value, comment=None):
        old_value = self._change_tree(self._config, option_name, value, self.delimiter)
        self.set_comment(option_name, comment)
        return old_value

    def get_option(self, option_name: str, default_value=None):
        self._assemble()
        node = self._get_node(option_name)
        if not option_name:
            value = self._yaml_config
            return yaml.load(yaml.dump(value, Dumper=yaml.RoundTripDumper), Loader=yaml.Loader)
        value = default_value
        last_opt = option_name.split(self.delimiter)[-1]
        if node and last_opt in node:
            value = node[last_opt]
            if isinstance(value, yaml.comments.CommentedMap):
                value = yaml.load(yaml.dump(value, Dumper=yaml.RoundTripDumper), Loader=yaml.Loader)
        return value

    def get_comment(self, option_name: str):
        self._assemble()
        last_opt = option_name.split(self.delimiter)[-1]
        node = self._get_node(option_name)
        result = self._get_comment(node, last_opt)
        return result

    def set_comment(self, option_name: str, comment: str):
        if comment is not None:
            if comment[0] == '^':
                option_name = self.delimiter.join([option_name, '#before'])
            else:
                option_name = self.delimiter.join([option_name, '#eol'])
        self._change_tree(self._comments, option_name, comment, self.delimiter)
        self._changed = True

    @staticmethod
    def _change_tree(tree: dict, path: str, value, delimiter='/'):
        parts = path.split(delimiter)
        last_part = parts[-1]
        node = tree
        for part in parts[:-1]:
            if part not in node:
                node[part] = {}
            node = node[part]
        old_value = node[last_part] if last_part in node else None
        node[last_part] = value
        return old_value

    @staticmethod
    def _get_round_comment(node, key):
        if node.ca.comment is None:
            return None, None
        result = []
        for i in range(1, 3):
            if node.ca.comment[i] is None:
                result.push(None)
                continue
            result_item = []
            for item in node.ca.comment[i]:
                result_item += [item.value]
            result += [result_item]
        return tuple(result)  # before_comment, after_comment

    @staticmethod
    def _get_comment(node, key):
        result = None
        if node and key in node and key in node.ca.items and node.ca.items[key][2] is not None:
            value = node.ca.items[key][2].value
            if value is not None:
                result = value.split('#', 1)[1][1:]
        return result

    @staticmethod
    def _set_comment(node, option_name: str, comment: str):
        if option_name in node:
            if comment is not None:
                if comment[0] == '^':
                    node.yaml_set_comment_before_after_key(option_name, before=comment[1:])
                else:
                    node.yaml_add_eol_comment(comment, option_name)
            else:
                node.ca.items[option_name][2] = None

    @property
    def comments(self):
        return self._comments

    @property
    def changed(self):
        return self._changed
