# GitHub Integration API

Esta API foi desenvolvida para intermediar e simplificar a interação com o ecossistema do GitHub. Utilizando a biblioteca **PyGitHub**, ela abstrai a complexidade da API REST oficial do GitHub, permitindo o gerenciamento programático de repositórios e seus conteúdos.

## 🚀 Funcionalidades Principais

A API oferece suporte completo ao ciclo de vida de ativos no GitHub através de operações **CRUD** (Create, Read, Update, Delete):

### 1. Gerenciamento de Repositórios

Permite o controle administrativo sobre a conta do usuário ou organização, incluindo:

* **Criação:** Instanciar novos repositórios públicos ou privados.
* **Leitura:** Consultar metadados, configurações e listar repositórios existentes.
* **Atualização:** Editar descrições, nomes e configurações de visibilidade.
* **Deleção:** Remoção definitiva de repositórios.

### 2. Manipulação de Arquivos e Conteúdo

A atualização de um repositório é realizada através da gestão direta de seus arquivos. Os endpoints permitem:

* **Upload/Criação:** Adicionar novos arquivos a ramos (*branches*) específicos.
* **Consulta:** Recuperar o conteúdo ou metadados de arquivos existentes.
* **Edição:** Sobrescrever conteúdos e realizar commits programáticos.
* **Exclusão:** Remover arquivos da árvore de diretórios do repositório.

---

## 🔐 Autenticação e Segurança

Para garantir a segurança e o acesso aos recursos, a API utiliza o protocolo de autorização do GitHub.

* **Requisito:** É obrigatório o uso de um **Personal Access Token (PAT)**.
* **Como obter:** O token deve ser gerado nas configurações de desenvolvedor da conta GitHub (Settings > Developer Settings > Personal Access Tokens).
* **Escopo:** Certifique-se de que o token possua as permissões de `repo` para operar repositórios privados e realizar commits.

> :exclamation: :exclamation: :exclamation:
> O token deve ser enviado no cabeçalho (*header*) de cada requisição para validar a identidade do usuário e as permissões de escrita/leitura.

---

## 🛠 Arquitetura dos Endpoints

A estrutura de rotas foi projetada de forma semântica, utilizando o repositório como recurso base para todas as operações subsequentes.

| Recurso | Método | Descrição |
| --- | --- | --- |
| `/repositories` | $\color{green}{\text{GET}}$ | Lista todos os repositórios. |
| `/repositories` | $\color{yellow}{\text{POST}}$ | Cria um novo repositório. |
| `/repositories/{repo_name}` | $\color{green}{\text{GET}}$ | Retorna detalhes de um repositório específico. |
| `/repositories/{repo_name}` | $\color{magenta}{\text{PATCH}}$ | Atualiza a descrição do repositório. |
| `/repositories/{repo_name}` | $\color{red}{\text{DELETE}}$ | Deleta um repositório específico. |
| `/repositories/{repo_name}/files` | $\color{green}{\text{GET}}$ | Lista todos os arquivos em um repositório específico. |
| `/repositories/{repo_name}/files` | $\color{yellow}{\text{POST}}$ | Cria um novo arquivo dentro de um repositório específico. |
| `/repositories/{repo_name}/files/{path}` | $\color{green}{\text{GET}}$ | Retorna as informações de um arquivo específico dentro de um repositório |
| `/repositories/{repo_name}/files/{path}` | $\color{magenta}{\text{PUT}}$ | Cria ou atualiza um arquivo no caminho especificado. |
| `/repositories/{repo_name}/files/{path}` | $\color{red}{\text{DELETE}}$ | Remove um arquivo do repositório. |

---

Será demonstrado abaixo como utilizar a API através da biblioteca requests em python.

## Configurações iniciais

Crie um arquivo .env na pasta raíz do projeto e escreva a seguinte variável de ambiente:

```
GITHUB_API_TOKEN='seu token de API'
```

Defina as seguintes importações e constantes no início do seu arquivo.

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env', override=True)

