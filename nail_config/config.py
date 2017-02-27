import os
from common import dict_enrich, dict_concat2
import ruamel.yaml as yaml


class Config(object):

    """docstring for Config"""
    _default_config = {}
    _config = {}
    _config_filename = ''
    _yaml_config = None

    def __init__(self, filename='.config.yml'):
        self._config_filename = filename
        self._config = self.load()
        self._yaml_config = yaml.comments.CommentedMap()
        print(self.as_yamlstr())

    def __call__(self, option: str = None, default_value=None):
        return self.config(option, default_value)

    def load(self):
        filename = self._config_filename
        self._config = {}
        if not os.path.exists(filename):
            self._config = {}
        else:
            with open(filename, 'r') as f:
                d = yaml.load(f, yaml.RoundTripLoader)
                self._config = dict_concat2(self._config, d)
        return self._config

    def config(self, option: str = None, default_value=None):
        section = self._default_config.copy()
        section = dict_concat2(section, self._config)
        if option is None:
            return section
        section_names = option.split('.')
        name = section_names[-1]
        for section_name in section_names[:-1]:
            if section_name not in section:
                section[section_name] = {}
            section = section[section_name]
        if name not in section:
            section[name] = default_value
        return section[name]

    def save(self):
        with open(self._config_filename, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)

    def default_config(self, dconf, comments):
        self._default_config = dict_enrich(self._default_config, dconf)

    def as_yamlstr(self):
        return yaml.dump(self._yaml_config, Dumper=yaml.RoundTripDumper)

    def set_option(self, option_name: str, value, comment=None):
        old_value = None
        options = option_name.split('.')
        last_opt = options[-1]
        node = self._yaml_config
        for option in options[:-1]:
            if not (option in node and isinstance(node[option], yaml.comments.CommentedMap)):
                node[option] = yaml.comments.CommentedMap()
            node = node[option]
        if last_opt in node:
            old_value = node[last_opt]
        node[last_opt] = value
        if comment is not None:
            node.yaml_add_eol_comment(comment, last_opt)
        return old_value

    def get_option(self, option_name: str):
        value = None
        options = option_name.split('.')
        last_opt = options[-1]
        node = self._yaml_config
        for option in options[:-1]:
            if not (option in node and isinstance(node[option], yaml.comments.CommentedMap)):
                return None
            node = node[option]
        if last_opt in node:
            value = node[last_opt]
        return value

    def get_comment(self, option_name: str):
        value = None
        options = option_name.split('.')
        last_opt = options[-1]
        node = self._yaml_config
        for option in options[:-1]:
            if not (option in node and isinstance(node[option], yaml.comments.CommentedMap)):
                return None
            node = node[option]
        if last_opt in node and last_opt in node.ca.items and node.ca.items[last_opt][2] is not None:
            value = node.ca.items[last_opt][2].value
            if value is not None:
                value = value[3:]
        return value
