"""
Configuration file for settings
"""

SECRET_KEY = '<SECRET KEY>'

ALLOWED_HOSTS = ['*']

DB_NAME = 'iitbcn'

DB_USERNAME = 'iitbcn'

DB_PASSWORD = 'iitbcn'

DB_HOST_NAME = 'localhost'

DB_PORT = '5432'

ADMINS_EMAIL_LIST = [
    # ('Name', 'email@example.com'),
]

EMAIL_BACKEND = 'core.notification.IITBEmailBackend'

# Email server settings
EMAIL_HOST = 'smtp-auth.iitb.ac.in'
EMAIL_PORT = 25

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_FROM = 'iitbcn@iitb.ac.in'

EMAIL_SUBJECT_PREFIX = '[IITBCN] '
