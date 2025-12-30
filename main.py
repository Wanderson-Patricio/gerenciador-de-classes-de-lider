from api.src.controllers.github_manager import GithubManager

from dotenv import load_dotenv

load_dotenv()

try:
    with GithubManager() as git:
        try:
            repos = git.get_repos()
            repo = repos[0]
            from pprint import pprint
            pprint(repo.name)
            pprint(repo.description)
            pprint(repo.html_url)
            pprint(repo.id)
        except Exception as e:
            print(f"Erro: {type(e)}")
            print(f"Erro: {e}")

except Exception as e:
    print(f"Erro ao conectar ao GitHub: {type(e)}")
    print(f"Erro ao conectar ao GitHub: {e}")    


