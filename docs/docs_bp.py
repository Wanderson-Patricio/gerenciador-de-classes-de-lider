from flask import Blueprint, render_template

docs_bp = Blueprint("docs", __name__, template_folder='templates', static_folder='static')

@docs_bp.route("/api")
def api_docs():
    return render_template('api_docs.html')

@docs_bp.route("/")
def home_docs():
    return render_template('docs.html')