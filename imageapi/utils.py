import dynamic_yaml
from pathlib import Path
from functools import update_wrapper, partial

def load_config(config_path: Path):
    with open(config_path) as conf:
        config = dynamic_yaml.load(conf)
    return config


def check_mode(attribute, dec):
    def _check_authorization(f):
        def wrapper(self, *args):
            mode = getattr(self, attribute)
            if mode != "test":
                return dec(f(self, *args))
            return f(self, *args)

        return wrapper

    return _check_authorization

