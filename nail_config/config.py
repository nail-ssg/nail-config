import os
from .common import dict_enrich, dict_concat2
import ruamel.yaml as yaml


class Config(object):
    """docstring for Config"""
    _default_config = {}
    _config = {}
    _config_filename = ''

    def __init__(self, filename='.config.yml'):
        self._config_filename = filename
        self._config = self.load_config()

    def load_config(self):
        filename = self._config_filename
        self._config = {}
        if not os.path.exists(filename):
            self._config = {}
        else:
            with open(filename, 'r') as f:
                d = yaml.load(f, yaml.RoundTripLoader)
                self._config = dict_concat2(self._config, d)
        return self._config

    def __call__(self, option: str = None, default_value=None):
        return self.config(option, default_value)

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
