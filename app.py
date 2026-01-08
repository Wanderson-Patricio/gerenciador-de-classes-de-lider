from flask import Flask, redirect, request, render_template, jsonify, url_for
from api.src.errors import BadRequestError, GithubError, AlreadyExistsError


from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

API_URL = 'http://localhost:3000/api'
HEADERS = {
    'x-api-token': os.getenv('GITHUB_API_TOKEN')
}


app = Flask(__name__, 
            template_folder='app/templates', 
            static_folder='app/static')



@app.route("/")
@app.route("/index")
def index():
    token = os.getenv("GITHUB_API_TOKEN", "")
    if not token:
        return render_template('register_token.html', page_info={"title": "Registrar Token"})
    
    page_info = {
        "title": "Gerenciador de Classes de Líder"
    }

    return render_template('index.html', page_info=page_info, github_token=token)


@app.route("/register-token")
def register_token():
    page_info = {
        "title": "Registrar Token"
    }

    return render_template('register_token.html', page_info=page_info)


@app.route("/create-new-class")
def create_new_class():
    page_info = {
        "title": "Criar Nova Classe",
        "logo": "Criação de Nova Classe"
    }

    return render_template('create_new_class.html', page_info=page_info)


def create_github_repo(repo_name: str, description: str = ""):
    url = f"{API_URL}/repositories" 
    payload = {
        "name": repo_name,
        "description": description
    }
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 201:
        return response.json()
    else:
        raise AlreadyExistsError(resource_type="Repositório", resource_identifier=repo_name)


def upload_file_in_repo(repo_name, file, path_in_repo):
    files = {
        "file": (file.filename, file, "application/octet-stream")
    }
    data = {
        "path": path_in_repo,
        "message": f"Add {file.filename} via script"             # Opcional
    }

    api_url_post = f'{API_URL}/repositories/{repo_name}/files'
    res = requests.post(api_url_post, headers=HEADERS, files=files, data=data)

    if res.status_code == 201:
        return res.json()
    else:
        raise GithubError(f"Erro ao criar repositório: {res.status_code} - {res.text}", 500)


def create_requirement_file(repo_name, group_id, group_name, id, requirement):
    path_in_repo = f'{group_id} - {group_name}/{str(id).zfill(2)} - {requirement.get("requirementDescription")}/conclusion.json'
    content = json.dumps(requirement.get("conclusion")).encode('utf-8')
    files = {
        "file": ('conclusion.json', content, "application/json")
    }
    data = {
        "path": path_in_repo,
        "message": f"Add conclusion.json for requirement {id} via script" 
    }

    api_url_post = f'{API_URL}/repositories/{repo_name}/files'
    res = requests.post(api_url_post, headers=HEADERS, files=files, data=data)

    if res.status_code == 201:
        return res.json()
    else:
        raise GithubError(f"Erro ao criar repositório: {res.status_code} - {res.text}", 500)

@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        # Verifica se o arquivo faz parte da requisição
        if 'file' not in request.files:
            raise BadRequestError("Nenhum arquivo foi enviado na requisição.")
        
        file = request.files['file']

        if not file or file.filename == '':
            raise BadRequestError("Nenhum arquivo foi enviado na requisição.")

        try:
            content = file.read()
            data = json.loads(content.decode("utf-8"))
            file.seek(0)


            info = data.get('info')
            repo_name = info.get('name')
            repo_description = info.get('description', '')
            create_github_repo(repo_name, repo_description)
            upload_file_in_repo(repo_name, file, 'requirements.json')


            # 1. Cria um dicionário para busca rápida: {id: nome}
            # Isso transforma uma busca lenta (O(n)) em uma busca instantânea (O(1))
            grupos_map = {g.get('groupId'): g.get('groupName') for g in data.get('groups', [])}
            requirements = data.get('requirements', [])

            # for req in requirements:
            #     req_id = req.get("requirementId")
            #     group_id = req.get("groupId")
                
            #     # Busca o nome no mapa. Se não existir, retorna "Não encontrado" (ou None)
            #     group_name = grupos_map.get(group_id, "Grupo não encontrado")
                
            #     create_requirement_file(repo_name, group_id, group_name, req_id, req)

        except json.JSONDecodeError as e:
            raise BadRequestError("O arquivo enviado não é um JSON válido. Erro: " + str(e))

    return redirect(url_for('index'))
