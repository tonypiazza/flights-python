"""
    Configuration data for report apps.
"""

from yaml import load


class Config(object):
    """Loads application configuration from YAML file and makes it available as
       properties
    """
    instance = None

    class __Config(object):
        def __init__(self):
            try:
                from yaml import CLoader as Loader, CDumper as Dumper
            except ImportError:
                from yaml import Loader, Dumper
            with open('config.yaml', 'r') as f:
                data = load(f, Loader=Loader)
                self.airportPath = data['airportPath']
                self.carrierPath = data['carrierPath']
                self.flightPaths = data['flightPaths']
                self.planePath = data['planePath']

    def __str__(self):
        return repr(self.instance)

    def __init__(self):
        if not Config.instance:
            Config.instance = Config.__Config()

    def __getattr__(self, name):
        return getattr(self.instance, name)
