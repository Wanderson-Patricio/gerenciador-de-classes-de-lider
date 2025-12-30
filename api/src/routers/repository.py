from flask import Blueprint, jsonify, request
from ..models import RepositoryData
from ..controllers import GithubManager
from ..errors import GithubException

# Criar um Blueprint para rotas de usuários
repos_bp = Blueprint("repositories", __name__)

@repos_bp.route("/", methods=["GET"])
def list_repos():
    token = request.headers.get('x-api-token')
    try:
        with GithubManager(token, True) as git:
            repos = git.get_repos()
            return jsonify(
                [RepositoryData.from_repository(repo) for repo in repos]
            )
    except GithubException as e:
        return jsonify(e.send_error()), e.status_code

@repos_bp.route("/<string:repo_name>", methods=["GET"])
def get_repo(repo_name: str):
    token = request.headers.get('x-api-token')
    try:
        with GithubManager(token, True) as git:
            repo = git.get_repo_by_name(repo_name)
            return jsonify(RepositoryData.from_repository(repo))
    except GithubException as e:
        return jsonify(e.send_error()), e.status_code