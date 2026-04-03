from django.core.management.base import BaseCommand

from core.services.digest import DigestService


class Command(BaseCommand):
    help = 'Send digest emails (daily or weekly)'

    def add_arguments(self, parser):
        parser.add_argument(
            'period',
            choices=['daily', 'weekly'],
            help='Digest period',
        )

    def handle(self, *args, **options):
        period = options.get('period')
        sent = DigestService.send_digests(period)
        self.stdout.write(self.style.SUCCESS(f'Sent {sent} {period} digests'))
