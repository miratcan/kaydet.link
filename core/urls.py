from django.urls import path

from core.views.auth.login import LoginView, LogoutView
from core.views.auth.register import RegisterView
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
    path('tag/<slug:tag_slug>/', LinkListView.as_view(), name='link-list-by-tag'),
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
    path('wiki/<slug:slug>/', WikiPageView.as_view(), name='wiki-page'),
    path('wiki/<slug:slug>/edit/', WikiEditView.as_view(), name='wiki-edit'),

    # auth
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
]
