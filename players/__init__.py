import os
from importlib import import_module

__all__ = []

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith('.py'):
        name = filename[:-3]
        module = import_module('players.%s' % name)
        globals()[name] = module
        __all__.append(name)
