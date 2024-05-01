# Mailman Web configuration file.
# /etc/mailman3/settings.py

# Get the default settings from mailman_web/settings/mailman.py
from mailman_web.settings.base import *
from mailman_web.settings.mailman import *

# Settings below supplement or override the defaults.
# see also https://docs.djangoproject.com/en/4.1/ref/settings/

#: Default list of admins who receive the emails from error logging.
ADMINS = [
        # ('Mailman Suite Admin', 'root@localhost'), # optional for sending exceptions via e-mail
]

# Postgresql database setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/@VARDIR@/db/mailman.db',
    }
}

# 'collectstatic' command will copy all the static files here.
# Alias this location from your webserver to `/static`
STATIC_ROOT = '@VARDIR@/web/static'

# enable the 'compress' command.
COMPRESS_ENABLED = True

# Make sure that this directory is created or Django will fail on start.
LOGGING['handlers']['file']['filename'] = '@LOGDIR@/mailmanweb.log'

#: See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "localhost",  # Archiving API from Mailman, keep it.
    "127.0.0.1",
    # "lists.your-domain.org",
    # Add here all production domains you have.
]

#: See https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins
#: these are of the form 'https://lists.example.com' or
#: 'https://*.example.com' to include subdomains
CSRF_TRUSTED_ORIGINS = [
    # "https://lists.your-domain.org",
    # Add here all production domains you have.
]

#: Filter visible Mailing Lists based on the current host being used to serve.
#:  Default: False
# FILTER_VHOST = True

#: Current Django Site being served. This is used to customize the web host
#: being used to serve the current website. For more details about Django
#: site, see: https://docs.djangoproject.com/en/dev/ref/contrib/sites/
#: in case of "FILTER_VHOST = True" consider "SITE_ID = 0" for having related site autoselected
SITE_ID = 1

# Set this to a new secret value.
SECRET_KEY = '@SECRET_KEY@'

# Set this to match the api_key setting in
# /etc/mailman3/hyperkitty.cfg (quoted here, not there).
MAILMAN_ARCHIVER_KEY = '@MAILMAN_ARCHIVER_KEY@'

# default with custom PATH
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': "@VARDIR@/archives/haystack/fulltext_index",
    },
}

# The sender of emails from Django such as address confirmation requests.
# Set this to a valid email address.
DEFAULT_FROM_EMAIL = 'admin@example.com'

# The sender of error messages from Django. Set this to a valid email
# address.
SERVER_EMAIL = 'admin@example.com'


# see also
# https://docs.mailman3.org/en/latest/config-web.html
# https://docs.mailman3.org/projects/mailman-web/en/latest/settings.html
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
# EMAIL_HOST_USER = <username>     # optional
# EMAIL_HOST_PASSWORD = <password> # optional

# Mailman Core default API Path
#  Identical except for quoting with /etc/mailman.cfg -> [webservice]
#   MAILMAN_REST_API_USER <-> admin_user
#   MAILMAN_REST_API_PASS <-> admin_pass
#  Must be aligned with /etc/mailman.cfg -> [webservice]
#   MAILMAN_REST_API_URL <-> port
MAILMAN_REST_API_URL = 'http://localhost:@RESTAPIPORT@'
MAILMAN_REST_API_USER = 'restadmin'
MAILMAN_REST_API_PASS = '@RESTAPIPASS@'

# Postorius
POSTORIUS_TEMPLATE_BASE_URL = 'http://localhost:@WEBPORT@'


### CAPTCHA support

## Google's reCAPTCHA
# service   : https://developers.google.com/recaptcha
# django-app: https://pypi.org/project/django-recaptcha/
INSTALLED_APPS.append('django_recaptcha')
# SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error'] # enable this in case RECAPTCHA_PUBLIC_KEY+RECAPTCHA_PRIVATE_KEY are not used
RECAPTCHA_PUBLIC_KEY      = '<your sitekey>'
RECAPTCHA_PRIVATE_KEY     = '<your secret key>'
RECAPTCHA_PUBLIC_KEY_V2C  = '<your sitekey V2 Checkbox>'
RECAPTCHA_PRIVATE_KEY_V2C = '<your secret key V2 Checkbox>'
RECAPTCHA_PUBLIC_KEY_V2I  = '<your sitekey V2 Invisible>'
RECAPTCHA_PRIVATE_KEY_V2I = '<your secret key V2 Invisible>'
RECAPTCHA_PUBLIC_KEY_V3   = '<your sitekey V3>'
RECAPTCHA_PRIVATE_KEY_V3  = '<your secret key V3>'
RECAPTCHA_DOMAIN          = 'www.recaptcha.net'
# RECAPTCHA_PROXY         = {'http': 'http://127.0.0.1:3128', 'https': 'https://127.0.0.1:3128'} # optional

## hCaptcha
# general   : https://docs.hcaptcha.com/
# django-app: https://pypi.org/project/django-hCaptcha/
INSTALLED_APPS.append('hcaptcha')
HCAPTCHA_SITEKEY = '<your sitekey>'
HCAPTCHA_SECRET  = '<your secret key>'
# HCAPTCHA_PROXIES = {'http': 'http://127.0.0.1:3128', 'https': 'https://127.0.0.1:3128'} # optional

## Friendly Captcha
# service   : https://docs.friendlycaptcha.com/
# django-app: https://pypi.org/project/django-friendly-captcha/
INSTALLED_APPS.append('friendly_captcha')
FRC_CAPTCHA_SITE_KEY         = '<your sitekey>'
FRC_CAPTCHA_SECRET           = '<your secret key>'
FRC_CAPTCHA_VERIFICATION_URL = 'https://api.friendlycaptcha.com/api/v1/siteverify'

## Cloudflare's Turnstile
# service   : https://developers.cloudflare.com/turnstile
# django-app: https://pypi.org/project/django-turnstile/
INSTALLED_APPS.append('turnstile')
TURNSTILE_SITEKEY = '<your sitekey>'
TURNSTILE_SECRET = '<your secret key>'
# TURNSTILE_PROXIES = {'http': 'http://127.0.0.1:3128', 'https': 'https://127.0.0.1:3128'} # optional

## CAPTCHA selector
# CAPTCHA_SERVICE = 'recaptcha' # same as recaptchaV2C
# CAPTCHA_SERVICE = 'recaptchaV2C'
# CAPTCHA_SERVICE = 'recaptchaV2I'
# CAPTCHA_SERVICE = 'recaptchaV3'
# CAPTCHA_SERVICE = 'hcaptcha'
# CAPTCHA_SERVICE = 'friendlycaptcha'
# CAPTCHA_SERVICE = 'turnstile'


# Disable gravatar by default
HYPERKITTY_ENABLE_GRAVATAR = False
INSTALLED_APPS.remove('django_gravatar')
