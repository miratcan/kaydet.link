class AppError(Exception):
    def __init__(self, message, humans=False, **extras):
        if humans:
            message = message.title()
        super().__init__(message)
        self.humans = humans
        self.message = message
        self.extras = extras


class LinkServiceError(AppError):
    ...


class BookmarkServiceError(AppError):
    ...


class NotificationServiceError(AppError):
    ...


class DigestServiceError(AppError):
    ...
