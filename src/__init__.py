from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Init db
db = SQLAlchemy()


def create_app():
    # Load env variables
    load_dotenv()

    # Create app
    app = Flask(__name__)
    # Handling CORS
    # CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
    CORS(app)

    # Config section
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER"),
            DB_PASSWORD=os.getenv("DB_PASSWORD"),
            DB_HOST=os.getenv("DB_HOST"),
            DB_NAME=os.getenv("DB_NAME"),
        )
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connect the db to app
    db.init_app(app)

    # Init migration
    migrate = Migrate(app, db)

    # Import routes
    from src.routes.auth_routes import auth_bp
    from src.routes.book_routes import book_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(book_bp, url_prefix="/api/v1/books")

    return app
