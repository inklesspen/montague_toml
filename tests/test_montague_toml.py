from __future__ import absolute_import

import os
from montague.loadwsgi import Loader
from montague import load_app, load_filter, load_server
import montague_testapps
from montague.validation import validate_montague_standard_format, validate_config_loader_methods
from webtest.debugapp import debug_app

here = os.path.dirname(__file__)


LOGGING_CONF = {
    'version': 1,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'mimir': {
            'level': 'DEBUG',
            'handlers': [],
        },
        'sqlalchemy.engine': {
            'level': 'INFO',
            'handlers': [],
        },
    },
    'formatters': {
        'generic': {
            'format': '%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
            'level': 'NOTSET',
            'stream': 'ext://sys.stderr',
        }
    }
}


def test_read_config():
    expected = {
        'globals': {},
        'application': {
            'main': {'use': 'package:montague_testapps#basic_app'},
            'egg': {'use': 'egg:montague_testapps#other'},
            'filtered-app': {
                'filter-with': 'filter',
                'use': 'package:montague_testapps#basic_app',
            },
        },
        'composite': {},
        'filter': {
            'filter': {
                'use': 'egg:montague_testapps#caps',
                'method_to_call': 'lower',
            },
        },
        'server': {
            'server_factory': {
                'use': 'egg:montague_testapps#server_factory',
                'port': 42,
            },
            'server_runner': {
                'use': 'egg:montague_testapps#server_runner',
                'host': '127.0.0.1',
            },
        },
        'logging': {
            'main': LOGGING_CONF,
        }
    }
    toml_loader = Loader(os.path.join(here, 'config.toml'))
    actual = toml_loader.config_loader.config()
    assert actual == expected


def test_load_app():
    config_path = os.path.join(here, 'config.toml')
    app = load_app(config_path)
    app2 = load_app(config_path, name='egg')
    assert app is montague_testapps.apps.basic_app
    assert app2 is montague_testapps.apps.basic_app2


def test_load_filter():
    config_path = os.path.join(here, 'config.toml')
    filter = load_filter(config_path, name='filter')
    filtered = filter(None)
    assert isinstance(filtered, montague_testapps.apps.CapFilter)
    assert filtered.method_to_call == 'lower'


def test_load_server():
    config_path = os.path.join(here, 'config.toml')
    server1 = load_server(config_path, 'server_factory')
    assert isinstance(server1, montague_testapps.servers.TestServer)
    server1_testapp = server1(debug_app)
    assert server1_testapp.montague_conf['local_conf']['port'] == 42
    # server2 will be a function that does the same thing as calling server1
    # but it will be a different object due to the different entry point protocol
    server2 = load_server(config_path, 'server_runner')
    server2_testapp = server2(debug_app)
    assert server2_testapp.montague_conf['local_conf']['host'] == u'127.0.0.1'


def test_logging_conf():
    toml_loader = Loader(os.path.join(here, 'config.toml'))
    expected = LOGGING_CONF
    actual = toml_loader.logging_config()
    assert expected == actual


def test_validity():
    loader = Loader(os.path.join(here, 'config.toml'))
    config_loader = loader.config_loader
    validate_montague_standard_format(config_loader.config())
    validate_config_loader_methods(config_loader)
