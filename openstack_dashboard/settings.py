# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import os
import sys

from openstack_dashboard import exceptions
from django.utils.translation import ugettext_lazy as _

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.abspath(os.path.join(ROOT_PATH, '..', 'bin'))

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_BRANDING = _('Syscloud Control Panel')

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'
# LOGIN_REDIRECT_URL can be used as an alternative for
# HORIZON_CONFIG.user_home, if user_home is not set.
# Do not set it to '/home/', as this will cause circular redirect loop
LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(ROOT_PATH, '..', 'static'))
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

ROOT_URLCONF = 'openstack_dashboard.urls'

HORIZON_CONFIG = {
    'dashboards': ('project', 'admin', 'settings',),
    'default_dashboard': 'project',
    'user_home': 'horizon.views.base.get_user_home',
    'ajax_queue_limit': 10,
    'help_url': "http://go.sisyun.com",
    'exceptions': {'recoverable': exceptions.RECOVERABLE,
                   'not_found': exceptions.NOT_FOUND,
                   'unauthorized': exceptions.UNAUTHORIZED},
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'horizon.middleware.HorizonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'horizon.context_processors.horizon',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'horizon.loaders.TemplateLoader'
)

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

less_binary = os.path.join(BIN_DIR, 'less', 'lessc')
COMPRESS_PRECOMPILERS = (
    ('text/less', (less_binary + ' {infile} {outfile}')),
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
)

COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = 'dashboard'
COMPRESS_CSS_HASHING_METHOD = 'hash'
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

INSTALLED_APPS = (
    'openstack_dashboard',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'compressor',
    'horizon',
    'horizon.dashboards.project',
    'horizon.dashboards.admin',
    'horizon.dashboards.settings',
    'openstack_auth',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
AUTHENTICATION_BACKENDS = ('openstack_auth.backend.KeystoneBackend',)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = False

gettext_noop = lambda s: s
LANGUAGES = (
    ('en', gettext_noop('English')),
    ('zh-cn', gettext_noop('Simplified Chinese')),
)
LANGUAGE_CODE = 'zh-cn'
USE_I18N = True
USE_L10N = True
USE_TZ = True

OPENSTACK_KEYSTONE_DEFAULT_ROLE = 'Member'

DEFAULT_EXCEPTION_REPORTER_FILTER = 'horizon.exceptions.HorizonReporterFilter'

try:
    from local.local_settings import *
except ImportError:
    logging.warning("No local_settings file found.")

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