API_URL = 'http://localhost:3000/api'
HEADERS = {
    'x-api-token': os.getenv('GITHUB_API_TOKEN')
}
``` 

## Utilização das Rotas

- **Repositories**

    1. `GET` /repositories

    ```python
    data = requests.get(
        f'{API_URL}/repositories',
        headers=HEADERS
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    [
        {
            "description": string,
            "html_url": string,
            "id": int,
            "name": string
        }, ...
    ]
    ```
    
    2. `GET` /repositories/{repo_name}

    ```python
    data = requests.get(
        f'{API_URL}/repositories/teste-de-repositorio',
        headers=HEADERS
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    {
        "description": string,
        "html_url": string,
        "id": int,
        "name": string
    }
    ```
    
    3. `POST` /repositories

    ```python
    data = requests.post(
        f'{API_URL}/repositories',
        headers=HEADERS,
        json={
            'name': 'teste-de-repositorio',
            'description': 'Descrição do repositório de teste', #Opcional
            'private': False,                                   #Opcional
            'auto_init': True,                                  #Opcional
            'gitignore_template': 'Python',                     #Opcional
            'license_template': 'mit'                           #Opcional
        }
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    {
        "description": string,
        "html_url": string,
        "id": int,
        "name": string
    }
    ```

    4. `PATCH` /repositories/{repo_name}

    ```python
    data = requests.patch(
        f'{API_URL}/repositories/teste-de-repositorio',
        headers=HEADERS,
        json={
            'description': 'Updated description'
        }
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    {
        "description": string,
        "html_url": string,
        "id": int,
        "name": string
    }
    ```
    
    5. `DELETE` /repositories/{repo_name}

    ```python
    data = requests.delete(
        f'{API_URL}/repositories/teste-de-repositorio',
        headers=HEADERS
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    {
        "message": string
    }
    ```

- **Files**

    1. `GET` /repositories/{repo_name}/files

    ```python
    # Se precisar escolher outra branch, passe via query string: ?branch=develop
    params = {
        "branch": "main"
    }

    data = requests.get(
        f'{API_URL}/repositories/teste-de-repositorio/files',
        headers=HEADERS,
        params=params
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    [
        {
            "path": string
            "name": string
            "html_url": string
            "sha": string
            "download_url": string
            "content": string
            "repository_name": string
            "language": string
            "type": string
        }
    ]
    ```
    
    2. `GET` /repositories/{repo_name}/files/{path}

    ```python
    # Se precisar escolher outra branch, passe via query string: ?branch=develop
    params = {
        "branch": "main"
    }

    data = requests.get(
        f'{API_URL}/repositories/teste-de-repositorio/files/README.md',
        headers=HEADERS,
        params=params
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    {
        "path": string
        "name": string
        "html_url": string
        "sha": string
        "download_url": string
        "content": string
        "repository_name": string
        "language": string
        "type": string
    }
    ```
    
    3. `POST` /repositories/{repo_name}/files

    ```python
    # Se precisar escolher outra branch, passe via query string: ?branch=develop
    params = {
        "branch": "main"
    }

    filename = "teste.pdf"
    path_in_repo = f"pasta/arquivos/{filename}"


    with open(filename, "rb") as f:
        files = {
            "file": (filename, f, "application/octet-stream")
        }
        data = {
            "path": path_in_repo,
            "message": f"Add {filename} via script"             # Opcional
        }

        api_url_post = f'{API_URL}/repositories/teste-de-repositorio/files'
        res = requests.post(api_url_post, params=params, headers=HEADERS, files=files, data=data)


    print(res.status_code)
    try:
        print(res.json())
    except Exception:
        print(res.text)
    ``` 

    Retorno Esperado

    ```js
    {
        "path": string
        "name": string
        "html_url": string
        "sha": string
        "download_url": string
        "content": string
        "repository_name": string
        "language": string
        "type": string
    }
    ```

    4. `PUT` /repositories/{repo_name}/files/{path}

    ```python
    # Se precisar escolher outra branch, passe via query string: ?branch=develop
    params = {
        "branch": "main"
    }

    filename = "teste_novo.pdf"
    path_in_repo = f"pasta/arquivos/{filename}"


    with open(filename, "rb") as f:
        files = {
            "file": (filename, f, "application/octet-stream")
        }
        data = {
            "message": f"Updated {filename} via script"             # Opcional
        }

        api_url_post = f'{API_URL}/repositories/teste-de-repositorio/files/{path_in_repo}'
        res = requests.post(api_url_post, params=params, headers=HEADERS, files=files, data=data)


    print(res.status_code)
    try:
        print(res.json())
    except Exception:
        print(res.text)
    ``` 

    Retorno Esperado

    ```js
    {
        "path": string
        "name": string
        "html_url": string
        "sha": string
        "download_url": string
        "content": string
        "repository_name": string
        "language": string
        "type": string
    }
    ```

    5. `DELETE` /repositories/{repo_name}/files/{path}

    ```python
    # Se precisar escolher outra branch, passe via query string: ?branch=develop
    params = {
        "branch": "main"
    }

    data = requests.delete(
        f'{API_URL}/repositories/teste-de-repositorio/files/README.md',
        headers=HEADERS.
        params=params,
        json={
            'message': 'deleted file via script'        # Opcional
        }
    )

    print(data.status_code)
    print(data.json())
    ``` 

    Retorno Esperado

    ```js
    {
        "message": string
    }
    ```