import sys
import ruamel.yaml as yaml


def yprint(obj):
    yaml.dump(obj, sys.stdout)
