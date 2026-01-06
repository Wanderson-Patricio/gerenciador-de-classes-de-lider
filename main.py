import base64
from dotenv import load_dotenv
import requests
import os

load_dotenv()


API_URL = "http://localhost:3000/api"
HEADERS = {
    'x-api-token': os.getenv("GITHUB_API_TOKEN", "")

}

params = {
    "branch": "main"
}

filename = "README.md"
path_in_repo = f"pasta/arquivos/{filename}"


with open(filename, "rb") as f:
    files = {
        "file": (filename, f, "application/octet-stream")
    }
    data = {
        "message": f"Updated {filename} via script"             # Opcional
    }

    api_url_post = f'{API_URL}/repositories/Classe-de-Lider-de-Aventureiros/files/{path_in_repo}'
    res = requests.put(api_url_post, params=params, headers=HEADERS, files=files, data=data)


print(res.status_code)
try:
    print(res.json())
except Exception:
    print(res.text)