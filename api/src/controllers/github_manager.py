from typing import Dict, Optional, Type, List
from types import TracebackType

from github import Github
from github.Auth import Token
from github.AuthenticatedUser import AuthenticatedUser
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.ContentFile import ContentFile

from ..errors import TokenMissingError, NotFoundError, AlreadyExistsError

class GithubManager:

    def __init__(self, 
                 token: Optional[str] = None, 
                 requested_by_api: bool = False
            ) -> None:
        
        self._token = self._get_token(token, requested_by_api)
        self._auth: Token = Token(self._token)
        self._git: Github = Github(auth=self._auth)

        
        try:
            self.get_user().login
        except Exception as e:
            raise TokenMissingError("Invalid GitHub API token provided.") from e


    def _get_token(self, 
                   token: Optional[str] = None, 
                   requested_by_api: bool = False
                ) -> str:
        
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
    

    def __enter__(self) -> 'GithubManager':
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
            if exc_type is not None or exc_value is not None or traceback is not None:
                return False  # Propaga a exceção
            return True

    
    def get_user(self) -> AuthenticatedUser:
        return self._git.get_user()
    
    
    def get_repos(self) -> PaginatedList[Repository]:
        user = self.get_user()
        return user.get_repos()
    
    
    def get_repo_by_name(self, repo_name: str) -> Repository:
        try:
            user = self.get_user()
            return user.get_repo(repo_name)
        except:
            raise NotFoundError(resource_type="Repository", resource_identifier=repo_name)
    

    def create_repo( self, 
                    name: str, 
                    description: Optional[str] = None, 
                    private: bool = False, 
                    auto_init: bool = True, 
                    gitignore_template: Optional[str] = "Python", 
                    license_template: Optional[str] = "mit" 
                ) -> Repository: 
        
        """ Cria um novo repositório no GitHub para o usuário autenticado. 
        :param name: Nome do repositório 
        :param description: Descrição do repositório 
        :param private: Define se o repositório será privado (True) ou público (False) 
        :param auto_init: Se True, cria o repositório já com um README.md 
        :param gitignore_template: Template de .gitignore (ex: "Python") 
        :param license_template: Template de licença (ex: "mit") 
        :return: Objeto Repository criado """ 
        user = self.get_user() 
        repo = user.create_repo(name=name, 
                                description=description, 
                                private=private, 
                                auto_init=auto_init, 
                                gitignore_template=gitignore_template, 
                                license_template=license_template) 
        return repo
    
    
    def delete_repo(self, repo_name: str) -> Dict:
        """ Deleta um repositório do GitHub do usuário autenticado. 
        :param repo_name: Nome do repositório a ser deletado 
        """ 
        repo = self.get_repo_by_name(repo_name) 
        repo.delete()
        return {"message": f"Repository '{repo_name}' deleted successfully."}


    def _file_exists(self, 
                            repo_name: str, 
                            path: str, 
                            ref: Optional[str] = "main") -> bool:
        try:
            self.get_file(repo_name, path, ref=ref)
            return True
        except NotFoundError:
            return False
        
    def _branch_exists(self,
                        repo_name: str,
                        branch: str) -> bool:
        
        repo = self.get_repo_by_name(repo_name)
        try:
            repo.get_branch(branch)
            return True
        except:
            return False
    
    def upload_file(self,
                    repo_name: str, 
                    path: str, 
                    content: str, 
                    message: Optional[str] = "Add new file via script", 
                    branch: Optional[str] = 'main'
                ) -> None:
        
        repo = self.get_repo_by_name(repo_name)

        if self._file_exists(repo_name, path, ref=branch):
            raise AlreadyExistsError(resource_type="File", resource_identifier=path)
        
        if not self._branch_exists(repo_name, branch):
            raise NotFoundError(resource_type="Branch", resource_identifier=branch)

        repo.create_file(
            path=path,
            content=content,
            message=message,
            branch=branch
        )
        return self.get_file(repo_name, path, ref=branch)


    def update_file_content(self, 
                    repo_name: str,
                    path: str,
                    new_content: str,
                    sha: str,
                    message: Optional[str] = "Update file via script",
                    branch: Optional[str] = 'main'
                ) -> None:

        repo = self.get_repo_by_name(repo_name)

        if not self._file_exists(repo_name, path, ref=branch):
            raise NotFoundError(resource_type="File", resource_identifier=path)
        
        if not self._branch_exists(repo_name, branch):
            raise NotFoundError(resource_type="Branch", resource_identifier=branch)

        repo.update_file(
            path=path,
            content=new_content,
            message=message,
            sha=sha,
            branch=branch
        )
        return self.get_file(repo_name, path, ref=branch)

    
    def delete_file(self, 
                    repo_name: str,
                    path: str,
                    sha: str,
                    message: Optional[str] = "Delete file via script", 
                    branch: Optional[str] = "main"
                ) -> None:
        
        repo = self.get_repo_by_name(repo_name)

        if not self._file_exists(repo_name, path, ref=branch):
            raise NotFoundError(resource_type="File", resource_identifier=path)
        
        if not self._branch_exists(repo_name, branch):
            raise NotFoundError(resource_type="Branch", resource_identifier=branch)

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
        
        try:
            repo = self.get_repo_by_name(repo_name)
            return repo.get_contents(path=path, ref=ref)
        except:
            raise NotFoundError(resource_type="File", resource_identifier=path)
    
    
    def list_files(self, 
                   repo_name: str, 
                   path: str = "", 
                   ref: str = "main"
                ) -> List[ContentFile]:
        
        """
        Lista todos os arquivos e pastas do repositório de forma recursiva.
        """
        repo = self.get_repo_by_name(repo_name)
        contents = repo.get_contents(path, ref=ref)
        all_files: List[ContentFile] = []

        while contents:
            file_content = contents.pop(0)
            all_files.append(file_content)

            # Se for uma pasta, busca os conteúdos dentro dela
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path, ref=ref))

        return all_files

    
    