import base64
from dotenv import load_dotenv
import requests
import os

load_dotenv()


API_URL = "http://localhost:3000/api/repositories/teste-de-repositorio/files"
TOKEN = os.getenv("GITHUB_API_TOKEN", "")

# Se precisar escolher outra branch, passe via query string: ?branch=develop
params = {
    "branch": "main"
}


filename = "Análise de Dados com Python Utilizando o CHATGPT como assistente.pdf"
path_in_repo = f"{filename}"

headers = {
    "x-api-token": TOKEN
}



with open(filename, "rb") as f:
    files = {
        # campo "file" deve bater com o que sua rota Flask espera: request.files.get('file')
        "file": (filename, f, "application/octet-stream")
    }
    data = {
        "path": path_in_repo,
        "message": f"Add {filename} via script"
    }

    resp = requests.post(API_URL, params=params, headers=headers, files=files, data=data)




print(resp.status_code)
from pprint import pprint
try:
    pprint(resp.json())
except Exception:
    print(resp.text)

