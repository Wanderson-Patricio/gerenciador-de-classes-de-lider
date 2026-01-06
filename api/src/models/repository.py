from dataclasses import dataclass

from github.Repository import Repository

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