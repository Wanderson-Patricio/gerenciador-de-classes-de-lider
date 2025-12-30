from flask import Flask
from api.src.routers.repository import repos_bp

app = Flask(__name__)

# Registrar os Blueprints
app.register_blueprint(repos_bp, url_prefix="/api/repositories")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
