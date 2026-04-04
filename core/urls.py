from django.urls import path, re_path

from core.views.collection import (
    CollectionAddBookmarkView,
    CollectionCreateView,
    CollectionDeleteView,
    CollectionDetailView,
    CollectionEditView,
    CollectionListView,
)
from core.views.bookmark_list import BookmarkListView
from core.views.bookmark_status import BookmarkPinToggleView, BookmarkStatusSetView, BookmarkStatusToggleView
from core.views.comment import CommentCreateView, CommentDeleteView, CommentUpdateView
from core.views.data import ExportCSVView, ExportHTMLView, ExportJSONView, ExportView, ImportView
from core.views.dashboard import DashboardRediscoverView, DashboardView, HomeRedirectView
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
from core.views.search import SearchView
from core.views.preferences import PreferencesUpdateView
from core.views.tag import TagListView
from core.views.wiki import WikiEditView, WikiIndexView, WikiPageView

urlpatterns = [
    # home — redirects to dashboard or explore
    path('', HomeRedirectView.as_view(), name='home'),

    # dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/rediscover/', DashboardRediscoverView.as_view(), name='dashboard-rediscover'),

    # feed (explore)
    path('explore/', LinkListView.as_view(), name='link-list'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', LinkListView.as_view(), name='link-list-by-tag'),
    path('user/<str:username>/', LinkListView.as_view(), name='link-list-by-user'),

    # links
    path('links/random/', RandomLinkView.as_view(), name='link-random'),
    path('links/<int:pk>/', LinkDetailView.as_view(), name='link-detail'),

    # bookmarks
    path('bookmarks/', BookmarkListView.as_view(), name='bookmark-list'),
    path('bookmarks/new/', BookmarkCreateView.as_view(), name='bookmark-create'),
    path('bookmarks/<int:pk>/edit/', BookmarkEditView.as_view(), name='bookmark-edit'),
    path('bookmarks/<int:pk>/delete/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
    path('bookmarks/<int:pk>/status/', BookmarkStatusToggleView.as_view(), name='bookmark-status-toggle'),
    path('bookmarks/<int:pk>/status/<str:status>/', BookmarkStatusSetView.as_view(), name='bookmark-status-set'),
    path('bookmarks/<int:pk>/pin/', BookmarkPinToggleView.as_view(), name='bookmark-pin-toggle'),

    # collections
    path('collections/', CollectionListView.as_view(), name='collection-list'),
    path('collections/new/', CollectionCreateView.as_view(), name='collection-create'),
    path('collections/<str:slug>/edit/', CollectionEditView.as_view(), name='collection-edit'),
    path('collections/<str:slug>/delete/', CollectionDeleteView.as_view(), name='collection-delete'),
    path('collections/<str:username>/<str:slug>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('collections/<int:collection_pk>/toggle/<int:bookmark_pk>/', CollectionAddBookmarkView.as_view(), name='collection-toggle-bookmark'),

    # data
    path('settings/export/', ExportView.as_view(), name='export'),
    path('settings/export/json/', ExportJSONView.as_view(), name='export-json'),
    path('settings/export/html/', ExportHTMLView.as_view(), name='export-html'),
    path('settings/export/csv/', ExportCSVView.as_view(), name='export-csv'),
    path('settings/import/', ImportView.as_view(), name='import'),

    # search
    path('search/', SearchView.as_view(), name='search'),

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
