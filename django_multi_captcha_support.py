#### Multi CAPTCHA Support for Django
#
# (P)+(C) 2023-2023 by Peter Bieringer <pb@bieringer.de>
#
# Used at least for "enhanced" mailman3, see https://github.com/pbiering/mailman3-rpm
#
# 20231223/pbiering: initial carve-out from dedicated patches

### Generic definitions
from django.conf import settings

## activated by CAPTCHA_SERVICE

## Google's reCAPTCHA
# service   : https://developers.google.com/recaptcha
# django-app: https://pypi.org/project/django-recaptcha/
# settings  : CAPTCHA_SERVICE = 'recaptcha'    # same as 'recaptchaV2C'
#             CAPTCHA_SERVICE = 'recaptchaV2C' # (v2 "Checkbox")
#             CAPTCHA_SERVICE = 'recaptchaV2I' # (v2 "Invisible")
#             CAPTCHA_SERVICE = 'recaptchaV3'  # (v3)
# Supported optional dedicated keys per method
# RECAPTCHA_PUBLIC_KEY_V2C / RECAPTCHA_PRIVATE_KEY_V2C (v2 "Checkbox")
# RECAPTCHA_PUBLIC_KEY_V2I / RECAPTCHA_PRIVATE_KEY_V2I (v2 "Invisible")
# RECAPTCHA_PUBLIC_KEY_V3  / RECAPTCHA_PRIVATE_KEY_V3  (v3)
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV2Invisible, ReCaptchaV3


## hCaptcha
# general   : https://docs.hcaptcha.com/
# django-app: https://pypi.org/project/django-hCaptcha/
# settings  : CAPTCHA_SERVICE = 'hcaptcha'
from hcaptcha.fields import hCaptchaField


## Friendly Captcha
# service   : https://docs.friendlycaptcha.com/
# django-app: https://pypi.org/project/django-friendly-captcha/
# settings  : CAPTCHA_SERVICE = 'friendlycaptcha'
from friendly_captcha.fields import FrcCaptchaField

## Cloudflare's Turnstile
# service   : https://developers.cloudflare.com/turnstile
# django-app: https://pypi.org/project/django-turnstile/
# settings  :CAPTCHA_SERVICE = 'turnstile'
from turnstile.fields import TurnstileField


## Function for getting CAPTCHA from selected service
# Requires: "action"
#   feeded into Google's reCAPTCHA v3
def multicaptcha(action):
    captcha_service = getattr(settings, 'CAPTCHA_SERVICE', None)
    if captcha_service != None:
        if captcha_service == 'recaptcha' or captcha_service == 'recaptchaV2C':
            captcha_public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY_V2C', None)
            captcha_private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY_V2C', None)
            if captcha_public_key != None and captcha_private_key != None:
                captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, public_key=captcha_public_key, private_key=captcha_private_key)
            else:
                captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
        elif captcha_service == 'recaptchaV2I':
            captcha_public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY_V2I', None)
            captcha_private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY_V2I', None)
            if captcha_public_key != None and captcha_private_key != None:
                captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, public_key=captcha_public_key, private_key=captcha_private_key)
            else:
                captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
        elif captcha_service == 'recaptchaV3':
            captcha_public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY_V3', None)
            captcha_private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY_V3', None)
            if captcha_public_key != None and captcha_private_key != None:
                captcha = ReCaptchaField(widget=ReCaptchaV3(action=action), public_key=captcha_public_key, private_key=captcha_private_key)
            else:
                captcha = ReCaptchaField(widget=ReCaptchaV3(action=action))
        elif captcha_service == 'hcaptcha':
            captcha = hCaptchaField()
        elif captcha_service == 'friendlycaptcha':
            captcha = FrcCaptchaField()
        elif captcha_service == 'turnstile':
            captcha = TurnstileField()
        else:
            captcha = None
    else:
        captcha = None

    return captcha
