from django.urls import path, re_path

from core.views.comment import CommentCreateView, CommentDeleteView, CommentUpdateView
from core.views.link import (
    BookmarkCreateView,
    BookmarkDeleteView,
    BookmarkEditView,
    FetchUrlInfoView,
    LinkDetailView,
    LinkListView,
    RandomLinkView,
)
from core.views.notification import NotificationListView
from core.views.preferences import PreferencesUpdateView
from core.views.tag import TagListView
from core.views.wiki import WikiEditView, WikiIndexView, WikiPageView

urlpatterns = [
    # feed
    path('', LinkListView.as_view(), name='link-list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', LinkListView.as_view(), name='link-list-by-tag'),
    path('user/<str:username>/', LinkListView.as_view(), name='link-list-by-user'),

    # links
    path('links/random/', RandomLinkView.as_view(), name='link-random'),
    path('links/<int:pk>/', LinkDetailView.as_view(), name='link-detail'),

    # bookmarks
    path('bookmarks/new/', BookmarkCreateView.as_view(), name='bookmark-create'),
    path('bookmarks/<int:pk>/edit/', BookmarkEditView.as_view(), name='bookmark-edit'),
    path('bookmarks/<int:pk>/delete/', BookmarkDeleteView.as_view(), name='bookmark-delete'),

    # tags
    path('tags/', TagListView.as_view(), name='tag-list'),

    # comments
    path('comments/<int:link_pk>/submit/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # api (htmx)
    path('api/fetch-url/', FetchUrlInfoView.as_view(), name='fetch-url-info'),

    # notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # preferences
    path('preferences/', PreferencesUpdateView.as_view(), name='preferences'),

    # wiki
    path('wiki/', WikiIndexView.as_view(), name='wiki-index'),
    re_path(r'^wiki/(?P<slug>[-\w]+)/$', WikiPageView.as_view(), name='wiki-page'),
    re_path(r'^wiki/(?P<slug>[-\w]+)/edit/$', WikiEditView.as_view(), name='wiki-edit'),

]
