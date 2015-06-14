from __future__ import absolute_import

import pytoml
from characteristic import attributes
from montague.vendor import reify


MSF_KEYS = ('globals', 'application', 'composite', 'filter', 'server', 'logging')


@attributes(['path'], apply_immutable=True, apply_with_init=False)
class TOMLConfigLoader(object):

    def __init__(self, path):
        self.path = path

    @reify
    def _config(self):
        with open(self.path, 'rb') as infile:
            val = pytoml.load(infile)
            for key in MSF_KEYS:
                val.setdefault(key, {})
            return val

    def config(self):
        return self._config
