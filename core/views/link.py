from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
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
            context['current_tag'] = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
        if 'username' in self.kwargs:
            context['profile_user'] = get_object_or_404(
                get_user_model(), username=self.kwargs.get('username'),
            )
        return context

    def get_paginate_by(self, queryset):
        return None


class LinkDetailView(DetailView):
    model = Link
    template_name = 'links/detail.html'
    context_object_name = 'link'

    def get_queryset(self):
        return Link.objects.prefetch_related('bookmarks__user', 'bookmarks__tags', 'comments__posted_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.forms.comment import CommentForm
        from core.services.bookmark import BookmarkService

        context['comment_form'] = CommentForm()
        context['bookmarks'] = self.object.bookmarks.select_related('user').prefetch_related('tags').order_by('-created_at')
        context['is_saved'] = BookmarkService.is_saved(self.request.user, self.object)
        return context


class BookmarkCreateView(LoginRequiredMixin, View):
    template = 'links/bookmark_form.html'

    def get(self, request):
        parent_id = request.GET.get('from')
        form = BookmarkForm()
        parent = None

        if parent_id:
            parent = Bookmark.objects.filter(pk=parent_id).select_related('link').prefetch_related('tags').first()
            if parent:
                form = BookmarkForm(initial={
                    'url': parent.link.url,
                    'note': parent.note,
                    'tag_names': ', '.join(parent.tags.values_list('name', flat=True)),
                })

        return TemplateResponse(request, self.template, self._context(form, parent))

    def post(self, request):
        parent_id = request.POST.get('parent_id')
        parent = None
        if parent_id:
            parent = Bookmark.objects.filter(pk=parent_id).select_related('link').first()

        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(user=request.user, parent=parent)
            return redirect(bookmark.link.get_absolute_url())
        return TemplateResponse(request, self.template, self._context(form, parent))

    def _context(self, form, parent):
        from django.utils.translation import gettext as _

        return {
            'form': form,
            'parent': parent,
            'link': parent.link if parent else None,
            'show_url': parent is None,
            'page_title': _('Save a Link'),
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

        return {
            'form': form,
            'link': bookmark.link,
            'bookmark': bookmark,
            'show_url': False,
            'page_title': _('Edit Bookmark'),
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
