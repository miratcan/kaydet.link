import logging
from datetime import timedelta

from django.utils import timezone

from django.conf import settings

from core.exceptions import DigestServiceError

logger = logging.getLogger('core.DigestService')

PERIOD_DAYS = {
    'daily': 1,
    'weekly': 7,
}


class DigestService:

    @staticmethod
    def send_digests(period):
        from django.core.mail import send_mail

        from core.models import Link, UserPreferences

        days = PERIOD_DAYS.get(period)
        if not days:
            raise DigestServiceError(f'Unknown period: {period}')

        since = timezone.now() - timedelta(days=days)
        recent_links = Link.objects.filter(created_at__gte=since).select_related('posted_by')

        if not recent_links.exists():
            logger.info('No links to send for period: %s', period)
            return 0

        recipients = UserPreferences.objects.filter(
            summary_mails=period,
        ).select_related('user')

        sent = 0
        for pref in recipients:
            try:
                body = '\n'.join(
                    f'- {link.title} ({link.url or "text post"})' for link in recent_links[:20]
                )
                send_mail(
                    subject=f'{settings.SITE_NAME} {period} digest',
                    message=body,
                    from_email=None,
                    recipient_list=[pref.user.email],
                    fail_silently=True,
                )
                sent += 1
            except Exception:
                logger.exception('Failed to send digest to %s', pref.user.email)

        logger.info('Sent %d %s digests', sent, period)
        return sent
