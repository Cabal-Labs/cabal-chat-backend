from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
