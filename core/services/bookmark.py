import logging

from core.services.link import LinkService

logger = logging.getLogger('core.BookmarkService')


class BookmarkService:

    @staticmethod
    def create_bookmark(user, url, note='', tags=None, parent=None):
        from core.models import Bookmark

        link = LinkService.get_or_create_link(url)

        existing = Bookmark.objects.filter(user=user, link=link).first()
        if existing:
            existing.note = note
            existing.save(update_fields=['note'])
            if tags:
                existing.tags.set(tags)
            return existing

        bookmark = Bookmark.objects.create(
            user=user,
            link=link,
            parent=parent,
            note=note,
        )
        if tags:
            bookmark.tags.set(tags)
        return bookmark

    @staticmethod
    def save_from(user, parent_bookmark):
        from core.models import Bookmark

        existing = Bookmark.objects.filter(user=user, link=parent_bookmark.link).first()
        if existing:
            return existing

        bookmark = Bookmark.objects.create(
            user=user,
            link=parent_bookmark.link,
            parent=parent_bookmark,
            note=parent_bookmark.note,
        )
        bookmark.tags.set(parent_bookmark.tags.all())
        return bookmark

    @staticmethod
    def is_saved(user, link):
        if not user.is_authenticated:
            return False
        from core.models import Bookmark

        return Bookmark.objects.filter(user=user, link=link).exists()

    @staticmethod
    def delete_bookmark(user, bookmark):
        if bookmark.user != user:
            return False
        bookmark.delete()
        return True
