from dataclasses import dataclass

from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.ContentFile import ContentFile

@dataclass(frozen=True)
class RepositoryData:
    id: int
    name: str
    description: str
    html_url: str

    def from_repository(repo: Repository):
        return RepositoryData(
            repo.id,
            repo.name,
            repo.description,
            repo.html_url
        )

@dataclass(frozen=True)
class RepositoryCreate:
    pass


@dataclass(frozen=True)
class RepositoryUpdate:
    pass


@dataclass(frozen=True)
class RepositoryDelete:
    pass