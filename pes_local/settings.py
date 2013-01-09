# -*- coding:utf-8 -*-

PROJECT_NAME = 'tthess' 
SESAME_REPOSITORY_NAME = "pesRepository"
SECRET_KEY = '+y&amp;b#6s@9ysxzp)xaq2%g%)9f39i2$oickf3#yp6bvy5!%%p_7'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PES_USE_CONTEXT = True

# SESAME_REPOSITORY_NAME = 'thessRepository'

import os.path
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# OpenRDF configuration
OPENRDF_SERVER_NAME = 'localhost'  # default value ... to be change
OPENRDF_SERVER_PORT = '8080'       # default value when served with stock jetty conf


ROOT_URLCONF = 'pes_local.urls'
WSGI_APPLICATION = 'pes_local.wsgi.application'


LOCALE_PATHS = (
    '/home/clo/projects/pes/pes/locale',
)

# uncommnt and set your own SENTRY_DSN
# SENTRY_DSN = ''

# uncomment and set your own main city
# DEFAULT_MAIN_CITY = (Point(5.3697800, 43.2964820), u'Marseille')  #set your own main city

from django.core.exceptions import ImproperlyConfigured

try:
    from pes.default_project_settings import *
except ImportError, exp:
    raise ImproperlyConfigured("Unable to find default_project_settings.py file from pes")


# debug settings : load dev tools (FireLogger & Django debug Toolbar) or setup Sentry Logging
try:
    DEBUG_SETTINGS = {'apps': INSTALLED_APPS,
                      'middleware': MIDDLEWARE_CLASSES,
                      'logging': LOGGING
                        }
    from pes.debug_settings import *
except ImportError, exp:
    raise ImproperlyConfigured("Unable to find pes/debug_settings.py file in pes : ", exp)


# db_settings file for DATABASES, DATABASE ROUTERS and CACHE backend settings
try:
    from db_settings import *
except ImportError, exp:
    raise ImproperlyConfigured("No db_settings.py file was found")


SITE_TITLE = 'tthess'



INSTALLED_APPS += (
    'pes_local',)


FEED_MODELS = [
    'tag', 'navtree',
    ]
# Later, it should be
# FEED_MODELS=['organization', 'person', 'role', 'product', 'engagement', 'location', 
#               'relation', 'exchange', 'contact', 'article']




