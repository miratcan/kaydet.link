import hashlib

from django import template

register = template.Library()

GRAVATAR_BASE = 'https://www.gravatar.com/avatar/'
GRAVATAR_DEFAULT = 'mp'


@register.filter
def gravatar_url(email, size=80):
    email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()  # noqa: S324
    return f'{GRAVATAR_BASE}{email_hash}?d={GRAVATAR_DEFAULT}&s={size}'
