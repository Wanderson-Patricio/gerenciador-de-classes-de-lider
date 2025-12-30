from flask import Blueprint, jsonify, request, g
from ..models import RepositoryData
from ..controllers import GithubManager
from ..errors import GithubException
from .token_required import token_required

# Criar um Blueprint para rotas de repositórios
repos_bp = Blueprint("repositories", __name__)

@repos_bp.errorhandler(GithubException)
def handle_github_exception(e):
    return jsonify(e.send_error()), e.status_code

@repos_bp.route("/", methods=["GET"])
@token_required
def list_repos():
    with GithubManager(g.token, True) as git:
        repos = git.get_repos()
        return jsonify(
            [RepositoryData.from_repository(repo) for repo in repos]
        )

@repos_bp.route("/<string:repo_name>", methods=["GET"])
@token_required
def get_repo(repo_name: str):
    with GithubManager(g.token, True) as git:
        repo = git.get_repo_by_name(repo_name)
        return jsonify(RepositoryData.from_repository(repo))
    
@repos_bp.route("/", methods=["POST"])
@token_required
def create_repo():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", None)
    private = data.get("private", False)
    auto_init = data.get("auto_init", True)
    gitignore_template = data.get("gitignore_template", "Python")
    license_template = data.get("license_template", "mit")

    with GithubManager(g.token, True) as git:
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
    with GithubManager(g.token, True) as git:
        result = git.delete_repo(repo_name)
        return jsonify(result), 200