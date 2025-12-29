from api.src.controllers.github_manager import GithubManager

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("GITHUB_API_TOKEN")

with GithubManager(token, requested_by_api=True) as git:
    files = git.list_files('gerenciador-de-classes-de-lider')
    file = files[1]
    print(file.path, file.sha)