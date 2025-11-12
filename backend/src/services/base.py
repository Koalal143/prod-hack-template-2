from typing import Generic, TypeVar

RepoType = TypeVar("RepoType")


class BaseService(Generic[RepoType]):
    def __init__(self, repository: RepoType) -> None:
        self.repository = repository
