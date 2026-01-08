from app import app
from api.src.routers.repository import repos_bp
from docs.docs_bp import docs_bp

# Registrar os Blueprints
app.register_blueprint(repos_bp, url_prefix="/api/repositories")
app.register_blueprint(docs_bp, url_prefix="/docs")

if __name__ == "__main__":
    app.run(debug=True, port=3000)