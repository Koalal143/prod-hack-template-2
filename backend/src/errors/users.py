from core.error import ApplicationError


class UserWithEmailAlreadyExistsError(ApplicationError):
    pass


class UserNotFoundError(ApplicationError):
    pass


class UserPasswordIsIncorrectError(ApplicationError):
    pass
