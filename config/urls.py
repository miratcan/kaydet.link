from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('yonetim-f0f0992c/', admin.site.urls),
    path('auth/', include('allauth.urls')),
    path('', include('core.urls')),
]
