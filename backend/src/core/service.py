from typing import Generic, TypeVar

RepoType = TypeVar("RepoType")


class BaseService(Generic[RepoType]):

    def __init__(self, repository: RepoType):
        self.repository = repository
