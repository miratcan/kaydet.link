from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Bookmark, Comment, Link, Tag

User = get_user_model()

TAGS = ['python', 'django', 'javascript', 'rust', 'web', 'devops', 'design']

LINKS = [
    {
        'url': 'https://www.djangoproject.com/',
        'metadata': {'og:title': 'Django 6.0 Released', 'og:description': 'The latest version of Django is out with exciting new features.', 'og:image': 'https://static.djangoproject.com/img/logos/django-logo-negative.png'},
        'note': 'Big release. Async support is finally mature.',
        'tags': ['python', 'django', 'web'],
    },
    {
        'url': 'https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html',
        'metadata': {'og:title': 'Understanding Rust Ownership', 'og:description': 'A deep dive into Rust\'s ownership system.', 'og:image': 'https://www.rust-lang.org/static/images/rust-social-wide.jpg'},
        'note': 'Best explanation of ownership I\'ve read.',
        'tags': ['rust'],
    },
    {
        'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties',
        'metadata': {'og:title': 'CSS Custom Properties Guide', 'og:description': 'Learn how to use CSS variables effectively.', 'og:image': 'https://developer.mozilla.org/mdn-social-share.cd6c4a5a.png'},
        'tags': ['web', 'design'],
    },
    {
        'url': 'https://docs.astral.sh/uv/',
        'metadata': {'og:title': 'uv \u2014 An extremely fast Python package installer', 'og:description': 'A fast Python package installer and resolver, written in Rust.'},
        'note': 'After years of pip and poetry, uv is a breath of fresh air.',
        'tags': ['python', 'devops'],
    },
    {
        'url': 'https://htmx.org/',
        'metadata': {'og:title': 'htmx \u2014 High Power Tools for HTML', 'og:description': 'Access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML.', 'og:image': 'https://htmx.org/img/htmx_logo.1.png'},
        'note': 'This + Django = no need for React.',
        'tags': ['javascript', 'web'],
    },
    {
        'url': 'https://www.postgresql.org/',
        'metadata': {'og:title': 'PostgreSQL 17 Released', 'og:description': 'Major improvements to performance, developer experience, and observability.', 'og:image': 'https://www.postgresql.org/media/img/about/press/elephant.png'},
        'tags': ['devops'],
    },
    {
        'url': 'https://aosabook.org/en/',
        'metadata': {'og:title': 'The Architecture of Open Source Applications', 'og:description': 'Free book covering how real open source projects are structured.'},
        'note': 'Wish I had this when I started programming.',
        'tags': ['design'],
    },
    {
        'url': 'https://tailwindcss.com/docs/utility-first',
        'metadata': {'og:title': 'Utility-First Fundamentals \u2014 Tailwind CSS', 'og:description': 'Using utility classes to build custom designs without writing CSS.'},
        'note': 'Unpopular opinion: utility-first CSS couples your markup to presentation.',
        'tags': ['web', 'design'],
    },
    {
        'url': 'https://click.palletsprojects.com/',
        'metadata': {'og:title': 'Click \u2014 Python CLI Framework', 'og:description': 'Click is a Python package for creating beautiful command line interfaces.', 'og:image': 'https://click.palletsprojects.com/en/stable/_images/click-logo.png'},
        'tags': ['python'],
    },
    {
        'url': 'https://litestream.io/',
        'metadata': {'og:title': 'Litestream \u2014 Streaming SQLite Replication', 'og:description': 'Continuously stream SQLite changes to S3-compatible storage.', 'og:image': 'https://litestream.io/img/logo.svg'},
        'note': 'SQLite in prod is actually viable with this.',
        'tags': ['devops'],
    },
    {
        'url': 'https://www.rust-lang.org/',
        'metadata': {'og:title': 'Rust Programming Language', 'og:description': 'A language empowering everyone to build reliable and efficient software.'},
        'note': 'Memory safety without garbage collection. Every C developer should learn this.',
        'tags': ['rust'],
    },
    {
        'url': 'https://django-ninja.dev/',
        'metadata': {'og:title': 'Django Ninja \u2014 Fast Django REST Framework', 'og:description': 'A fast, async-ready alternative to DRF with automatic OpenAPI docs.', 'og:image': 'https://django-ninja.dev/img/logo-big.png'},
        'tags': ['python', 'django', 'web'],
    },
    {
        'url': 'https://norvig.com/21-days.html',
        'metadata': {'og:title': 'Teach Yourself Programming in Ten Years \u2014 Peter Norvig', 'og:description': 'Why it takes ten years to learn programming, not 21 days.'},
        'note': 'Required reading for every new developer.',
        'tags': ['design'],
    },
]


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@linkfloyd.dev', 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin.set_password('admin')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (password: admin)'))

        extra_users = []
        for uname, email in [('floyd', 'floyd@example.com'), ('ada', 'ada@example.com'), ('linus', 'linus@example.com')]:
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={'email': email},
            )
            if created:
                u.set_password(f'{uname}123')
                u.save()
                self.stdout.write(self.style.SUCCESS(f'Created user {uname} (password: {uname}123)'))
            extra_users.append(u)

        tags = {}
        for name in TAGS:
            tag, _created = Tag.objects.get_or_create(
                slug=slugify(name),
                defaults={'name': name},
            )
            tags[name] = tag

        users = [admin, *extra_users]

        # create links and first bookmarks
        for i, link_data in enumerate(LINKS):
            poster = users[i % len(users)]
            link, created = Link.objects.get_or_create(
                url=link_data.get('url'),
                defaults={'metadata': link_data.get('metadata', {})},
            )
            if created:
                self.stdout.write(f'  Created link: {link.title}')

            # first bookmark = the person who shared it
            bm, bm_created = Bookmark.objects.get_or_create(
                user=poster,
                link=link,
                defaults={'note': link_data.get('note', '')},
            )
            if bm_created:
                bm.tags.set([tags[t] for t in link_data.get('tags', [])])

        # additional saves from other users
        if Bookmark.objects.count() <= len(LINKS):
            import random
            all_links = list(Link.objects.all())
            extra_count = 0
            for link in all_links:
                existing_users = set(link.bookmarks.values_list('user_id', flat=True))
                for u in users:
                    if u.pk in existing_users:
                        continue
                    if random.random() < 0.4:  # noqa: S311
                        first_bm = link.bookmarks.first()
                        Bookmark.objects.create(user=u, link=link, parent=first_bm)
                        extra_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created {extra_count} additional saves'))

        if not Comment.objects.exists():
            all_links = list(Link.objects.all())
            comments_data = [
                (all_links[0], extra_users[0], 'This is great news!'),
                (all_links[0], admin, 'Agreed, can\'t wait to try the new features.'),
                (all_links[0], extra_users[1], 'Already upgraded, zero issues so far.'),
                (all_links[1], extra_users[2], 'Ownership is the hardest part of Rust for newcomers.'),
                (all_links[1], extra_users[0], 'Once it clicks, you never want to go back to manual memory management.'),
                (all_links[4], admin, 'htmx + Django is such a great combo.'),
                (all_links[4], extra_users[1], 'Replaced our entire React frontend with htmx. No regrets.'),
                (all_links[7], extra_users[0], 'Strong disagree. Tailwind saved us so much time.'),
                (all_links[7], extra_users[2], 'I agree with OP. Semantic CSS > utility classes.'),
                (all_links[7], admin, 'Both approaches have tradeoffs. Use what fits your team.'),
                (all_links[3], extra_users[1], 'uv is insanely fast. pip feels ancient now.'),
                (all_links[10], extra_users[0], 'Ninja is great for new projects but DRF has a much bigger ecosystem.'),
                (all_links[11], extra_users[2], 'Classic Norvig. Should be required reading.'),
            ]
            for link, user, body in comments_data:
                Comment.objects.create(link=link, posted_by=user, body=body)
            self.stdout.write(self.style.SUCCESS(f'Created {len(comments_data)} comments'))

        self.stdout.write(self.style.SUCCESS('Seed complete'))
