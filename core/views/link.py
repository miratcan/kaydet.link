from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import DetailView, ListView

from core.forms.link import BookmarkEditForm, BookmarkForm
from core.models import Bookmark, Link, Tag
from core.services.link import LinkService


class LinkListView(ListView):
    model = Link
    template_name = 'links/list.html'
    context_object_name = 'links'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        username = self.kwargs.get('username')
        ordering = self.request.GET.get('ordering', 'hot')

        tag = None
        saved_by = None

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
        if username:
            saved_by = get_object_or_404(get_user_model(), username=username)

        return LinkService.build_feed(
            user=self.request.user,
            tag=tag,
            saved_by=saved_by,
            ordering=ordering,
            page=self.request.GET.get('page', 1),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordering'] = self.request.GET.get('ordering', 'hot')
        if 'tag_slug' in self.kwargs:
            current_tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
            context['current_tag'] = current_tag
            # Co-occurring tags: tags that appear on bookmarks alongside the current tag
            context['related_tags'] = (
                Tag.objects.filter(
                    bookmarks__tags=current_tag,
                )
                .exclude(pk=current_tag.pk)
                .annotate(co_count=models.Count('bookmarks'))
                .order_by('-co_count')[:10]
            )
        if 'username' in self.kwargs:
            profile_user = get_object_or_404(
                get_user_model(), username=self.kwargs.get('username'),
            )
            context['profile_user'] = profile_user
            context['profile_bookmark_count'] = Bookmark.objects.filter(
                user=profile_user, is_private=False,
            ).count()
            context['profile_top_tags'] = (
                Tag.objects.filter(
                    bookmarks__user=profile_user,
                    bookmarks__is_private=False,
                )
                .annotate(usage_count=models.Count('bookmarks'))
                .order_by('-usage_count')[:5]
            )

        # Sidebar stats and tags for authenticated users
        user = self.request.user
        if user.is_authenticated:
            from datetime import timedelta

            from django.utils import timezone
            now = timezone.now()
            user_bookmarks = Bookmark.objects.filter(user=user)
            context['user_stats'] = {
                'total': user_bookmarks.count(),
                'this_week': user_bookmarks.filter(
                    created_at__gte=now - timedelta(days=7),
                ).count(),
            }
            context['user_top_tags'] = (
                Tag.objects.filter(bookmarks__user=user)
                .annotate(usage_count=models.Count('bookmarks'))
                .order_by('-usage_count')[:15]
            )

        return context

    def get_paginate_by(self, queryset):
        return None


class LinkDetailView(DetailView):
    model = Link
    template_name = 'links/detail.html'
    context_object_name = 'link'

    def get_queryset(self):
        from django.db.models import Exists, IntegerField, OuterRef, Subquery, Value

        from core.models import Bookmark

        qs = Link.objects.prefetch_related('bookmarks__user', 'bookmarks__tags', 'comments__posted_by')

        user = self.request.user
        if user.is_authenticated:
            qs = qs.annotate(
                is_saved=Exists(Bookmark.objects.filter(user=user, link=OuterRef('pk'))),
                user_bookmark_id=Subquery(Bookmark.objects.filter(user=user, link=OuterRef('pk')).values('pk')[:1]),
            )
        else:
            qs = qs.annotate(
                is_saved=Value(False),
                user_bookmark_id=Value(None, output_field=IntegerField()),
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.forms.comment import CommentForm

        context['comment_form'] = CommentForm()
        bookmarks = self.object.bookmarks.select_related('user').prefetch_related('tags').order_by('-created_at')
        user = self.request.user
        if user.is_authenticated:
            bookmarks = bookmarks.filter(
                models.Q(is_private=False) | models.Q(user=user),
            )
        else:
            bookmarks = bookmarks.filter(is_private=False)
        context['bookmarks'] = bookmarks

        # Related links: links that share tags with this link
        link_tags = Tag.objects.filter(bookmarks__link=self.object)
        context['related_links'] = (
            Link.objects.filter(bookmark__tags__in=link_tags)
            .exclude(pk=self.object.pk)
            .annotate(shared_tags=models.Count('bookmark__tags'))
            .order_by('-shared_tags', '-save_count')
            .distinct()[:6]
        )
        return context


class BookmarkCreateView(LoginRequiredMixin, View):
    template = 'links/bookmark_form.html'

    def get(self, request):
        parent_id = request.GET.get('from')
        form = BookmarkForm(user=request.user)
        parent = None

        if parent_id:
            parent = Bookmark.objects.filter(pk=parent_id).select_related('link').prefetch_related('tags').first()
            if parent:
                form = BookmarkForm(initial={
                    'url': parent.link.url,
                    'note': parent.note,
                    'tag_names': ', '.join(parent.tags.values_list('name', flat=True)),
                }, user=request.user)

        return TemplateResponse(request, self.template, self._context(form, parent))

    def post(self, request):
        parent_id = request.POST.get('parent_id')
        parent = None
        if parent_id:
            parent = Bookmark.objects.filter(pk=parent_id).select_related('link').first()

        form = BookmarkForm(request.POST, user=request.user)
        if form.is_valid():
            bookmark = form.save(user=request.user, parent=parent)
            return redirect(bookmark.link.get_absolute_url())
        return TemplateResponse(request, self.template, self._context(form, parent))

    def _context(self, form, parent):
        from django.utils.translation import gettext as _

        user_tags = Tag.objects.filter(
            bookmarks__user=self.request.user,
        ).annotate(
            usage_count=models.Count('bookmarks'),
        ).order_by('-usage_count')[:20]

        return {
            'form': form,
            'parent': parent,
            'link': parent.link if parent else None,
            'show_url': parent is None,
            'page_title': _('Save a Link'),
            'user_tags': user_tags,
        }


class BookmarkEditView(LoginRequiredMixin, View):
    template = 'links/bookmark_form.html'

    def get(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        form = BookmarkEditForm(instance=bookmark)
        return TemplateResponse(request, self.template, self._context(form, bookmark))

    def post(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        form = BookmarkEditForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return redirect(bookmark.link.get_absolute_url())
        return TemplateResponse(request, self.template, self._context(form, bookmark))

    def _context(self, form, bookmark):
        from django.utils.translation import gettext as _

        user_tags = Tag.objects.filter(
            bookmarks__user=self.request.user,
        ).annotate(
            usage_count=models.Count('bookmarks'),
        ).order_by('-usage_count')[:20]

        return {
            'form': form,
            'link': bookmark.link,
            'bookmark': bookmark,
            'show_url': False,
            'page_title': _('Edit Bookmark'),
            'user_tags': user_tags,
        }


class BookmarkDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        bookmark = get_object_or_404(Bookmark, pk=pk)
        if bookmark.user != request.user:
            return HttpResponseForbidden()
        bookmark.delete()
        return redirect('link-list')


class RandomLinkView(View):
    def get(self, request):
        if request.user.is_authenticated:
            bookmark = Bookmark.objects.filter(user=request.user).select_related('link').order_by('?').first()
            if bookmark:
                return redirect(bookmark.link.get_absolute_url())
        link = Link.objects.order_by('?').first()
        if link:
            return redirect(link.get_absolute_url())
        return redirect('link-list')


class FetchUrlInfoView(LoginRequiredMixin, View):
    def get(self, request):
        url = request.GET.get('url', '')
        if not url:
            if request.htmx:
                return HttpResponse('<div id="url-preview"></div>')
            return JsonResponse({})
        try:
            result = LinkService.scrape_url(url)
        except Exception:
            if request.htmx:
                return HttpResponse('<div id="url-preview"></div>')
            return JsonResponse({})

        if request.htmx:
            metadata = result.get('metadata', {})
            context = {
                'info': {
                    'metadata': metadata,
                    'title': metadata.get('og:title', ''),
                    'description': metadata.get('og:description', ''),
                    'image': metadata.get('og:image', ''),
                },
            }
            return TemplateResponse(request, 'links/partials/url_preview.html', context)
        return JsonResponse(result)
