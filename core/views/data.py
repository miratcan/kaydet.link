import csv
import io
import json
import re
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView

from core.models import Bookmark, Tag
from core.services.link import LinkService


class ExportView(LoginRequiredMixin, TemplateView):
    template_name = 'data/export.html'


class ExportJSONView(LoginRequiredMixin, View):
    def get(self, request):
        bookmarks = (
            Bookmark.objects.filter(user=request.user)
            .select_related('link')
            .prefetch_related('tags')
            .order_by('-created_at')
        )

        data = {
            'exported_at': datetime.now().isoformat(),
            'format': 'kaydet.link',
            'version': 1,
            'bookmarks': [
                {
                    'url': bm.link.url,
                    'title': bm.link.title,
                    'description': bm.link.description,
                    'note': bm.note,
                    'tags': list(bm.tags.values_list('name', flat=True)),
                    'is_private': bm.is_private,
                    'status': bm.status,
                    'is_pinned': bm.is_pinned,
                    'created_at': bm.created_at.isoformat(),
                }
                for bm in bookmarks
            ],
        }

        response = HttpResponse(
            json.dumps(data, indent=2, ensure_ascii=False),
            content_type='application/json',
        )
        response['Content-Disposition'] = 'attachment; filename="kaydet-link-export.json"'
        return response


class ExportHTMLView(LoginRequiredMixin, View):
    """Export in Netscape Bookmark File Format."""

    def get(self, request):
        bookmarks = (
            Bookmark.objects.filter(user=request.user)
            .select_related('link')
            .prefetch_related('tags')
            .order_by('-created_at')
        )

        lines = [
            '<!DOCTYPE NETSCAPE-Bookmark-file-1>',
            '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
            '<TITLE>Bookmarks</TITLE>',
            '<H1>Bookmarks</H1>',
            '<DL><p>',
        ]

        # Group by tags
        tagged = {}
        untagged = []
        for bm in bookmarks:
            tags = list(bm.tags.values_list('name', flat=True))
            if tags:
                for tag in tags:
                    tagged.setdefault(tag, []).append(bm)
            else:
                untagged.append(bm)

        for tag, bms in sorted(tagged.items()):
            lines.append(f'    <DT><H3>{tag}</H3>')
            lines.append('    <DL><p>')
            for bm in bms:
                ts = int(bm.created_at.timestamp())
                title = bm.link.title or bm.link.url
                lines.append(f'        <DT><A HREF="{bm.link.url}" ADD_DATE="{ts}">{title}</A>')
                if bm.note:
                    lines.append(f'        <DD>{bm.note}')
            lines.append('    </DL><p>')

        if untagged:
            lines.append('    <DT><H3>Untagged</H3>')
            lines.append('    <DL><p>')
            for bm in untagged:
                ts = int(bm.created_at.timestamp())
                title = bm.link.title or bm.link.url
                lines.append(f'        <DT><A HREF="{bm.link.url}" ADD_DATE="{ts}">{title}</A>')
                if bm.note:
                    lines.append(f'        <DD>{bm.note}')
            lines.append('    </DL><p>')

        lines.append('</DL><p>')

        response = HttpResponse('\n'.join(lines), content_type='text/html')
        response['Content-Disposition'] = 'attachment; filename="kaydet-link-bookmarks.html"'
        return response


class ExportCSVView(LoginRequiredMixin, View):
    def get(self, request):
        bookmarks = (
            Bookmark.objects.filter(user=request.user)
            .select_related('link')
            .prefetch_related('tags')
            .order_by('-created_at')
        )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['url', 'title', 'note', 'tags', 'is_private', 'status', 'created_at'])

        for bm in bookmarks:
            writer.writerow([
                bm.link.url,
                bm.link.title,
                bm.note,
                ', '.join(bm.tags.values_list('name', flat=True)),
                bm.is_private,
                bm.status,
                bm.created_at.isoformat(),
            ])

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="kaydet-link-export.csv"'
        return response


class ImportView(LoginRequiredMixin, TemplateView):
    template_name = 'data/import.html'

    def post(self, request):
        uploaded = request.FILES.get('file')
        if not uploaded:
            return self.render_to_response({'error': 'No file uploaded.'})

        content = uploaded.read().decode('utf-8', errors='replace')
        filename = uploaded.name.lower()

        if filename.endswith('.json'):
            result = self._import_json(request.user, content)
        elif filename.endswith('.html') or filename.endswith('.htm'):
            result = self._import_html(request.user, content)
        else:
            return self.render_to_response({'error': 'Unsupported format. Use .json or .html.'})

        return self.render_to_response({'result': result})

    def _import_json(self, user, content):
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON file.'}

        bookmarks = data.get('bookmarks', [])
        created = 0
        skipped = 0

        for item in bookmarks:
            url = item.get('url', '').strip()
            if not url:
                continue

            link = LinkService.get_or_create_link(url)

            if Bookmark.objects.filter(user=user, link=link).exists():
                skipped += 1
                continue

            note = item.get('note', '')
            is_private = item.get('is_private', True)
            status = item.get('status', 'unread')

            bm = Bookmark.objects.create(
                user=user,
                link=link,
                note=note,
                is_private=is_private,
                status=status,
            )

            # Tags
            tag_names = item.get('tags', [])
            if tag_names:
                tags = []
                for name in tag_names:
                    slug = slugify(name, allow_unicode=True)
                    if slug:
                        tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
                        tags.append(tag)
                bm.tags.set(tags)

            created += 1

        return {'created': created, 'skipped': skipped, 'total': len(bookmarks)}

    def _import_html(self, user, content):
        # Parse Netscape Bookmark File Format
        created = 0
        skipped = 0
        total = 0

        # Find all <A> tags with HREF
        link_pattern = re.compile(
            r'<[Aa]\s+[^>]*HREF="([^"]+)"[^>]*>([^<]*)</[Aa]>',
            re.IGNORECASE,
        )
        # Find folder names (H3 tags) for tag context
        current_folder = ''
        lines = content.split('\n')

        for line in lines:
            folder_match = re.search(r'<H3[^>]*>([^<]+)</H3>', line, re.IGNORECASE)
            if folder_match:
                current_folder = folder_match.group(1).strip()
                continue

            link_match = link_pattern.search(line)
            if link_match:
                url = link_match.group(1).strip()
                total += 1

                if not url.startswith(('http://', 'https://')):
                    continue

                link = LinkService.get_or_create_link(url)

                if Bookmark.objects.filter(user=user, link=link).exists():
                    skipped += 1
                    continue

                bm = Bookmark.objects.create(
                    user=user,
                    link=link,
                    is_private=True,
                )

                # Use folder as tag
                if current_folder and current_folder.lower() not in ('bookmarks bar', 'bookmarks', 'other bookmarks', 'untagged'):
                    slug = slugify(current_folder, allow_unicode=True)
                    if slug:
                        tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': current_folder})
                        bm.tags.add(tag)

                created += 1

        return {'created': created, 'skipped': skipped, 'total': total}
