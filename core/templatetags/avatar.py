import hashlib

from django import template

register = template.Library()

GRAVATAR_BASE = 'https://www.gravatar.com/avatar/'


@register.simple_tag
def avatar_url(user, size=80):
    """Return avatar URL: Google profile picture > Gravatar > default."""
    if not user or not hasattr(user, 'pk'):
        return ''

    # Try Google (or any social) profile picture
    try:
        from allauth.socialaccount.models import SocialAccount

        account = SocialAccount.objects.filter(user=user).first()
        if account:
            picture = account.extra_data.get('picture', '')
            if picture:
                return picture
    except Exception:
        pass

    # Fallback to Gravatar
    email = getattr(user, 'email', '') or ''
    email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()  # noqa: S324
    return f'{GRAVATAR_BASE}{email_hash}?d=mp&s={size}'
