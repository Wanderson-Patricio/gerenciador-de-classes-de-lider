from typing import Optional, Type, List
from types import TracebackType
from github import Github
from github.Auth import Token
from github.AuthenticatedUser import AuthenticatedUser
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.ContentFile import ContentFile

from ..errors.github_exceptions import TokenMissingError

class GithubManager:
    def __init__(self, token: Optional[str] = None, requested_by_api: bool = False):
        self._token = self._get_token(token, requested_by_api)
        self._auth: Token = Token(self._token)
        self._git: Github = Github(auth=self._auth)

    def _get_token(self, token: Optional[str] = None, requested_by_api: bool = False) -> str:
        if token:
            return token
        
        if requested_by_api:
            raise TokenMissingError("GitHub API token must be provided when requested by API.")
        
        import os
        env_token = os.getenv("GITHUB_API_TOKEN")
        if env_token:
            return env_token
        
        from getpass import getpass
        prompt_token = getpass("Enter your GitHub API token: ")
        if prompt_token and prompt_token.strip() and prompt_token != "":
            return prompt_token
        
        raise TokenMissingError("GitHub API token must be provided either as an argument or via the GITHUB_API_TOKEN environment variable.")
    
    def __enter__(self):
        return self
    
    def __exit__(
        self, 
        exc_type: Optional[Type[BaseException]], 
        exc_value: Optional[BaseException], 
        traceback: Optional[TracebackType]
    ) -> None:
        """
        Fecha a conexão com o GitHub de forma segura.
        """
        try:
            self._git.close()
        finally:
            pass

    def get_user(self) -> AuthenticatedUser:
        return self._git.get_user()
    
    def get_repos(self) -> PaginatedList[Repository]:
        user = self.get_user()
        return user.get_repos()
    
    def get_repo_by_name(self, repo_name: str) -> Repository:
        user = self.get_user()
        return user.get_repo(repo_name)
    
    def upload_file(self,
                    repo_name: str, 
                    path: str, 
                    content: str, 
                    message: str, 
                    branch: Optional[str] = 'main'
                ) -> None:
        
        repo = self.get_repo_by_name(repo_name)
        repo.create_file(
            path=path,
            content=content,
            message=message,
            branch=branch
        )

    def delete_file(self, 
                    repo_name, 
                    path, 
                    message, 
                    sha, 
                    branch="main"
                ) -> None:
        
        repo = self.get_repo_by_name(repo_name)
        repo.delete_file(
            path=path, 
            message=message, 
            sha=sha, 
            branch=branch
        )

    def get_file(self, 
                 repo_name: str, 
                 path: str, 
                 ref: Optional[str] = "main"
            ) -> ContentFile:
        
        repo = self.get_repo_by_name(repo_name)
        return repo.get_contents(path=path, ref=ref)
    
    def list_files(self, 
                   repo_name: str, 
                   ref: Optional[str] = "main"
                ) -> List[ContentFile]:
        
        return self.get_file(repo_name=repo_name, path="", ref=ref)