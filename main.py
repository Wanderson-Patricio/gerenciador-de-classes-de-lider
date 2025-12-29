from api.src.controllers.github_manager import GithubManager

from dotenv import load_dotenv
import os

load_dotenv()

try:
    with GithubManager() as git:
        try:
            git.upload_file(
                repo_name="gerenciador-de-classes-de-lider",
                path="README.md",
                content="# Gerenciador de Classes de Líder\nEste repositório contém o código"
            )
        except Exception as e:
            print(f"Erro: {type(e)}")
            print(f"Erro: {e}")

except Exception as e:
    print(f"Erro ao conectar ao GitHub: {type(e)}")
    print(f"Erro ao conectar ao GitHub: {e}")    