class ApplicationError(Exception):
    pass


class NotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass


class AccessError(ApplicationError):
    pass


class BadRequestError(ApplicationError):
    pass
