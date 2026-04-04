from django.conf import settings


def site_name(request):
    return {'site_name': settings.SITE_NAME}


def wiki_has_pages(request):
    from core.models import Page

    return {'wiki_has_pages': Page.objects.filter(is_listed=True).exists()}
