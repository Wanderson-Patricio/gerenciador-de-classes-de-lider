from flask import Blueprint, jsonify, request, g
from github.GithubException import GithubException
import base64

from ..models import RepositoryData, ContentFileData
from ..controllers import GithubController
from ..errors import GithubError, BadRequestError
from .token_required import token_required

# Criar um Blueprint para rotas de repositórios
repos_bp = Blueprint("repositories", __name__)


@repos_bp.errorhandler(GithubError)
def handle_github_exception(e):
    return jsonify(e.send_error()), e.status_code

@repos_bp.errorhandler(GithubException)
def handle_github_exception(e):
    args = e.args[1]
    return jsonify(
        {
            'message': args.get('message'),
            'status_code': args.get('status')
        }
    ), e.args[0]


@repos_bp.route("/", methods=["GET"])
@token_required
def list_repos():
    with GithubController(g.token, True) as git:
        repos = git.get_repos()
        return jsonify(
            [RepositoryData.from_repository(repo) for repo in repos]
        ), 200


@repos_bp.route("/<string:repo_name>", methods=["GET"])
@token_required
def get_repo(repo_name: str):
    with GithubController(g.token, True) as git:
        repo = git.get_repo_by_name(repo_name)
        return jsonify(RepositoryData.from_repository(repo)), 200


@repos_bp.route("/", methods=["POST"])
@token_required
def create_repo():
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not name:
        raise BadRequestError("Campo 'name' é obrigatório")

    description = data.get("description", None)
    private = data.get("private", False)
    auto_init = data.get("auto_init", True)
    gitignore_template = data.get("gitignore_template", "Python")
    license_template = data.get("license_template", "mit")

    with GithubController(g.token, True) as git:
        repo = git.create_repo(
            name=name,
            description=description,
            private=private,
            auto_init=auto_init,
            gitignore_template=gitignore_template,
            license_template=license_template
        )
        return jsonify(RepositoryData.from_repository(repo)), 201


@repos_bp.route('/<string:repo_name>', methods=['DELETE'])
@token_required
def delete_repo(repo_name: str):
    with GithubController(g.token, True) as git:
        result = git.delete_repo(repo_name)
        return jsonify(result), 200
    

@repos_bp.route('/<string:repo_name>/files', methods=['GET'])
@token_required
def list_files(repo_name: str):
    path = request.args.get('path', '')
    branch = request.args.get('branch', 'main')

    with GithubController(g.token, True) as git:
        files = git.list_files(repo_name, path, branch)
        return jsonify(
            [ContentFileData.from_content_file(file) for file in files]
        ), 200


@repos_bp.route('/<string:repo_name>/files/<string:path>', methods=['GET'])
@token_required
def get_file(repo_name: str, path: str):
    branch = request.args.get('branch', 'main')
    with GithubController(g.token, True) as git:
        file = git.get_file(repo_name, path, branch)
        return jsonify(ContentFileData.from_content_file(file)), 200


@repos_bp.route('/<string:repo_name>/files', methods=['POST'])
@token_required
def upload_file(repo_name: str):
    branch = request.args.get('branch', 'main')
    
    file = request.files.get("file")
    
    path = request.form.get("path")
    message = request.form.get("message", "Add file via script")


    if not path or not file:
        raise BadRequestError("Campos 'path' e 'file' são obrigatórios")


    with GithubController(g.token, True) as git:
        result = git.upload_file(
            repo_name=repo_name,
            path=path,
            content=file,
            message=message,
            branch=branch
        )

    return jsonify(ContentFileData.from_content_file(result)), 201



@repos_bp.route('/<string:repo_name>/files/<path:path>', methods=['PUT'])
@token_required
def update_file(repo_name: str, path: str):
    branch = request.args.get('branch', 'main')

    file = request.files.get('file')   # campo "file" com o novo conteúdo
    message = request.form.get('message', 'Update file via script')

    if not file:
        raise BadRequestError("Campos 'file' (novo conteúdo) é obrigatório")

    with GithubController(g.token, True) as git:
        result = git.update_file_content(
            repo_name=repo_name,
            path=path,
            new_content=file,  # file-like
            message=message,
            branch=branch
        )

    return jsonify(ContentFileData.from_content_file(result)), 200



@repos_bp.route('/<string:repo_name>/files/<string:path>', methods=['DELETE'])
@token_required
def delete_file(repo_name: str, path: str):
    branch = request.args.get('branch', 'main')
    data = request.get_json(silent=True) or {}
    message = data.get('message', 'Delete file via script')
    with GithubController(g.token, True) as git:
        result = git.delete_file(
            repo_name,
            path,
            message,
            branch
        )

        return jsonify(result), 200
    

