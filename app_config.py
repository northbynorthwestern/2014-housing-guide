#!/usr/bin/env python

"""
Project-wide application configuration.

DO NOT STORE SECRETS, PASSWORDS, ETC. IN THIS FILE.
They will be exposed to users. Use environment variables instead.
See get_secrets() below for a fast way to access them.
"""

import os

"""
NAMES
"""
# Project name used for display
PROJECT_NAME = 'Housing Guide'

# Project name to be used in urls
# Use dashes, not underscores!
PROJECT_SLUG = 'housing'

# The name of the repository containing the source
REPOSITORY_NAME = 'housing2'
REPOSITORY_URL = 'git@github.com:TylerFisher/%s.git' % REPOSITORY_NAME
REPOSITORY_ALT_URL = None # 'git@bitbucket.org:nprapps/%s.git' % REPOSITORY_NAME'

# Project name used for assets rig
# Should stay the same, even if PROJECT_SLUG changes
ASSETS_SLUG = 'housing2'

# Project name to be used in file paths
PROJECT_FILENAME = 'housing2'

"""
DEPLOYMENT
"""
PRODUCTION_S3_BUCKETS = ['apps.northbynorthwestern.com']
STAGING_S3_BUCKETS = []
ASSETS_S3_BUCKET = []

PRODUCTION_SERVERS = ['cron.nprapps.org']
STAGING_SERVERS = ['50.112.92.131']

# Should code be deployed to the web/cron servers?
DEPLOY_TO_SERVERS = False

SERVER_USER = 'ubuntu'
SERVER_PYTHON = 'python2.7'
SERVER_PROJECT_PATH = '/home/%s/apps/%s' % (SERVER_USER, PROJECT_FILENAME)
SERVER_REPOSITORY_PATH = '%s/repository' % SERVER_PROJECT_PATH
SERVER_VIRTUALENV_PATH = '%s/virtualenv' % SERVER_PROJECT_PATH

# Should the crontab file be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_CRONTAB = False

# Should the service configurations be installed on the servers?
# If True, DEPLOY_TO_SERVERS must also be True
DEPLOY_SERVICES = False

UWSGI_SOCKET_PATH = '/tmp/%s.uwsgi.sock' % PROJECT_FILENAME
UWSGI_LOG_PATH = '/var/log/%s.uwsgi.log' % PROJECT_FILENAME
APP_LOG_PATH = '/var/log/%s.app.log' % PROJECT_FILENAME

# Services are the server-side services we want to enable and configure.
# A three-tuple following this format:
# (service name, service deployment path, service config file extension)
SERVER_SERVICES = [
    ('app', SERVER_REPOSITORY_PATH, 'ini'),
    ('uwsgi', '/etc/init', 'conf'),
    ('nginx', '/etc/nginx/locations-enabled', 'conf'),
]

# These variables will be set at runtime. See configure_targets() below
S3_BUCKETS = []
S3_BASE_URL = ''
SERVERS = []
SERVER_BASE_URL = ''
DEBUG = True

"""
COPY EDITING
"""
COPY_GOOGLE_DOC_KEY = '0AqjLQISCZzBkdEFBTHAtWHlGNnA5N2pFSTdsQUlnbnc'
COPY_PATH = 'data/copy.xlsx'

"""
SHARING
"""
PROJECT_DESCRIPTION = "The North by Northwestern Freshman Housing Guide, featuring photos, videos, statistics and the opinions of current residents of Northwestern University's housing options."
SHARE_URL = 'http://%s/%s/' % (PRODUCTION_S3_BUCKETS[0], PROJECT_SLUG)

# Will be resized to 120x120, can't be larger than 1MB
TWITTER_IMAGE_URL = ''
TWITTER_HANDLE = '@nbn_tweets'

# 16:9 ("wide") image. FB uses 16:9 in the newsfeed and crops to square in timelines.
# No documented restrictions on size
FACEBOOK_IMAGE_URL = ''
FACEBOOK_APP_ID = ''

# Thumbnail image for Google News / Search.
# No documented restrictions on resolution or size
GOOGLE_IMAGE_URL = TWITTER_IMAGE_URL

NPR_DFP = {
    'STORY_ID': '1002',
    'TARGET': 'homepage',
    'ENVIRONMENT': 'NPRTEST',
    'TESTSERVER': 'false'
}

"""
SERVICES
"""
GOOGLE_ANALYTICS = {
    'ACCOUNT_ID': 'UA-15143352-1',
    'DOMAIN': PRODUCTION_S3_BUCKETS[0],
    'TOPICS': '' # e.g. '[1014,3,1003,1002,1001]'
}

"""
Utilities
"""
def get_secrets():
    """
    A method for accessing our secrets.
    """
    secrets = [
        'EXAMPLE_SECRET'
    ]

    secrets_dict = {}

    for secret in secrets:
        name = '%s_%s' % (PROJECT_FILENAME, secret)
        secrets_dict[secret] = os.environ.get(name, None)

    return secrets_dict

def configure_targets(deployment_target):
    """
    Configure deployment targets. Abstracted so this can be
    overriden for rendering before deployment.
    """
    global S3_BUCKETS
    global S3_BASE_URL
    global SERVERS
    global SERVER_BASE_URL
    global DEBUG
    global DEPLOYMENT_TARGET
    global APP_LOG_PATH

    if deployment_target == 'production':
        S3_BUCKETS = PRODUCTION_S3_BUCKETS
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKETS[0], PROJECT_SLUG)
        SERVERS = PRODUCTION_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        DEBUG = False
    elif deployment_target == 'staging':
        S3_BUCKETS = STAGING_S3_BUCKETS
        S3_BASE_URL = 'http://%s/%s' % (S3_BUCKETS[0], PROJECT_SLUG)
        SERVERS = STAGING_SERVERS
        SERVER_BASE_URL = 'http://%s/%s' % (SERVERS[0], PROJECT_SLUG)
        DEBUG = True
    else:
        S3_BUCKETS = []
        S3_BASE_URL = 'http://127.0.0.1:8000'
        SERVERS = []
        SERVER_BASE_URL = 'http://127.0.0.1:8001/%s' % PROJECT_SLUG
        DEBUG = True
        APP_LOG_PATH = '/tmp/%s.app.log' % PROJECT_SLUG

    DEPLOYMENT_TARGET = deployment_target

"""
Run automated configuration
"""
DEPLOYMENT_TARGET = os.environ.get('DEPLOYMENT_TARGET', None)

configure_targets(DEPLOYMENT_TARGET)

