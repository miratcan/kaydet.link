import logging
from urllib.parse import urljoin, urlparse

import markdown_it
import nh3
import requests
from bs4 import BeautifulSoup
from django.db.models import Exists, OuterRef, Q, Value

from core.exceptions import LinkServiceError

logger = logging.getLogger('core.LinkService')

SCRAPE_TIMEOUT = 15
SCRAPE_USER_AGENT = 'Mozilla/5.0 (compatible; kaydet-link/1.0)'
LINKS_PER_PAGE = 25


class LinkService:

    @staticmethod
    def render_markdown(text):
        md = markdown_it.MarkdownIt('commonmark', {'html': False})
        raw_html = md.render(text)
        return nh3.clean(raw_html)

    @staticmethod
    def scrape_url(url):
        if not url or not url.startswith(('http://', 'https://')):
            return {}

        try:
            response = requests.get(
                url,
                timeout=SCRAPE_TIMEOUT,
                headers={'User-Agent': SCRAPE_USER_AGENT},
            )
        except requests.RequestException as exc:
            logger.exception('Failed to scrape URL: %s', url)
            raise LinkServiceError('Could not fetch URL') from exc

        metadata = {}
        images = []
        content_type = response.headers.get('content-type', '')

        if 'text/html' in content_type:
            soup = BeautifulSoup(response.text, 'html.parser')
            if not soup:
                return {'metadata': metadata, 'images': images}

            # collect all og: meta tags
            for tag in soup.find_all('meta', attrs={'property': True}):
                prop = tag.get('property', '')
                content = tag.get('content', '').strip()
                if prop.startswith('og:') and content:
                    metadata[prop] = content

            # fallbacks for title and description
            if 'og:title' not in metadata and soup.title and soup.title.string:
                metadata['og:title'] = soup.title.string.strip()

            if 'og:description' not in metadata:
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    metadata['og:description'] = meta_desc.get('content', '').strip()

            # build images list from og:image
            if metadata.get('og:image'):
                img_url = metadata.get('og:image')
                if not img_url.startswith('http'):
                    img_url = urljoin(url, img_url)
                    metadata['og:image'] = img_url
                images.append(img_url)

        elif 'image' in content_type:
            images = [url]
            metadata['og:image'] = url

        return {'metadata': metadata, 'images': images}

    @staticmethod
    def get_or_create_link(url):
        from core.models import Link

        link, created = Link.objects.get_or_create(url=url)
        if created:
            try:
                result = LinkService.scrape_url(url)
                link.metadata = result.get('metadata', {})
                link.save(update_fields=['metadata'])
            except Exception:
                pass
        return link

    @staticmethod
    def build_feed(user=None, tag=None, saved_by=None, ordering='hot', page=1):
        from core.models import Bookmark, Link

        query = Q()

        if tag:
            query &= Q(bookmark__tags=tag)

        if saved_by:
            query &= Q(bookmark__user=saved_by)

        links = Link.objects.filter(query).distinct()

        if user and user.is_authenticated:
            from django.db.models import Subquery

            links = links.annotate(
                is_saved=Exists(
                    Bookmark.objects.filter(
                        user=user,
                        link=OuterRef('pk'),
                    ),
                ),
                user_bookmark_id=Subquery(
                    Bookmark.objects.filter(
                        user=user,
                        link=OuterRef('pk'),
                    ).values('pk')[:1],
                ),
            )
        else:
            from django.db.models import IntegerField

            links = links.annotate(
                is_saved=Value(False),
                user_bookmark_id=Value(None, output_field=IntegerField()),
            )

        order_map = {
            'hot': '-last_saved_at',
            'top': '-save_count',
            'latest': '-created_at',
            'discussed': '-comment_count',
        }
        links = links.order_by(order_map.get(ordering, '-last_saved_at'))

        from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

        paginator = Paginator(links, LINKS_PER_PAGE)

        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)
