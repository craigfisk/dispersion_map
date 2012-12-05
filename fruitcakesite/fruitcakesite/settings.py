# Django settings for fruitcakesite project.

# Check if deployed (server name is 'zazen')  or else assume localhost
import socket
if socket.gethostname() == 'zazen':
    DEBUG = False
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' 
else:
    DEBUG = True
    #NOTE: switch to following IF DEBUGGING LOCALLY -- writes to console (or to file)
    #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = '/tmp/fruitcake_shipments'

# Django will email ADMINS about broken links 404 with DEBUG = False + the following setting, 
# but will ignore the IGNORABLE_404_URLS.
# See https://docs.djangoproject.com/en/dev/howto/error-reporting/

SEND_BROKEN_LINK_EMAILS = True
import re
IGNORABLE_404_URLS = (
        re.compile(r'\.(php|cgi)$'),
        re.compile(r'^/phpmyadmin/'),
        re.compile(r'^/favicon\.ico$'),
        re.compile(r'^/robots\.txt$'),
        )


TEMPLATE_DEBUG = DEBUG

WIDTH_AVATAR = 120
WIDTH_FRUITCAKE = 192

ADMINS = (
    ('Craig Fisk', 'craigfisk@justfruitcake.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', #'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fruitcake',                      # Or path to database file if using sqlite3.
        'USER': 'fruitcakeuser',                      # Not used with sqlite3.
        'PASSWORD': 'Fr00t[*]C8ke',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}
#-------------------------------------------------
#  CF20121103 Note: default settings for the followng are in 
#  django/conf/global_settings.py

#email settings for craigfisk@justfruitcake.com on Thunderbird:
#   imap server name: mail.justfruitcake.com port: 993 username: craigfisk@justfruitcake.com
#   connection security: SSL/TLS, authentication: normal password
#   smtp server name: zazen.picocosmos.net port: 587
#   connection security: STARTTLS, authentication: Normal password, username: craigfisk@justfruitcake.com
# The character set of email sent with django.core.mail is set to the value of your DEFAULT_CHARSET setting (utf-8)

#See https://docs.djangoproject.com/en/1.4/topics/email/
#FILE_CHARSET = 'utf-8' #default is utf-8
##EMAIL_HOST = 'mail.justfruitcake.com' #default: localhst
##EMAIL_PORT = 25  #587 default: 25
##EMAIL_USE_TLS = False #True default: False
##EMAIL_HOST_USER = 'craigfisk@justfruitcake.com'
##EMAIL_HOST_PASSWORD = 'Sp8rky=4242'
##DEFAULT_FROM_EMAIL = 'support@justfruitcake.com' #dfault: webmaster@localhost

#See https://docs.djangoproject.com/en/1.4/topics/email/
EMAIL_HOST = 'mail.picocosmos.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# next 2 are used to authenticate to the smtp server.
EMAIL_HOST_USER = 'craigfisk@picocosmos.net'
EMAIL_HOST_PASSWORD = 'Sp8rky=4242'
DEFAULT_FROM_EMAIL = 'craigfisk@picocosmos.net' #support@justfruitcake.com'
SERVER_EMAIL = 'craigfisk@picocosmos.net'
##SERVER_EMAIL = 'support@justfruitcake.com' #default: root@localhost

FILE_UPLOAD_MAX_MEMORY_SIZE = 16777216 #16MB, 2^24; default 2621440 (2.5 MB)
FILE_UPLOAD_TEMP_DIR = None #default: Note, so Django uses Linux default /tmp
FILE_UPLOAD_PERMISSIONS = None #default: None; numeric mode which to set newly upload files, as used with os.chmod, see docs.python.org/lib/os-file-dir.html
#------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# So, ..justfruitcake/fruitcakesite with app subdirs below that, adn
#     ..justfruitcake
# respectively

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
##MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static/media/')
#MEDIA_ROOT = "/home/fisk/virt/justfruitcake/fruitcakesite/static/media/"
#images/whatever.JPG is then what is saved in database in forum_userprofile and joined to MEDIA_URL (below) for display

##See: https://docs.djangoproject.com/en/1.4/topics/forms/media/#paths-in-media-definitions
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/static/media/'
#MEDIA_URL = ''

##
LOGIN_URL = '/login/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

#CF20121107 ADMIN_MEDIA_PREFIX is removed in 1.4, see http://deathofagremmie.com/category/django/
#ADMIN_MEDIA_PREFIX = '/static/admin/'

#for django-registration
ACCOUNT_ACTIVATION_DAYS = 1

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/fisk/virt/justfruitcake/fruitcakesite/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(+ko+zwgg3t9*^5$f*+hzonc$(j&amp;md=hb(ih3y!tx5vih2vq&amp;n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #CF20121107 next setting is new in 1.4, see http://deathofagremmie.com/category/django/
    # Uncomment the next line for simple clickjacking protection:
###    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_URL = '/registration/login/'

LOGOUT_URL = '/registration/logout/'

LOGIN_REDIRECT_URL = '/registration/profile/'


ROOT_URLCONF = 'fruitcakesite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fruitcakesite.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
##    '/home/fisk/virt/justfruitcake/fruitcakesite/fruitcakesite/templates',
##    '/home/fisk/virt/justfruitcake/fruitcakesite/polls/templates',
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
#    'polls',
##    'accounts',
##    'world',
#django-registration, see readthedocs
    'registration',
    'myfruitcake',
    'forum',
)


# See https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
AUTH_PROFILE_MODULE = 'forum.UserProfile'
##'accounts.UserProfile'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
