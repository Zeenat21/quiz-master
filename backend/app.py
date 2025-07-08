from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from auth import auth_bp
from routes import admin_routes, user_routes
from initial_data import create_admin
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_routes)
    
    app.register_blueprint(user_routes)

    # Create tables and admin if not already done
    create_admin(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
